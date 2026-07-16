import pandas as pd
import random
from datetime import datetime, timedelta

# seed ~ page number for tracebility
random.seed(42)

SYMBOLS = ["APPL", "MSFT", "GOOGL", "TSLA", "NVDA", "JPM", "CITI", "GS"]
SIDES = ["BUY", "SELL"]
QUANTITIES = [100,200,500,1000,2500]
STATUSES = ["FILLED", "PARTIALLY_FILLED", "REJECTED", "CANCELLED","NEW"]
# weight status distribution so it feels realistic
STATUS_WEIGHTS = [0.55,0.15,0.08,0.12,0.10]

REJECT_REASONS = ["INSUFFICIENT_LIQUIDITY", "PRICE_OUT_OF_RANGE","RISK_LIMIT_BREACH","INVALID_SYMBOL"]

def generate_orders(n=300):
    rows=[]
    start_time = datetime(2026,7,16,9,30,0) # market_open

    for i in range(n):
        # :05d forces number to be 5 digit long
        order_id = f"ORD{i+1:05d}"
        symbol = random.choice(SYMBOLS)
        side = random.choice(SIDES)
        qty = random.choice(QUANTITIES)
        price = round(random.uniform(50,800),2)
        # it is list with single item in it
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]

        # timestamp drifts forward through the trading day
        timestamp = start_time + timedelta(seconds=i * random.randint(5,45))

        # latency : rejects are usually fast, fills vary more, occasional outlines
        if status == "REJECTED":
            latency_ms = random.randint(1,15)
        else:
            latency_ms = random.randint(5,120)
            if random.random() < 0.03:  # ~3% latency spikes
                latency_ms += random.randint(500,2000)

        reject_reason = random.choice(REJECT_REASONS) if status == "REJECTED" else ""

        rows.append({
            "order_id" : order_id,
            "symbol" : symbol,
            "side" : side,
            "qty" : qty,
            "price" : price,
            "status" : status,
            "reject_reason": reject_reason,
            "latency_ms": latency_ms,
            "timestamp" : timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

    return pd.DataFrame(rows)

