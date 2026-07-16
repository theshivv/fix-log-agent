import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()
df = pd.read_csv("data/orders.csv")


@tool
def query_orders(status: str ="", symbol: str ="", side:  str="") -> str:
    """Filter orders by status (FILLED/PARTIALLY_FILLED/REJECTED/CANCELLED/NEW),
    symbol (e.g. AAPL), and/or side (BUY/SELL). Leave a field empty string to skip that filter.
    Returns matching rows as text (capped at 20 rows)."""

    result = df.copy()
    if status:
        result = result[result["status"] == status.upper()]
    if symbol:
        result = result[result["symbol"] == symbol.upper()]
    if side:
        result = result[result["side"] == side.upper()]

    if result.empty:
        return "No matching orders found."
    
    return f"{len(result)} matching orders. Showing up to 20:\n" + result.head(20).to_string(index=False)


@tool
def compute_stat(column: str, operation: str, status_filter : str="") -> str:
    """Compute a statistic on a numeric column ('latency_ms, 'qty', or 'price').
    operation is one of: mean, min, sum, count.
    Optioanlly filter by status first (e.g. 'FILLED')    
    """

    data = df.copy()
    if status_filter:
        data = data[data["status"] == status_filter.upper()]

    if column not in ["latency_ms", "qty", "price"]:
        return f"Invalid column '{column}'. Use in latency_ms, qty or price."
    
    series = data[column]

    ops = {
        "mean" : series.mean,
        "max" : series.max,
        "min" : series.min,
        "sum" : series.sum,
        "count" : series.count
    }

    if operation not in ops:
        return f"Invalid operation '{operation}'. Use mean, max, min, sum or count."
    
    return f"{operation}({column}){' where status=' + status_filter if status_filter else ''} = {ops[operation]():.2f}"

