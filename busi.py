import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail():
    st.header("메일 보내기")

    with st.form(key='email_form'):
        # 메일 폼 작성
        from_subject = st.text_input("메일 제목", key='m_subject')
        from_id = st.text_input("보내는 사람 E-mail", key='m_id')
        from_content = st.text_area("본문 내용", height=5, key='m_content')
        from_file = st.file_uploader("첨부파일", type=['csv', 'txt', 'xls', 'xlsx'], key='m_file')

        # 폼 제출 버튼
        submit_button = st.form_submit_button(label='메일 보내기')

    if submit_button:
        # 업로드된 파일을 로컬에 저장
        if from_file is not None:
            with open(from_file.name, 'wb') as file:
                file.write(from_file.getbuffer())

        # 메일에 첨부
        msg = MIMEMultipart()
        msg['From'] = from_id
        msg['To'] = 'kstobit@naver.com'  # 수신자 이메일 주소
        msg['Subject'] = from_subject

        # 본문 내용 첨부
        msg.attach(MIMEText(from_content, 'plain'))

        if from_file is not None:
            with open(from_file.name, 'rb') as f:
                file_data = MIMEBase('application', 'octet-stream')  # 바이너리 객체 변환
                file_data.set_payload(f.read())
            encoders.encode_base64(file_data)
            file_data.add_header('Content-Disposition', 'attachment', filename=from_file.name)
            msg.attach(file_data)

        # 이메일 전송 - 서버 설정
        try:
            smtp = smtplib.SMTP("smtp.naver.com", 587)
            smtp.starttls()  # 보안 설정
            smtp.login(user='kstobit@naver.com', password='9146531!@')
            smtp.sendmail(from_id, 'kstobit@naver.com', msg.as_string())
            smtp.quit()
            st.success('메일이 성공적으로 전송되었습니다.')
        except Exception as e:
            st.error(f'메일 전송에 실패했습니다: {e}')
