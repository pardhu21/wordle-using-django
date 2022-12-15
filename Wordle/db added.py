from models import Word

with open('Wordle\sgb-words.txt', 'r') as f:
    words = f.readlines()

print(words[0])