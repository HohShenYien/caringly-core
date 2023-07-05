import os
from typing import List

import pandas as pd
from tensorflow.keras.models import load_model

from server.scan.utils import preprocess_text

# TODO: Enable this later
model_layer_1 = load_model("./server/scan/models/lstm-layer-1.mod")
model_layer_2 = load_model("./server/scan/models/best-layer-2-bilstm.mod")


def classify(row):
    if row.is_dangerous <= 0.5:
        return "neutral", (1 - row.is_dangerous[0])
    if row.is_suicide > 0.5:
        return "suicide", row.is_suicide[0]
    return "depression", 1 - row.is_suicide[0]


def predict(texts: "List[str]"):
    clean_texts = [preprocess_text(text) for text in texts]
    pred1 = model_layer_1.predict(clean_texts)
    pred2 = model_layer_2.predict(clean_texts)
    res = pd.DataFrame(
        list(zip(clean_texts, pred1, pred2)),
        columns=["content", "is_dangerous", "is_suicide"],
    )
    return res.apply(lambda x: classify(x), axis=1)
