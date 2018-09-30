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
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()
    credObj = Cred()
    
    account_sid = credObj.id
    auth_token = credObj.token
    
    client = Client(account_sid, auth_token)
    
    
    messages = client.messages.list()
    phrase = messages[0].body

    #translate section
    translate_client = translate.Client()
    acceptedLang = set(['ja', 'fr', 'es', 'en', 'ru', 'yo'])
    
    if len(phrase) >= 15:
        text = phrase[15:]
        toNumber = phrase[3:15]
        #toNumber=
        # The target language
        target = phrase[:2].lower()
    else:
        text = phrase
        toNumber = "+15555555555"
        target='en'

    if phrase.lower()=='options' or (target not in acceptedLang):
        outPhrase = 'please use one of the following tags: ja, fr, es, en, ru, yo'
        #outPhrase = 'test'
    else:
        translation = translate_client.translate(
                                                 text,
                                                 target_language=target)
                                                 
        outPhrase = translation['translatedText']

    #send another message
    message = client.messages.create(
                                     to=toNumber,
                                     from_="+15555555555",
                                     body=outPhrase)

    # Add a message
    resp.message(outPhrase)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
