# Name: Edmund Liu
# Date: Sept. 18, 2026


url = input("Enter a URL: ")

cleaned_url = url.replace("http://", "")
cleaned_url = cleaned_url.replace("/", "")
print("cleaned_URL:", cleaned_url)

parts = cleaned_url.split(".")
print("The parts are: ", parts)

domain_name = parts[1]
tld = parts[2]
print("Domain name:", domain_name)
print("TLD:", tld)
