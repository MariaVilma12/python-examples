common = ["a","b","c"]
word = ("elephant")
charset = set(word)
print(charset)


for letter in set("telephone"):
    if letter in set("elephant"):
        print("Charset contains",letter)
        common.append(letter)

common = set(common)
print(common)

