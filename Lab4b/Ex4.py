# Edmund Liu
# Sept. 16, 2026
# Ask the user for a sentence
# Turn the sentence into a list of strings using split()
# Reverse the list
# Join the list back into a string using join()

sentence = input("Enter a sentence: ") 
words = sentence.split() 
words.reverse() 
reversed_sentence = " ".join(words) 
print(reversed_sentence) 
