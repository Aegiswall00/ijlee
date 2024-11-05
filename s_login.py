from pywinauto import application
import time
import logging
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
from datetime import datetime, timedelta

# 로그 출력을 위한 함수
def log_message(message):
    print(f"[LOG] {message}")

# DBSAFER AGENT 실행 경로
app_path = r'C:\Program Files (x86)\PNPSECURE\DBSAFER AGENT\DBSaferAgt.exe'

# 관리자 권한으로 DBSAFER AGENT 실행
logging.info("DBSAFER AGENT 실행 중...")
log_message("DBSAFER AGENT 실행 중...")
subprocess.run(["powershell", "Start-Process", f'"{app_path}"', "-Verb", "runAs"])

# 애플리케이션이 열리는 동안 잠시 대기
time.sleep(10)

# pywinauto를 사용하여 애플리케이션에 연결
try:
    app = application.Application().connect(title="DB보안 사용자 인증", timeout=10)
    logging.info("DBSAFER AGENT 1차 연결 성공")
    log_message("DBSAFER AGENT 1차 연결 성공")
except Exception as e:
    log_message(f"DBSAFER AGENT 1차 연결 실패: {e}")
    logging.info(f"DBSAFER AGENT 1차 연결 실패: {e}")
    exit()

# 로그인 창에 대한 핸들 얻기
dlg = app.window(title="DB보안 사용자 인증")

# 사용자 ID 'test_e' 입력
dlg.Edit1.type_keys('test_e')

# 비밀번호 'dbsafer00' 입력
dlg.Edit2.type_keys('dbsafer00')

# '확인' 버튼 클릭
dlg.Button1.click()

# OTP 창이 뜰 때까지 대기
time.sleep(5)

# ---------------- Gmail에서 OTP 가져오기 ----------------

# ChromeDriver 설정 및 브라우저 열기
log_message("Chrome 브라우저 열기...")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Gmail 로그인 페이지로 이동
driver.get("https://mail.google.com/")
time.sleep(2)

# 이메일 입력
log_message("Gmail 로그인 중...")
logging.info("Gmail 로그인 중...")
email_input = driver.find_element(By.ID, "identifierId")
email_input.send_keys("ijlee@pnpsecure.com")
email_input.send_keys(Keys.ENTER)
time.sleep(3)

# 비밀번호 입력 필드를 찾을 때까지 대기 (최대 10초)
try:
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Passwd"))
    )
    password_input.send_keys("Aegiswall00!@")
    password_input.send_keys(Keys.ENTER)
    log_message("Gmail 로그인 성공")
    logging.info("Gmail 로그인 성공")
except Exception as e:
    log_message(f"비밀번호 입력 필드를 찾는 도중 오류 발생: {e}")
    logging.info(f"비밀번호 입력 필드를 찾는 도중 오류 발생: {e}")
    driver.quit()
    exit()

# 2단계 인증 대기
log_message("2단계 인증 진행 중...")
time.sleep(30)

# 이메일 발송 지연을 고려해 15초 대기
log_message("메일 발송 지연을 고려해 15초 대기...")
time.sleep(15)

# 이메일 제목 "test_ijlee_maile"로 검색 후 결과가 나올 때까지 대기
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys('subject:test_ijlee_maile')
search_box.send_keys(Keys.ENTER)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tr.zA"))
    )
    log_message("이메일 검색 완료")
    time.sleep(5)
except Exception as e:
    log_message(f"이메일 검색 결과를 기다리는 중 오류 발생: {e}")
    driver.quit()
    exit()

try:
    first_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'test_ijlee_maile')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", first_email)
    driver.execute_script("arguments[0].click();", first_email)
    log_message("이메일 클릭 완료")
    time.sleep(3)
except Exception as e:
    log_message(f"이메일을 클릭하는 도중 오류 발생: {e}")
    driver.quit()
    exit()

# 이메일 본문에서 마지막 6자리 숫자 추출
try:
    # 이메일 본문 요소 로드 대기
    email_body_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.a3s.aiL"))
    )
    email_body = driver.execute_script("return arguments[0].innerText;", email_body_element)
    log_message(f"이메일 본문 내용: {email_body}")

    # 6자리 숫자 모두 찾은 후 가장 마지막 항목을 선택
    otp_codes = re.findall(r"\b\d{6}\b", email_body)  # 단어 경계를 사용해 확실하게 6자리만 추출
    if otp_codes:
        otp_code = otp_codes[-1]  # 가장 마지막 6자리 숫자 선택
        log_message(f"OTP 코드 추출 성공: {otp_code}")
    else:
        log_message("6자리 숫자를 찾을 수 없음")
except Exception as e:
    log_message(f"이메일 내용을 가져오는 도중 오류 발생: {e}")
    driver.quit()
    exit()

# 브라우저 닫기
driver.quit()

# ---------------- OTP 자동 입력 ----------------

# OTP 인증 창을 제대로 인식했는지 확인
try:
    dlg_otp = app.window(title="OTP 인증")
    dlg_otp.wait("exists ready", timeout=10)
    log_message("OTP 인증창이 확인되었습니다.")

    dlg_otp.Edit.type_keys(otp_code)
    dlg_otp.Button1.click()
    log_message("OTP 코드 입력 완료.")
    time.sleep(2)
except Exception as e:
    log_message(f"OTP 인증창을 찾는 도중 오류 발생: {e}")
    exit()


exec(open("s_log_check.py", encoding='utf-8').read())

