from keras.models import load_model
import visualkeras
import os
import tensorflow as tf
import base64
from io import BytesIO
import pandas as pd

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# origins = ["*"]


def Model_info(path):
    model = load_model(path)
    img = visualkeras.layered_view(model, legend=True, spacing=30)  # selected font
    buffer = BytesIO()
    img = img.convert("RGB")
    img.save(buffer, "JPEG")
    payload = base64.b64encode(buffer.getvalue())
    table = pd.DataFrame(columns=["Type", "Shape", "Param"])
    for layer in model.layers:
        table = table.append(
            {
                "Type": layer.__class__.__name__,
                "Shape": layer.output_shape,
                "Param": layer.count_params(),
            },
            ignore_index=True,
        )
    table = table.to_dict(orient="records")
    return payload, table, model.count_params()
