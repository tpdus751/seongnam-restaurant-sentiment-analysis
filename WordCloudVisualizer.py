import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

def plot_wordcloud(counter, title="워드클라우드"):
    if not counter:
        st.write("❌ 단어가 충분하지 않아 워드클라우드를 생성할 수 없습니다.")
        return

    wc = WordCloud(
        font_path="malgun.ttf",  # ✅ 윈도우 한글 폰트 경로 (필요시 변경)
        background_color="white",
        width=800,
        height=400
    ).generate_from_frequencies(counter)

    st.subheader(title)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
