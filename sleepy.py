import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 메일 제목 입력
from_subject = st.text_input('메일 제목')

# 보내는 사람 E-mail 입력
from_email = st.text_input('보내는 사람 E-mail')

# 본문 내용 입력
from_content = st.text_area('본문 내용', height=5)

# 첨부파일 업로드
from_file = st.file_uploader('첨부파일', type=['csv', 'txt', 'xls', 'xlsx'])

# 입력된 내용 출력
st.write('메일 제목:', from_subject)
st.write('보내는 사람 E-mail:', from_email)
st.write('본문 내용:', from_content)

# 첨부파일 확인
if from_file is not None:
    st.write('첨부된 파일 이름:', from_file.name)

# 메일 전송 함수
def send_email(subject, from_email, to_email, content, file=None):
    my_mail = 'kstobit@naver.com'  # 송신자 이메일 주소
    pwd = '9146531!@'  # 송신자 이메일 비밀번호
    smtp_name = "smtp.naver.com"  # SMTP 서버 이름
    smtp_port = 587  # SMTP 포트 번호

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    msg.attach(MIMEText(content, 'plain'))

    if file is not None:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % file.name)
        msg.attach(part)

    try:
        s = smtplib.SMTP(smtp_name, smtp_port)
        s.starttls()
        s.login(my_mail, pwd)
        s.sendmail(from_email, to_email, msg.as_string())
        s.quit()
        st.success('메일이 성공적으로 전송되었습니다.')
    except Exception as e:
        st.error(f'메일 전송에 실패했습니다: {e}')

# 메일 전송 버튼
if st.button('메일 전송'):
    if from_subject and from_email and from_content:
        send_email(from_subject, from_email, 'kstobit@naver.com', from_content, from_file)
    else:
        st.warning('모든 필드를 입력해 주세요.')
