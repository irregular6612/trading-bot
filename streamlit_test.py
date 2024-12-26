import json  # JSON 파싱
import requests
#import boto3
import streamlit as st
from streamlit_echarts import st_echarts, st_pyecharts
import os
from dotenv import load_dotenv

load_dotenv()


#bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
DOMAIN_URL=os.getenv("DOMAIN_URL")
PRICE_URL=os.getenv("PRICE_URL")
ACCESS_TOKEN_URL=os.getenv("ACCESS_TOKEN_URL")
BALANCE_URL=os.getenv("BALANCE_URL")
ORDER_URL=os.getenv("ORDER_URL")
CANCEL_URL=os.getenv("CANCEL_URL")
APP_KEY=os.getenv("APP_KEY")
APP_SECRET=os.getenv("APP_SECRET")
ACCOUNT_NO=os.getenv("ACCOUNT_NO")
ACCOUNT_CODE=os.getenv("ACCOUNT_CODE")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")

# 웹 앱 제목 설정
st.title("Trading Bot")

def get_access_token():
    global ACCESS_TOKEN

    if ACCESS_TOKEN != '':
        return ACCESS_TOKEN
    else:   
        request_url = DOMAIN_URL + ACCESS_TOKEN_URL
        headers = {
            "content-type": "application/json"
        }
        body = {
            "appkey": APP_KEY,
            "appsecret": APP_SECRET,
            "grant_type": "client_credentials",
        }
        response = requests.post(request_url, headers=headers, json=body)
        print(response.json())
        ACCESS_TOKEN = response.json()['access_token']
        os.environ['ACCESS_TOKEN'] = ACCESS_TOKEN
        return ACCESS_TOKEN


def current_price():
    ticker = "065350"
    request_url = DOMAIN_URL + PRICE_URL
    headers = {
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPST01010000"
    }
    query_params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": ticker
    }
    response = requests.get(request_url, headers=headers, params=query_params)
    return response.json()['output']['prdy_ctrt']
    #return response.json()




"""
# 세션 상태에 메시지 없으면 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 세션 상태에 저장된 메시지 순회하며 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # 채팅 메시지 버블 생성
        st.markdown(message["content"])  # 메시지 내용 마크다운으로 렌더링
"""

def get_response(prompt):
    try:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            }
        )
        return "Hello World"
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body,
        )
        response_body = json.loads(response.get("body").read())
        output_text = response_body["content"][0]["text"]
        return output_text
    except Exception as e:
        print(e)

"""
# 사용자로부터 입력 받음
if prompt := st.chat_input("Message Bedrock..."):
    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):  # 사용자 메시지 채팅 메시지 버블 생성
        st.markdown(prompt)  # 사용자 메시지 표시
    price = current_price()
    # 보조 응답을 세션 상태에 추가
    output_text = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": output_text}) # 보조 메시지 채팅 메시지 버블 생성
    with st.chat_message("assistant"):
        st.markdown(price)
        st.markdown(ACCESS_TOKEN)
"""

option = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [{"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)




