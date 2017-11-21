from prepareTrainingData import TrainingData
from prepareResponse import ResponseData
from sklearn.model_selection import train_test_split

import tflearn
import tensorflow as tf

class Model:
    def __init__(self):
        self.X, self.Y = TrainingData().convertDataToIntegerArray()

    def createModel(self):        

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=42)

        
        net = tflearn.input_data(shape=[None, len(X_train[0])])
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, len(y_train[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        self.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

        ckpt = tf.train.get_checkpoint_state("Checkpoint")

        if ckpt and ckpt.model_checkpoint_path:
            self.model.load("Checkpoint/my_model")
        else:
            # Start training (apply gradient descent algorithm)
            #self.model.fit(X_train, y_train, validation_set=(X_test, y_test), n_epoch=500, batch_size=16, show_metric=True)
            self.model.fit(X_train, y_train, n_epoch=500, batch_size=16, show_metric=True)
            self.model.save("Checkpoint/my_model")

    def predictTarget(self, sentence):
        data = TrainingData().convertXToIntegerArray(sentence)
        r = self.model.predict([data])
        result = []
        for rr in r[0]:
            if rr > 0.7:
                result.append(1)
                continue
            elif rr < 0.3:
                result.append(0)
                continue
            else:
                result.append(-1)

        return result

        


if __name__ == '__main__':
    model = Model()
    model.createModel()
    var = raw_input(">>")
    result = model.predictTarget(var)
    target = TrainingData().returnTarget(result)
    print ResponseData().getResponseData(target)
