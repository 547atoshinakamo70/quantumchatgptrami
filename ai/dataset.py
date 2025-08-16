import random
def stream_blocks():
    # TODO: replace with real stream from your chain API
    for i in range(1000):
        yield {"tx_count": random.randint(1,2000), "size": random.randint(100,2000000), "avg_fee": random.random()*0.005}
