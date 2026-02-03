word = "Hello, my name is Maria"
flip = True
for i in range(len(word)):
    temp = word[i]
    if(flip):
        temp = temp.lower()
    else:
        temp = temp.upper()
    print(temp,end="")
    flip = not flip