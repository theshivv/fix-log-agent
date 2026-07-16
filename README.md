# 📊 FIX Log Q&A Agent

> Ask plain-English questions about trading order flow. An LLM agent parses your intent, queries the order log, and answers — no SQL, no grepping FIX tags by hand.

---

## Why this exists

Reading FIX logs and order blotters usually means grepping raw tags or writing one-off pandas scripts every time you have a new question. This project wraps a synthetic order log in a small set of tools and hands them to an LLM agent, so questions like *"what's the average latency on filled orders?"* or *"why were orders rejected today?"* get answered conversationally — the agent decides which tool to call, runs it, and responds.

Built as a first step into agentic AI tooling for trading/order-flow use cases — the kind of "LLM sitting on top of financial infrastructure" pattern used in Forward Deployed Engineering and fintech AI roles.

---

## ✨ Features

- 🧠 **ReAct agent** (LangGraph) that reasons about which tool to call and when
- 📁 **Synthetic FIX-flavored order data** — 300 realistic orders with statuses, latencies, and reject reasons
- 🔧 **3 composable tools** — filter orders, compute stats, get status breakdowns
- 🔌 **Model-agnostic** — works with Anthropic's API directly or via OpenRouter (swap providers with zero changes to agent logic)
- 💬 **Simple CLI chat loop** — ask questions, get answers, no UI overhead

---

## 🗂 Project structure

```
fix-log-agent/
├── generate_data.py     # creates synthetic order log
├── agent.py             # the agent + tools + chat loop
├── data/
│   └── orders.csv        # generated order data
├── .env                  # API keys (not committed)
└── pyproject.toml         # managed by uv
```

---

## 🚀 Getting started

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/fix-log-agent.git
cd fix-log-agent
uv sync
```

### 2. Add your API key

```bash
echo "OPENROUTER_API_KEY=your-key-here" >> .env
```
*(or `ANTHROPIC_API_KEY` if calling Anthropic directly — see [Configuration](#-configuration))*

### 3. Generate the data

```bash
uv run generate_data.py
```

### 4. Run the agent

```bash
uv run agent.py
```

```
FIX Log Q&A Agent ready. Ask about the order log (type 'exit' to quit).

You: how many orders were rejected and why?
Agent: 24 orders were rejected (8% of total)...

You: what's the average latency for filled orders?
Agent: Average latency for filled orders is 42.3ms...
```

---

## 🛠 Configuration

The agent runs on any OpenAI-compatible or Anthropic-compatible endpoint.

| Provider | Setup |
|---|---|
| **Anthropic (direct)** | `uv add langchain-anthropic`, set `ANTHROPIC_API_KEY` |
| **OpenRouter** | `uv add langchain-openai`, set `OPENROUTER_API_KEY`, point `base_url` to `https://openrouter.ai/api/v1` |

Model swaps are one line — no changes to tools or agent wiring required.

---

## 🧪 Example questions to try

- `show me AAPL sell orders`
- `what's the reject rate today?`
- `is there a latency outlier I should know about?`
- `compare average fill latency vs partial fills`

---

## 🗺 Roadmap

- [ ] Real FIX tag parsing (35=D, 35=8, etc.) instead of synthetic CSV
- [ ] Second agent for anomaly detection (multi-agent graph)
- [ ] Streamlit front end for demo-ability
- [ ] EOD auto-generated summary report agent

---

## 🧩 Tech stack

`Python` · `LangGraph` · `LangChain` · `pandas` · `uv`

---

## 📄 License

MIT — do whatever you want with it.