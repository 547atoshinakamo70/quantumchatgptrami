def extract_features_from_block(block: dict) -> dict:
    # Minimal handcrafted features; replace with your schema
    txs = block.get("tx_count", 0)
    size = block.get("size", 0)
    fee = block.get("avg_fee", 0.0)
    return {"txs": txs, "size": size, "fee": fee}
