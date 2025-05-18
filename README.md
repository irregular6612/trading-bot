# Trading Bot

암호화폐 및 주식 거래를 위한 실시간 모니터링 및 분석 도구입니다.

## 주요 기능

- 실시간 시세 조회
  - 캔들스틱 차트 시각화
  - 거래량 분석
  - 실시간 가격 업데이트
- 보유 자산 현황 조회
- 투자 종목 분석

## 기술 스택

- Python 3.x
- Streamlit
- PyUpbit API
- Plotly
- Pandas
- NumPy

## 설치 방법

1. 저장소 클론
```bash
git clone [repository-url]
cd trading-bot
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정합니다:
```
DOMAIN_URL=
PRICE_URL=
ACCESS_TOKEN_URL=
BALANCE_URL=
ORDER_URL=
CANCEL_URL=
APP_KEY=
APP_SECRET=
ACCOUNT_NO=
ACCOUNT_CODE=
ACCESS_TOKEN=
```

## 실행 방법

```bash
streamlit run streamlit_test.py
```

## 프로젝트 구조

```
trading-bot/
├── streamlit_test.py    # 메인 애플리케이션 파일
├── requirements.txt     # 의존성 패키지 목록
├── .env                # 환경 변수 설정 파일
└── README.md          # 프로젝트 문서
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 