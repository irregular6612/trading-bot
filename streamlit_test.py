import json  # JSON 파싱
import requests
#import boto3
import streamlit as st
from streamlit_echarts import st_echarts, st_pyecharts
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import pandas as pd
import numpy as np
import schedule
import pyupbit
import mplfinance as mpf
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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


# 탭 컨테이너 생성
tabs = st.tabs(['시세 조회', '보유 자산 현황', '눈에 띠는 투자 종목'])

# 주식 데이터 가져오는 함수
def fetch_stock_data():
    # 예제 데이터 생성 (실제로는 API 호출)
    data = {
        #"time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "time": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "price": np.random.randint(low=0, high=100, size=7).tolist(),
    }
    return data
 
# 첫 번째 탭에 내용 추가
with tabs[0]:
    st.header('시세 조회')
    item_code = "065350 삼성전자"
    st.write(f"종목명: {item_code}")
    refresh_interval = st.slider('새로고침 간격(초)', 1, 10, 5)


    if st.button('실시간 조회 시작'):
        chart_container = st.empty()
        current_price_container = st.empty()
        volume_container = st.empty()
        price_container = st.empty()

        while True:
            minute1 = pyupbit.get_ohlcv("KRW-BTC", "minute1")        
            go.Figure().data = []

            candle_chart = go.Figure(data=[go.Candlestick(x=minute1.index,
                    open=minute1['open'], high=minute1['high'],
                    low=minute1['low'], close=minute1['close'])])
            candle_chart.update_layout(title=f"{item_code} Candlestick Chart", xaxis_rangeslider_visible=False)    
            price = pyupbit.get_current_price("KRW-BTC")
            volume = minute1['volume']

            chart_container.plotly_chart(candle_chart, use_container_width=True, key=f"candle_chart_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            price_container.write(f"현재 시세: {price}")
            volume_container.bar_chart(minute1['volume'])
        
            time.sleep(refresh_interval)
        
    
 
# 두 번째 탭에 내용 추가
with tabs[1]:
    st.header('보유 자산 현황')
    st.write('이것은 탭 2의 내용입니다.')
    
 
# 세 번째 탭에 내용 추가
with tabs[2]:
    st.header('눈에 띠는 투자 종목')
    st.write('이것은 탭 3의 내용입니다.')

