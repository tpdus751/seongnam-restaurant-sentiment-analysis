import torch
import torch.nn.functional as F
import pandas as pd

def predict_sentiment(texts, tokenizer, model):
    # ✅ 모든 입력을 문자열로 강제 변환
    texts = [str(t) for t in texts]

    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    inputs = {k: v.to("cpu") for k, v in inputs.items()}
    model = model.to("cpu")
    model.eval()

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        confidences, labels = torch.max(probs, dim=1)

    id2label = {0: '부정', 1: '중립', 2: '긍정'}
    results = [
        {"review": t, "label": id2label[l.item()], "confidence": c.item()}
        for t, l, c in zip(texts, labels, confidences)
    ]
    return pd.DataFrame(results)
