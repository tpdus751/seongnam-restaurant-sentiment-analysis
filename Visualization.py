import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import rcParams
import platform

def set_korean_font():
    if platform.system() == 'Windows':
        rcParams['font.family'] = 'Malgun Gothic'  # 윈도우
    elif platform.system() == 'Darwin':
        rcParams['font.family'] = 'AppleGothic'  # 맥OS
    else:
        rcParams['font.family'] = 'NanumGothic'  # 리눅스 또는 기타 (사전설치 필요)

    rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

def plot_pie_chart(df):
    set_korean_font()  # 한글 폰트 설정
    
    label_counts = df['label'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(label_counts, labels=label_counts.index, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # 동그란 원 유지
    st.pyplot(fig)
    
def display_top_reviews(df, label, top_k=5):
    subset = df[df['label'] == label].nlargest(top_k, 'confidence')
    return subset['review'].tolist()
