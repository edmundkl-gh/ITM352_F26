# Edmund Liu
# Sept. 18, 2026

email_address = input("Enter your email: ")
username, domain = email_address.split("@") 
print("Username:", username) 
print("Domain:", domain) 


email_address = input("Enter your email: ")
at_sign_index = email_address.index("@") 
username2 = email_address[:at_sign_index] 
domain2 = email_address[at_sign_index + 1:] 
print("Username:", username2) 
print("Domain:", domain2) 
