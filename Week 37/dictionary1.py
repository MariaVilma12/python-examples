groceries = {
    "eggs":
        {
            "quantity": 12,
            "note": "free range"
        },
    "bread": {
        "quantity": "1 loaf",
        "note": "seed or whole grain"
    },
    "milk": {
        "quantity": "1 litre",
        "note": "whole milk"
    }
}

for item in groceries:
    print(f" - {item} - ")
    print(f"\tQuantity: {groceries[item]["quantity"]}")
    print(f"\t{groceries[item]["note"]}\n")