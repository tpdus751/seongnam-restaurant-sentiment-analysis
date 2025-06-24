# ModelLoader.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st

@st.cache_resource
def load_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model