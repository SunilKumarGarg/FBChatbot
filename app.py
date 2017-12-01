from flask import Flask, render_template, request
from flask import jsonify, request
import json, requests
import pickle
from json import dumps
import spellCheck
import dateutil.parser

app = Flask(__name__)

PAT = "EAACyecYYj3EBANIADdMnUIrgz0ZBrdoORl1yr028DrRN0eDUmiRGtwsGOXAwEFRkmRdQ0uakb0qzoyh8sjoJEorGZBUb92bgaSQody6NGwGlrMSBxZBzokrVC7ZAZCPhEM3Mfssb6ck7Gs04wlmKlgcAidgPZC96GTfb4lL44zLgZDZD"
VERIFICATION_TOKEN = 'ThisIsMe'
fileBackup = "Chatbackup"

@app.route('/', methods=['GET'])
def handle_verification():
    print "Handling Verification."
    if request.args.get('hub.verify_token', '') == VERIFICATION_TOKEN:
        print "Webhook verified!"
        return request.args.get('hub.challenge', '')
    else:
        return "Wrong verification token!"


@app.route('/', methods=['POST'])
def reply():
    payload = request.get_data()

    #To do       

    for sender_id, message in messaging_events(payload):
        try:
            if message['type'] == 'text':
                sentence = str(message["data"]).lower()
                # try:
                #     date, data = dateutil.parser.parse(sentence, fuzzy_with_tokens=True)
                #     sent = []
                #     sent.append(str(date))
                #     for w in list(data):
                #         sent.append(w)
                #     sentence = " ".join(sent)
                # except:
                #     print "exception"

                # words = sentence.split(" ")
                # correctWords = []
                # for w in words:
                #     correctWords.append(spellCheck.correction(w))

                # sentence = " ".join(correctWords)
                context = loadChatHistory(str(sender_id))                
                c = getContext(sentence)
                print sentence
                if sentence != str(message["data"]).lower():
                    send_message(PAT, sender_id, "User Input:" + sentence)
                    

                if c != "None":
                    context = c

                result = model.predictTarget(context,sentence)
                target = RawData(context).returnTarget(result)

                if target == "None":
                    words = sentence.split(" ")

                    correctWords = []
                    for w in words:
                        correctWords.append(spellCheck.correction(w))

                    sentence = " ".join(correctWords)
                    print sentence
                    if sentence != str(message["data"]).lower():
                        send_message(PAT, sender_id, "User Input:" + sentence)
                    result = model.predictTarget(context,sentence)
                    target = RawData(context).returnTarget(result)

                    if target == "None":
                        text = execute.decode_line(sess, model_SeqToSeq, enc_vocab, rev_dec_vocab, sentence)
                    else:
                        text = ResponseData(context).getResponseData(target)
                else:
                    text = ResponseData(context).getResponseData(target)

                saveChatHistory(context, str(sender_id))
                send_message(PAT, sender_id, text)
        except:
            print "No Message"
            
    return "ok"

def getContext(var):
    contextList = ["cmpe297", "cmpe257"]
    for c in contextList:
        if c in var:
            return c
    return "None"

def saveChatHistory(object, sender_id):
    filehandler = open(fileBackup+ "/" +sender_id, 'w') 
    pickle.dump(object, filehandler)

def loadChatHistory(sender_id):
    try:
        filehandler = open(fileBackup+ "/" +sender_id, 'r') 
    except:
        print "Fail"
        return "cmpe297"
    object = pickle.load(filehandler)
    return object

def send_message(token, user_id, text):
    """Send the message text to recipient with id recipient.
    """
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {"text": text.decode('unicode_escape')}
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text

# Generate tuples of (sender_id, message_text) from the provided payload.
# This part technically clean up received data to pass only meaningful data to processIncoming() function
def messaging_events(payload):
    
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    
    for event in messaging_events:
        sender_id = event["sender"]["id"]

        # Not a message
        if "message" not in event:
            yield sender_id, None

        # Pure text message
        if "message" in event and "text" in event["message"] and "quick_reply" not in event["message"]:
            data = event["message"]["text"].encode('unicode_escape')
            yield sender_id, {'type':'text', 'data': data, 'message_id': event['message']['mid']}

        # Message with attachment (location, audio, photo, file, etc)
        elif "attachments" in event["message"]:

            # Location 
            if "location" == event['message']['attachments'][0]["type"]:
                coordinates = event['message']['attachments'][
                    0]['payload']['coordinates']
                latitude = coordinates['lat']
                longitude = coordinates['long']

                yield sender_id, {'type':'location','data':[latitude, longitude],'message_id': event['message']['mid']}

            # Audio
            elif "audio" == event['message']['attachments'][0]["type"]:
                audio_url = event['message'][
                    'attachments'][0]['payload']['url']
                yield sender_id, {'type':'audio','data': audio_url, 'message_id': event['message']['mid']}
            
            else:
                yield sender_id, {'type':'text','data':"I don't understand this", 'message_id': event['message']['mid']}
        
        # Quick reply message type
        elif "quick_reply" in event["message"]:
            data = event["message"]["quick_reply"]["payload"]
            yield sender_id, {'type':'quick_reply','data': data, 'message_id': event['message']['mid']}
        
        else:
            yield sender_id, {'type':'text','data':"I don't understand this", 'message_id': event['message']['mid']}
    

import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append("seq2seq")
import tensorflow as tf
import execute

sess = tf.Session()
sess, model_SeqToSeq, enc_vocab, rev_dec_vocab = execute.init_session(sess, conf='seq2seq/seq2seq_serve.ini')

from model import ModelCollection
from prepareRawData import RawData
from prepareResponse import ResponseData

model = ModelCollection()


if (__name__ == "__main__"):
    app.run(port = 5000)
