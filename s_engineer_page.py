from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# ChromeDriver 경로 설정
service = Service('C:/Users/pnpadmin/AppData/Local/Programs/Python/chromedriver-win64/chromedriver.exe')

# Chrome 옵션 설정 (HTTPS 인증서 오류 무시)
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')  # 로컬 HTTPS 인증서 오류 무시

# WebDriver 객체 생성
driver = webdriver.Chrome(service=service, options=chrome_options)

# 페이지로 이동
driver.get('https://192.168.2.214:3443/saferuas/engineer')

# 페이지 로딩 대기
time.sleep(3)

# 아이디 입력
username = driver.find_element(By.ID, 'userId')  # 'userId'는 id 속성
username.send_keys('secureadmin')

# 비밀번호 입력
password = driver.find_element(By.ID, 'userPw')  # 'userPw'는 id 속성
password.send_keys('secure1818##')

# 로그인 버튼 클릭
login_button = driver.find_element(By.ID, 'loginBt')  # 'loginBt'는 로그인 버튼의 id 속성
login_button.click()

# 로그인 후 대기 시간 (필요에 따라 수정)
time.sleep(5)

# '보안계정 별 2차인증' 체크박스 찾기
sauthType_checkbox = driver.find_element(By.ID, 'sauthType_user')

# 체크 여부 확인 및 체크
if not sauthType_checkbox.is_selected():
    sauthType_checkbox.click()

# OTP 유효 시간 값을  변경
otp_time_input = driver.find_element(By.ID, 'otpRuleTime')
otp_time_input.clear()  # 기존 값을 지우고
otp_time_input.send_keys('180')  # 새로운 값을 입력

# 저장 버튼 클릭
save_button = driver.find_element(By.ID, 'saveBt')
save_button.click()

# 대기 후 브라우저 종료 (원하는 경우 주석 처리 가능)
time.sleep(3)
driver.quit()


exec(open("s_login.py", encoding='utf-8').read())
