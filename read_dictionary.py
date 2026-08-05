# main.py
# Reading from a text file in Python

with open("products", "r") as file:
    contents = file.read()

print(contents)
