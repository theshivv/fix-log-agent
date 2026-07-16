from generate_data import  generate_orders


def main():
    print("Hello from fix-log-agent!")
    
    df = generate_orders(300)
    df.to_csv("data/orders.csv", index=False)
    print(f"Generated {len(df)} orders -> data/orders.csv")
    print((df["status"].value_counts(normalize=True)*100).round(2).map("{}%".format))


if __name__ == "__main__":
    main()
