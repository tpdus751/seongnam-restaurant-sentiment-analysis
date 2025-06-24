from konlpy.tag import Okt
from collections import Counter
import re

okt = Okt()

# 불용어 예시
STOPWORDS = set([
    "것", "수", "이", "에", "가", "를", "은", "는", "좀", "정도", "그리고", "또한", "더", "한", "그", "의", "에서"
])

def clean_text(text):
    text = re.sub(r"[^가-힣a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_keywords(texts, pos_tags={"Noun", "Verb", "Adjective"}, stopwords=STOPWORDS):
    words = []
    for sentence in texts:
        sentence = clean_text(sentence)
        tokens = okt.pos(sentence, stem=True)  # 기본형으로 변환
        for word, tag in tokens:
            if tag in pos_tags and word not in stopwords and len(word) > 1:
                words.append(word)
    return Counter(words)
