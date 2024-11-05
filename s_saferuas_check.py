import paramiko
import os
import time

# SSH dbsafer 서버 정보 
hostname = '192.168.2.214'
port = 7795
username = 'root'
password = 'dbsafer00'

def log_message(message):
    print(f"[LOG] {message}")

# AUTH_SITE 확인 
def check_auth_site():
    try:
        # SSH 클라이언트 생성 및 설정
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 서버에 접속
        ssh.connect(hostname, port=port, username=username, password=password)
        
        # 파일 읽기 명령어 실행
        stdin, stdout, stderr = ssh.exec_command('cat /dbsafer/.conf/pnp_oms_dms.conf')
        
        # 내용 읽기 및 인코딩 처리
        file_content = stdout.read().decode('latin-1')
        
        # AUTH_SITE 설정 확인 로직
        if 'AUTH_SITE = 9' in file_content and '#AUTH_SITE = 9' not in file_content:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return False
    
    finally:
        # SSH 연결 종료
        ssh.close()

# dasitelk.ini 파일 확인
def check_dasitelk_file():
    filepath = r'C:\Program Files (x86)\PNPSECURE\DBSAFER AGENT\dasitelk.ini'
    return os.path.exists(filepath)

# 메인 함수
def main():
    auth_site_status = check_auth_site()
    dasitelk_file_status = check_dasitelk_file()
    
    # 조건에 따라 로그 출력
    if auth_site_status and dasitelk_file_status:
        log_message("saferuas 준비 완료 다음 단계로")
    else:
        log_message("saferuas 준비 설정 부족")

# 실행 및 다음 py 전환
if __name__ == "__main__":
    main()
    time.sleep(2)

exec(open("s_engineer_page.py", encoding='utf-8').read())

