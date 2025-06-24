# 📊 성남시 음식점 리뷰 감성 분석 시스템

[![Streamlit App](https://img.shields.io/badge/Streamlit-Deployed-brightgreen?logo=streamlit)](https://share.streamlit.io/your-deployment-link)

> 네이버 지도에서 수집한 음식점 리뷰를 기반으로 감성 분석을 수행하고 시각적으로 분석 결과를 보여주는 Streamlit 기반 웹 애플리케이션입니다.

---

## 🧠 주요 기능

- ✅ **리뷰 기반 감성 분석** (긍정 / 중립 / 부정)
- ✅ **감정 비율 파이차트 시각화**
- ✅ **GPT-4 기반 장점/개선점 요약**
- ✅ **감정별 워드클라우드 생성**
- ✅ **개별 리뷰 실시간 감성 분석**
- ✅ **자동완성 검색 UI (음식점명 입력 시 유사 항목 제시)**

---

## 📁 프로젝트 구조

```
📦seongnam-restaurant-sentiment-analysis
┣ 📂kc_electra_sentiment_model_0624_3
┃ ┣ config.json
┃ ┣ pytorch_model.bin
┃ ┣ tokenizer.json
┣ 📂.streamlit
┃ ┣ config.toml
┃ ┗ secrets.toml (배포용 API 키)
┣ 📜App.py # Streamlit 메인 앱
┣ 📜ModelLoader.py # 모델 로드 함수
┣ 📜SentimentPredictor.py # 감성 분석 수행
┣ 📜Visualization.py # 파이차트 / 워드클라우드 등 시각화
┣ 📜TextProcessor.py # 키워드 추출
┣ 📜ReviewSummary.py # GPT 요약 함수
┣ 📜restaurant_reviews.csv # 수집된 리뷰 데이터
┣ 📜requirements.txt
┣ 📜packages.txt # Java 필요 패키지
┗ 📜README.md
```

---

## 🧬 감성 분석 모델

| 모델 | 설명 |
|------|------|
| `LSTM` | 형태소 분석 후 시퀀스 입력, Keras 기반 감성 분류 |
| `KcELECTRA` | HuggingFace `beomi/KcELECTRA-base`, 한국어에 특화된 Transformer 모델 |

현재 앱에서는 정확도가 더 높은 **KcELECTRA 모델**을 사용 중입니다.

---

## 🌐 사용 방법

1. **환경 준비 (로컬 실행 시)**

```
# 가상환경 설치 (권장)
conda create -n senti python=3.9
conda activate senti

# 필수 라이브러리 설치
pip install -r requirements.txt
실행

streamlit run App.py
웹 페이지 접속
```

앱이 브라우저에서 자동으로 실행됩니다 (localhost:8501)

## 📦 배포 환경 (Streamlit Cloud)
Konlpy 사용을 위해 packages.txt에 Java 런타임을 포함해야 합니다.


# packages.txt
default-jre
그리고 .streamlit/secrets.toml에는 OpenAI API 키를 포함시켜야 합니다.


# secrets.toml
OPENAI_API_KEY = "sk-..."

## 🧹 사용 기술
분야	기술 스택
웹 UI	Streamlit, Matplotlib, WordCloud
자연어처리	KoNLPy (Okt), Transformers (KcELECTRA), TensorFlow (LSTM)
크롤링	Selenium, BeautifulSoup
모델 배포	Git LFS (또는 별도 모델 다운로드 경로 제공)
요약	OpenAI GPT API 활용 요약 기능

## 📈 결과 예시
감정 비율 파이차트

긍정/부정 리뷰 요약

감정별 워드클라우드

## 📚 참고 자료
HuggingFace KcELECTRA 모델: https://huggingface.co/beomi/KcELECTRA-base

OpenAI GPT-4 API: https://platform.openai.com/

Streamlit 배포 가이드: https://docs.streamlit.io/

## 🙋‍♀️ 만든 사람
박세연
한국폴리텍 성남캠퍼스
인공지능소프트웨어과 2학년
Backend & NLP Engineer
GitHub: tpdus751
