from prepareRawData import RawData
from prepareResponse import ResponseData
from sklearn.model_selection import train_test_split
from readData import ReadContext

import tflearn
import tensorflow as tf

class ModelCollection:
    def __init__(self):
        self.ContextList = ReadContext().Context   
        self.model = {}
        for c in self.ContextList:
            self.model[c] = Model(c)
            self.model[c].createModel()

    def predictTarget(self, context, var):        
        
        if context not in self.ContextList:
            return "None"

        return self.model[context].predictTarget(var)
    

class Model:
    def __init__(self, Context):
        self.Context = Context
        self.X, self.Y = RawData(self.Context).convertDataToIntegerArray()
        print self.X
        print self.Y

    def createModel(self):        

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=42)
        tf.reset_default_graph()        
        net = tflearn.input_data(shape=[None, len(X_train[0])])
        net = tflearn.fully_connected(net, 64)
        net = tflearn.fully_connected(net, 64)
        net = tflearn.fully_connected(net, len(y_train[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        self.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

        ckpt = tf.train.get_checkpoint_state("Checkpoint/"+ self.Context)

        if ckpt and ckpt.model_checkpoint_path:
            self.model.load("Checkpoint/"+ self.Context + "/my_model")
        else:
            # Start training (apply gradient descent algorithm)
            #self.model.fit(X_train, y_train, validation_set=(X_test, y_test), n_epoch=500, batch_size=16, show_metric=True)
            self.model.fit(X_train, y_train, n_epoch=500, batch_size=16, show_metric=True)
            self.model.save("Checkpoint/" + self.Context + "/my_model")

    def predictTarget(self, sentence):
        sentence = sentence.replace("where","location")
        sentence = sentence.replace("when","time")
        data = RawData(self.Context).convertXToIntegerArray(sentence)
        r = self.model.predict([data])
        result = []
        for rr in r[0]:
            if rr > 0.5:
                result.append(1)
                continue
            elif rr < 0.5:
                result.append(0)
                continue
            else:
                result.append(-1)

        return result

        


if __name__ == '__main__':
    model = Model("cmpe297")
    model.createModel()

    while 1:
        var = raw_input(">>")
        result = model.predictTarget(var)
        print result        
        target = RawData("cmpe297").returnTarget(result)
        print target

        if "None" not in target:
            print ResponseData("cmpe297").getResponseData(target)
