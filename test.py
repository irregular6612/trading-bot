import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import time
import requests
import json
import os
import sys
import logging
import warnings

# 데이터 저장용 리스트
prices = []
times = []

# 그래프 초기화
fig, ax = plt.subplots(figsize=(12, 6))
line, = ax.plot([], [], 'b-', label='주가 등락률')

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


request_url = DOMAIN_URL + ACCESS_TOKEN_URL
def get_access_token():
    headers = {
        "content-type": "application/json"
    }
    body = {
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(request_url, headers=headers, json=body)
    return response.json()['access_token']
access_token = get_access_token()
print(access_token)

def current_price():
    request_url = DOMAIN_URL + PRICE_URL
    headers = {
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPST01010000"
    }
    query_params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": "065350"
    }
    response = requests.get(request_url, headers=headers, params=query_params)
    return response.json()['output']['prdy_ctrt']
    #return response.json()
current_price()
    
def animate(i):
    # 현재 가격 조회
    price = current_price()
    current_time = datetime.datetime.now()
    print(price, current_time)
    if price:
        # 데이터 추가
        prices.append(float(price))
        times.append(current_time)
        
        # 최근 30개 데이터만 표시
        if len(prices) > 30:
            prices.pop(0)
            times.pop(0)
        
        # 그래프 업데이트
        ax.clear()
        ax.plot(times, prices, 'b-')
        
        # 그래프 스타일링
        ax.set_title('실시간 주가 등락률')
        ax.set_xlabel('시간')
        ax.set_ylabel('등락률 (%)')
        ax.grid(True)
        
        # x축 시간 포맷 설정
        plt.gcf().autofmt_xdate()
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))

# 애니메이션 설정 (1초마다 업데이트)
ani = FuncAnimation(
    fig, 
    animate, 
    interval=1,
    cache_frame_data=False,
    save_count=None
)

plt.tight_layout()
plt.show()