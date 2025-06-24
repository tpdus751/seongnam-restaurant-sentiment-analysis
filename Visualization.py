import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.font_manager import FontProperties
import os

def plot_pie_chart(df):
    # ✅ 레포 내 malgun.ttf 경로 (예: 현재 디렉토리 기준)
    font_path = os.path.join(os.path.dirname(__file__), 'malgun.ttf')
    font_prop = FontProperties(fname=font_path)

    label_counts = df['label'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(
        label_counts,
        labels=label_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontproperties': font_prop}
    )
    ax.axis('equal')
    st.pyplot(fig)

    
def display_top_reviews(df, label, top_k=5):
    subset = df[df['label'] == label].nlargest(top_k, 'confidence')
    return subset['review'].tolist()
