import streamlit as st
import os, zipfile, requests

# ✅ 반드시 가장 위에서 설정
st.set_page_config(page_title="내돈내픽 감성 분석", layout="wide")

import pandas as pd
import re
from ModelLoader import load_model
from SentimentPredictor import predict_sentiment
from ReviewSummary import summarize_reviews
from Visualization import plot_pie_chart, display_top_reviews
from TextProcessor import extract_keywords
from WordCloudVisualizer import plot_wordcloud
import gdown

def download_and_extract_model_from_gdrive(file_id, dest_path, extract_to):
    # GDrive URL 포맷 생성
    url = f"https://drive.google.com/uc?id={file_id}"

    zip_path = os.path.join(dest_path, "kc_electra_model.zip")
    gdown.download(url, zip_path, quiet=False)

    # 압축 해제
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    os.remove(zip_path)

# 🚨 처음 실행 시에만 다운로드 (재시작 대비)
# 압축 풀 경로 (바깥 폴더만 지정)
model_folder = "kc_electra_sentiment_model_0624_3"

# 모델 경로는 압축된 내부 중첩 폴더까지 포함해야 함
model_path = os.path.join(model_folder, "kc_electra_sentiment_model_0624_3")

# 모델 압축 다운로드 및 추출
if not os.path.exists(model_path):
    download_and_extract_model_from_gdrive("1-Ukah1Vovn4hteVBpXUm5ekU1TDP5Mxf", ".", model_folder)

# 모델 로더에 경로 전달
tokenizer, model = load_model(model_path)

# Load dataset
try:
    df = pd.read_csv("restaurant_reviews.csv")
except Exception as e:
    st.error("리뷰 데이터 파일을 불러오는 데 실패했습니다.")
    st.stop()
restaurant_names = sorted(df['name'].dropna().unique())

# 음식점 이름 입력 + 자동완성
with st.sidebar:
    st.header("🔍 성남시 음식점 검색")
    query = st.text_input("성남시 음식점 이름을 입력하세요")

    matched_names = [name for name in restaurant_names if query.lower() in name.lower()][:10]
    selected_name = st.selectbox("성남시 음식점 후보를 선택하세요", matched_names) if matched_names else None

    if selected_name and st.button("리뷰 분석 시작"):
        filtered_reviews = df[df['name'] == selected_name]['content'].dropna().astype(str).tolist()
        result_df = predict_sentiment(filtered_reviews, tokenizer, model)
        st.session_state['result_df'] = result_df
        st.session_state['analyzed'] = True
        st.session_state['restaurant_name'] = selected_name
        if 'gpt_summary' in st.session_state:
            del st.session_state['gpt_summary']  # 새 음식점 분석 시 GPT 요약 초기화

# 리뷰 감성 분석 결과 출력
if st.session_state.get('analyzed', False):
    st.header(f"📊 리뷰(네이버 지도) 감성 분석 결과 - {st.session_state['restaurant_name']}")
    result_df = st.session_state['result_df']
    st.dataframe(result_df, use_container_width=True)

    st.subheader("🎯 감성 비율 시각화")
    plot_pie_chart(result_df)
    
    st.subheader("🖼️ 감정별 워드클라우드")
    for label in ['긍정', '중립', '부정']:
        texts = result_df[result_df['label'] == label]['review'].tolist()
        if texts:
            counter = extract_keywords(texts)
            plot_wordcloud(counter, title=f"{label} 리뷰 워드클라우드")
        else:
            st.markdown(f"**{label} 리뷰가 부족하여 워드클라우드를 생성할 수 없습니다.**")

    st.subheader("🧠 GPT-4o 요약 결과")
    if 'gpt_summary' not in st.session_state:
        with st.spinner("GPT가 리뷰 요약 중입니다..."):
            pos_reviews = display_top_reviews(result_df, '긍정')
            neg_reviews = display_top_reviews(result_df, '부정')
            pos_summary = summarize_reviews(pos_reviews, "아래는 음식점에 대한 긍정적인 리뷰입니다. 장점을 요약해주세요.")
            neg_summary = summarize_reviews(neg_reviews, "아래는 음식점에 대한 부정적인 리뷰입니다. 개선점을 요약해주세요.")
            st.session_state['gpt_summary'] = {
                "pos": pos_summary,
                "neg": neg_summary
            }

    st.markdown("### 👍 장점 요약")
    st.info(st.session_state['gpt_summary']['pos'])

    st.markdown("### 👎 개선점 요약")
    st.warning(st.session_state['gpt_summary']['neg'])

# 개별 리뷰 감성 분석
st.markdown("---")
st.header("📝 개별 리뷰 감성 분석")
user_review = st.text_area("리뷰를 입력하세요", height=100)
if st.button("감성 분석 실행"):
    if not user_review.strip():
        st.warning("리뷰를 입력해주세요.")
    else:
        single_result = predict_sentiment([user_review], tokenizer, model)
        st.session_state['single_result'] = single_result

if 'single_result' in st.session_state:
    row = st.session_state['single_result'].iloc[0]
    st.success(f"분석 결과: **{row['label']}**  ({row['confidence'] * 100:.2f}%)")