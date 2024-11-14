import paramiko
import subprocess

# 정보 입력
A_IP="10.1.2.3"
A_USER="test_user"
A_PW="mypassword"
A_DB="test_world" 

B_IP="10.1.2.4"
B_USER="svc_user"
B_PW="mypassword!@#"
B_DB="svc_world"

# 파일 경로 설정
A_BEFORE_PATH="/home/myhome/sample_before.txt"
A_AFTER_PATH="/home/myhome/sample_after.txt"
B_PATH="/home/yourhome"

# A 서버에서 파일 수정
def A_file_modify():
    # A 서버에 연결
    ssh = paramiko.SSHClient() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(A_IP, username=A_USER, password=A_PW)
    
    # 파일 복사 및 수정 명령어
    cmd = (
        f"cp {A_BEFORE_PATH} {A_AFTER_PATH} && "
        f"sed -i -e 's/IP: {A_IP}/IP: {B_IP}/' "
        f"-e 's/database: \"{A_DB}\"/database: \"{B_DB}\"/' "
        f"-e 's/username: \"{A_USER}\"/username: \"{B_USER}\"/' "
        f"-e 's/password: \"{A_PW}\"/password: \"{B_PW}\"/' "
        f"{A_AFTER_PATH} && ls {A_AFTER_PATH}"
    )
    
    ssh.exec_command(cmd)
    ssh.close()
    
# A 서버에서 B 서버로 파일 전송
def A_to_B():
    scp_cmd = [
        "scp",
        f"{A_USER}@{A_IP}:{A_AFTER_PATH}",
        f"{B_USER}@{B_IP}:{B_PATH}"
    ]
    
    subprocess.run(scp_cmd, check=True, text=True, capture_output=True)

# 함수 실행
if __name__ == "__main__":    
    A_file_modify()
    A_to_B()
        