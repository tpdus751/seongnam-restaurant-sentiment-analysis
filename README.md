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

📦seongnam-restaurant-sentiment-analysis
┣ 📂kc_electra_sentiment_model_0624_3
┃ ┣ config.json
┃ ┣ pytorch_model.bin
┃ ┣ tokenizer.json
┣ 📂.streamlit
┃ ┣ config.toml
┃ ┗ secrets.toml
┣ 📜App.py
┣ 📜ModelLoader.py
┣ 📜SentimentPredictor.py
┣ 📜Visualization.py
┣ 📜TextProcessor.py
┣ 📜ReviewSummary.py
┣ 📜restaurant_reviews.csv
┣ 📜requirements.txt
┣ 📜packages.txt
┗ 📜README.md

---

## 🧬 감성 분석 모델

| 모델 | 설명 |
|------|------|
| `LSTM` | 형태소 분석 후 시퀀스 입력, Keras 기반 감성 분류 |
| `KcELECTRA` | HuggingFace `beomi/KcELECTRA-base`, 한국어에 특화된 Transformer 모델 |

현재 앱에서는 정확도가 더 높은 **KcELECTRA 모델**을 사용 중입니다.

---

## 🌐 사용 방법

### 1. 로컬 실행

# 가상환경 설치 (권장)
conda create -n senti python=3.9
conda activate senti

# 라이브러리 설치
pip install -r requirements.txt
2. 실행
streamlit run App.py
앱이 자동으로 브라우저에서 실행됩니다 (localhost:8501).

📦 배포 환경 (Streamlit Cloud)
Java 기반 라이브러리(KoNLPy) 사용을 위해 packages.txt 필요:

default-jre
.streamlit/secrets.toml에는 OpenAI API 키를 포함해야 합니다:

OPENAI_API_KEY = "sk-..."
🧹 사용 기술
분야	기술 스택
웹 UI	Streamlit, Matplotlib, WordCloud
자연어처리	KoNLPy (Okt), Transformers (KcELECTRA), TensorFlow (LSTM)
크롤링	Selenium, BeautifulSoup
모델 배포	Git LFS 또는 모델 별도 다운로드
요약	OpenAI GPT API 기반 요약 기능

📈 결과 예시
(이미지 예시가 있다면 링크 삽입 또는 생략 가능)

🤖 시연 / 제출 자료
🟢 앱 배포 링크

📺 시연 영상 보기

📎 프로젝트 Tech Report 보기

📚 참고 자료
HuggingFace KcELECTRA 모델

OpenAI GPT-4 API

Streamlit 배포 가이드

🙋‍♀️ 만든 사람
박세연
한국폴리텍 성남캠퍼스
인공지능소프트웨어과 2학년
Backend & NLP Engineer
GitHub: tpdus751
