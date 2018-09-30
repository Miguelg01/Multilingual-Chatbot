# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilioCredentials import Cred
from google.cloud import translate

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    # Start our response
    resp = MessagingResponse()
    credObj = Cred()
    
    account_sid = credObj.id
    auth_token = credObj.token
    
    client = Client(account_sid, auth_token)
    
    
    messages = client.messages.list()
    phrase = messages[0].body
    
    
    
    #translate section
    mapPhoneNumber = {"+user_1_number":"+user_2_number","+user_2_number":"+user_1_number"}
    fromPhone = messages[0].from_
    toPhone = mapPhoneNumber[fromPhone]
    
    translate_client = translate.Client()
    acceptedLang = set(['ja', 'fr', 'es', 'en', 'ru', 'yo'])
    
    if len(phrase) >= 2:
        text = phrase[2:]
        target = phrase[:2].lower()
    else:
        text = phrase
        target='en'
    
    if phrase.lower()=='options' or (target not in acceptedLang):
        error1 = 'please use one of the following tags: ja, fr, es, en, ru, yo'
        error2 = 'reply in the form: <language tag> <message>'
        #outPhrase = 'test'
        resp.message(error1)
        resp.message(error2)
    else:
        translation = translate_client.translate(text,target_language=target)
        
        outPhrase = translation['translatedText']
        
        #send another message
        message = client.messages.create(to=toPhone,from_="+twilio_phone_number", body=outPhrase)
        
        # Add a message
        resp.message(outPhrase)
            
            return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
