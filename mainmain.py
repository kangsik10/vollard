import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
from io import BytesIO
import busi

# Function to fetch exchange rate data
def get_exchange_rate_data(currency_code, last_page_num):
    base_url = "https://finance.naver.com/marketindex/exchangeDailyQuote.naver"
    df = pd.DataFrame()
    
    for page_num in range(1, last_page_num + 1):
        url = f"{base_url}?marketindexCd={currency_code}&page={page_num}"
        dfs = pd.read_html(url, header=1, encoding='cp949')
        
        # 통화 코드가 잘못 지정됐거나 마지막 페이지의 경우 for 문을 빠져나옴
        if dfs[0].empty:
            if page_num == 1:
                st.error(f"통화 코드({currency_code})가 잘못 지정됐습니다.")
            else:
                st.info(f"{page_num}가 마지막 페이지입니다.")
            break
            
        # page별로 가져온 DataFrame 데이터 연결
        df = pd.concat([df, dfs[0]], ignore_index=True)
        time.sleep(0.1)  # 0.1초간 멈춤
        
    return df

# Sidebar for login
st.sidebar.header("로그인")
user_id = st.sidebar.text_input('아이디(ID) 입력', value="streamlit", max_chars=15)
user_password = st.sidebar.text_input('패스워드(Password) 입력', value="", type="password")

if user_password == '1234':

    st.sidebar.header("시기의 포트폴리오")

    menu = st.sidebar.radio("메뉴 선택", ['환율 조회', '부동산 조회(EDA)', '인공지능 예측/분류'])

    if menu == '환율 조회':
        st.title("환율 데이터 앱")

        # 통화 정보 딕셔너리
        currency_dict = {
            "USD": "FX_USDKRW",
            "EUR": "FX_EURKRW",
            "JPY": "FX_JPYKRW",
        }

        # 콤보상자로 통화 선택
        currency_name = st.selectbox("통화를 선택하세요", list(currency_dict.keys()))
        currency_code = currency_dict[currency_name]
        last_page_num = st.slider("페이지 수 선택", 1, 10, 5)

        if st.button("데이터 가져오기"):
            exchange_rate_df = get_exchange_rate_data(currency_code, last_page_num)
            st.dataframe(exchange_rate_df)  # 환율 데이터 표시

            if not exchange_rate_df.empty:
                # 날짜 형식을 datetime으로 변환
                exchange_rate_df['날짜'] = pd.to_datetime(exchange_rate_df['날짜'], format='%Y.%m.%d')

                # 차트 그리기(선그래프, 판다스 이용)
                plt.figure(figsize=(10, 5))
                plt.plot(exchange_rate_df['날짜'], exchange_rate_df['매매기준율'])
                plt.title(f"{currency_name} 환율 추이")
                plt.xlabel('날짜')
                plt.ylabel('매매기준율')
                plt.grid(True)
                st.pyplot(plt)

                # Prepare CSV data
                csv_data = exchange_rate_df.to_csv(index=False).encode('utf-8-sig')

                # Prepare Excel data
                excel_data = BytesIO()
                exchange_rate_df.to_excel(excel_data, index=False, engine='xlsxwriter')
                excel_data.seek(0)

                # Download buttons
                st.subheader("==환율 데이터 다운로드 ==")
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="CSV 파일 다운로드",
                        data=csv_data,
                        file_name=f"{currency_name}_exchange_rate.csv",
                        mime='text/csv',
                    )
                with col2:
                    st.download_button(
                        label="엑셀 파일 다운로드",
                        data=excel_data,
                        file_name=f"{currency_name}_exchange_rate.xlsx",
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    )

    elif menu == "부동산 조회(EDA)":
        st.sidebar.write("부동산 조회(EDA)")
        # Placeholder for real estate data analysis code

    elif menu == "인공지능 예측/분류":
        st.sidebar.write("인공지능 예측/분류")
        # Placeholder for AI prediction/classification code

    st.sidebar.markdown("---")
    if st.sidebar.button("메일 문의"):
        st.session_state.menu = '메일 보내기'

    if 'menu' in st.session_state and st.session_state.menu == '메일 보내기':
        busi.send_mail()

else:
    st.sidebar.error("패스워드가 올바르지 않습니다.")
