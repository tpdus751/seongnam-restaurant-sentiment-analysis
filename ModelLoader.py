from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import streamlit as st

@st.cache_resource
def load_model(model_path="./kc_electra_sentiment_model_0624_3"):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model
