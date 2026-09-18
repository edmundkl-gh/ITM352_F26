# Edmund Liu
# Sept. 16, 2026

email = input("Enter your email: ") 
username, domain = email.split("@") 
print("Username:", username) 
print("Domain:", domain) 

email = input("Enter your email: ")
at_position = email.index("@") 
username = email[:at_position] 
domain = email[at_position + 1:] 
print("Username:", username) 
print("Domain:", domain) 
