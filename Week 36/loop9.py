running = True
while running:
    word = input("Please enter a word: ")
    print(word)
    restart = input("Enter 'x' to exit")
    if restart == 'x':
        running = False