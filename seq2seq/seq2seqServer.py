

import tensorflow as tf
import execute

class Seq2seqServer:
    @staticmethod
    def __init__():
        sess = tf.Session()
        sess, model, enc_vocab, rev_dec_vocab = execute.init_session(sess, conf='seq2seq_serve.ini')