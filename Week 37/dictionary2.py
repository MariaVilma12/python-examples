dictionary = {
    "hello": "world",
    "answer": 42,
    "number": [4, 8, 15, 16, 23, 42],
    7: 11,
    42: ["Please restate the question", "This is a number"]
}

for key in dictionary:
    print(f"{key} : {dictionary[key]}")
