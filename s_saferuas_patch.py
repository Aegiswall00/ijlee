import time
import os
import paramiko
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 웹사이트에 접속하고 로그인하여 파일 다운로드
def download_file():
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": r"C:\Users\pnpadmin\Downloads"}  # 파일 다운로드 경로 설정
    options.add_experimental_option("prefs", prefs)
    
    # SSL 오류 무시 설정 추가
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    
    # ChromeDriver 서비스 설정
    service = Service(r'C:/Users/pnpadmin/AppData/Local/Programs/Python/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://bbs.pnpsecure.com/showthread.php?tid=13867")

    # 로그인 페이지가 로드될 때까지 기다림
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    # 로그인 과정
    username_field.send_keys("ijlee")
    password_field.send_keys("dbsafer00")
    driver.find_element(By.CLASS_NAME, "button").click()  # 로그인 버튼 클릭
    time.sleep(2)

    # 파일 다운로드 링크 클릭
    driver.get("https://bbs.pnpsecure.com/attachment.php?aid=47963")
    time.sleep(5)  # 파일이 다운로드될 시간을 충분히 줌

    driver.quit()

# SSH를 통해 서버에 파일 업로드 및 스크립트 실행
def upload_file_to_server(local_path, remote_path, hostname, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)

        # SFTP를 통한 파일 업로드
        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        print("파일 업로드 성공")
        logging.info("파일 업로드 성공")
        # patch.sh 스크립트 실행
        print("패치 스크립트 실행 중...")
        stdin, stdout, stderr = ssh.exec_command("cd /root/PKG_saferuas_patch && chmod +x patch.sh && ./patch.sh")
        
        # 스크립트 실행 결과 출력
        print("스크립트 실행 결과:")
        logging.info("safeuas 패치중 1분 정도 기다리세요")
        print(stdout.read().decode())
        print("스크립트 에러 메시지 (있는 경우):")
        print(stderr.read().decode())
        
    except FileNotFoundError:
        print(f"로컬 파일을 찾을 수 없습니다: {local_path}")
    except IOError as e:
        print(f"파일 업로드 실패: {e}")
    except paramiko.SSHException as e:
        print(f"SSH 연결 오류: {e}")
    finally:
        ssh.close()
        print("SSH 연결이 종료되었습니다.")
        logging.info("SSH 연결이 종료되었습니다.")

# 실행 코드
if __name__ == "__main__":
    # 파일 다운로드
    download_file()

    # 다운로드한 파일 경로 설정
    downloaded_file_path = r"C:\Users\pnpadmin\Downloads\saferuas.war.2.0.83.0_Build-2276_202410101327.tgz"  # 실제 파일명을 다운로드 후 확인하여 입력
    remote_path = "/root/PKG_saferuas_patch/patch_file/saferuas.war.2.0.83.0_Build-2276.tgz"  # 서버에 저장할 경로와 파일명

    # 서버에 파일 업로드 및 스크립트 실행
    upload_file_to_server(
        local_path=downloaded_file_path,
        remote_path=remote_path,
        hostname='192.168.2.214',
        port=7795,
        username='root',
        password='dbsafer00'
    )


exec(open("s_saferuas_check.py", encoding='utf-8').read())
    
