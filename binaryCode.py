import random
def decode(key, filename):
    f = open(filename, "rb")
    word = key
    word = [char for char in word]
    characters = []
    byte = f.read(1)
    while byte:
        characters.append(word[int.from_bytes(byte, "big")])
        byte = f.read(1)
    f.close()
    return "".join(characters).replace("⻲", "\n").replace("⻕", "\"")
def encode(text, key, use_file="none"):
    if use_file != "none":
        insert = open(use_file, "r")
        text = insert.read()
        insert.close()
    key = [char for char in key]
    text = [char for char in text]
    numbers = []
    for i in text:
        if i in key:
            numbers.append(key.index(i))
        elif i == "\n":
            numbers.append(key.index("⻲"))
        elif i == "\"":
            numbers.append(key.index("⻕"))
        else:
            print("Unknown character.")
            break
    return bytes(numbers)
def generateKey(log):
    needed = [char for char in "`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:|ZXCVBNM<>? ⻲⻕"]
    key = "".join(random.sample(needed, len(needed)))
    if log:
        print(key)
    return key