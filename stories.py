print ('#Extra addition: I added a new prompt asking for a place')
print ('Author : Julius Conteh')

print ('Purpose: Practice formatting strings to create a fun, personalized adventure story.')
print ("Please enter the following:\n")
print ("#Prompt for words and store them in variables")

adjective = input ("adjective: ")
animal = input ("animal: ")
verb1 = input ("verb: ")
exclamation = input ("exclamation: ")
verb2 = input ("verb: ")
verb3 = input ("verb: ")
place = input ("place: ") # <-- New addition

print ("#Display the story")
print ("\nMy story is:\n")
print (f"One morning, I woke up to the sound of a {adjective} {animal} trying to {verb1}.")
print(f"\"{exclamation.capitalize()}! \" I shouted, as I ran outside.")
print (f"I tried to {verb2}, but the {animal} was too quick.")
print (f"Suddenly, it began to {verb3} all over the {place}.")
print ("Everyone nearby stopped to watch, and we all agreed it was the funniest thing we had ever seen.")
