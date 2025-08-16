import os
USE_TF = os.environ.get("ENABLE_TF","0") == "1"

def train_model():
    # Optional: only runs if TensorFlow is enabled/installed
    if not USE_TF:
        return {"ok": False, "msg": "TensorFlow disabled (set ENABLE_TF=1)"} 
    try:
        import tensorflow as tf
    except Exception as e:
        return {"ok": False, "msg": f"TensorFlow not available: {e}"}
    from .dataset import stream_blocks
    from .features import extract_features_from_block
    xs, ys = [], []
    for block in stream_blocks():
        f = extract_features_from_block(block)
        xs.append([f["txs"], f["size"], f["fee"]]); ys.append(f["fee"])
    import numpy as np
    X = np.array(xs, dtype="float32"); y = np.array(ys, dtype="float32")
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(3,)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=2, verbose=0)
    path = os.environ.get("MODEL_PATH","model.keras")
    model.save(path)
    return {"ok": True, "path": path}
