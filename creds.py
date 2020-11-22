with open('creds.txt', 'r') as creds:
    creds = creds.read().split()
    email = creds[0]
    pas = creds[1]
    discord_url = creds[2]


def get_email():
    return email

def get_password():
    return pas

def get_discord_url():
    return discord_url