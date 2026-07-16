from generate_data import  generate_orders
from agent import query_orders
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent

load_dotenv()

def main():
    print("Hello from fix-log-agent!")
    
    # df = generate_orders(300)
    # df.to_csv("data/orders.csv", index=False)
    # print(f"Generated {len(df)} orders -> data/orders.csv")
    # print((df["status"].value_counts(normalize=True)*100).round(2).map("{}%".format))

    llm = ChatOpenAI(
        # model="anthropic/claude-sonnet-4.5",
        temperature=0,
        api_key=os.getenv("OPENRouter_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )
    tools = [query_orders]
    agent = create_agent(llm,tools=tools)

    print("FIX Log Q&A Agent ready. Ask about the order log (type 'exit to quit). \n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue

        response = agent.invoke({"messages": [{"role": "user", "content": question}]})
        answer = response["messages"][-1].content
        print(f"\nAgent: {answer}\n")


if __name__ == "__main__":
    main()
