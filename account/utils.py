import requests

guruh = "-1001803432717"
abdusattor = "148603286"

def send_code(code):
    link = f"https://api.telegram.org/bot6225079799:AAEJUlRbi7xD-WbOu-SelhYRZGlWh1BZpNw/sendMessage?chat_id={abdusattor}&text=Verification code : {code}"
    response = requests.get(link)
    return code