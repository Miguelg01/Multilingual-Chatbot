# Multilingual-Chatbot
A chat bot that does language translation between users

## How to Use
1. Fill out credentials and phone numbers in 'twilioCredentials'
2. Either user sends a text to the registered twilio number in the form: (language code) (message)
3. The sender receives the translated message or error code as confirmation
4. The other user receives only the translated message if there are no errors

## Supported Languages
Note: Input language is auto-detected, but output language is restricted to the following <br>
Though not included, the translation api supports [these languages](https://cloud.google.com/translate/docs/languages)
* (en) English 
* (es) Spanish 
* (fr) French 
* (ja) Japanese
* (ru) Russian
* (yo) Yoruba

## Help Codes (not case sensitive)
* option
* options
* ?

## Tools Used
* Python
* Flask
* Twilio API
* (Google) Cloud Translation API
* ngrok

## Resources
* [Twilio API Documentation](https://www.twilio.com/docs/sms/quickstart/python)
* [Cloud Translation API Documentation](https://cloud.google.com/translate/docs/reference/libraries)
