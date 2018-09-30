# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilioCredentials import Cred
from google.cloud import translate
from collections import defaultdict

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_translated_reply():
    # Start our response
    resp = MessagingResponse()
    
    #get twillio api credentials from ignored file
    credObj = Cred()
    account_sid = credObj.id
    auth_token = credObj.token
    client = Client(account_sid, auth_token)
    
    #grab body of most recent message
    messages = client.messages.list()
    phrase = messages[0].body
    
    #determine who to message based on sender
    mapPhoneNumber = defaultdict(lambda:credObj.user_1_number)
    mapPhoneNumber[credObj.user_1_number]=credObj.user_2_number
    
    fromPhone = messages[0].from_
    toPhone = mapPhoneNumber[fromPhone]
    
    #error checking for message length, assign output language
    if len(phrase) >= 2:
        text = phrase[2:]
        target = phrase[:2].lower()
    else:
        text = phrase
        target='en'
    
    #error checking for language tags
    acceptedLang = set(['ja', 'fr', 'es', 'en', 'ru', 'yo'])
    if phrase.lower()=='options' or (target not in acceptedLang):
        #respond excusively to sender with error info
        resp.message('reply in the form: <language tag> <message>')
        resp.message('accepted language tags: en, es, fr, ja, ru, yo')
    else:
        #translate text (in language auto-detected) to out language
        translate_client = translate.Client()
        translation = translate_client.translate(text,target_language=target)
        outPhrase = translation['translatedText']
        
        #send translated message to recipient
        message = client.messages.create(to=toPhone,from_=credObj.twilio_number, body=outPhrase)
        
        #send translated message back to sender as confirmation
        resp.message(outPhrase)
    
            return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
