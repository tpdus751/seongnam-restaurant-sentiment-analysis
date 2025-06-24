import openai
import os
import streamlit as st

if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_reviews(reviews, prompt_prefix, max_tokens=500):
    if not reviews:
        return "요약할 리뷰가 없습니다."

    joined = "\n- " + "\n- ".join(reviews[:10])
    system_msg = {
        "role": "system",
        "content": "너는 음식점 리뷰 분석 전문가야. 사용자 리뷰를 분석하여 장점/개선점을 요청에 따라 정중하게 요약해줘."
    }
    user_msg = {
        "role": "user",
        "content": f"{prompt_prefix} (리뷰 수: {len(reviews[:10])})\n{joined}\n\n요약:"
    }

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[system_msg, user_msg],
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.95,
            n=1
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ 요약 실패: {str(e)}"
