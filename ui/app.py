from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__,static_url_path="/static")

@app.route('/message', methods=['POST'])
def reply():
    result = model.predictTarget(request.form['msg'])
    target = TrainingData().returnTarget(result)

    if target == "None":
        text = execute.decode_line(sess, model_SeqToSeq, enc_vocab, rev_dec_vocab, request.form['msg'])
    else:
        text = ResponseData().getResponseData(target)

    return jsonify( { 'text': text } )

@app.route("/")
def index():
    return render_template("index.html")

import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append("seq2seq")
import tensorflow as tf
import execute

sess = tf.Session()
sess, model_SeqToSeq, enc_vocab, rev_dec_vocab = execute.init_session(sess, conf='seq2seq/seq2seq_serve.ini')

from model import Model
from prepareTrainingData import TrainingData
from prepareResponse import ResponseData

model = Model()
model.createModel()


if (__name__ == "__main__"):
    app.run(port = 5000)
