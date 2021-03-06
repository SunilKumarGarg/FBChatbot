from readData import ReadRawData
import numpy as np
import random
from tockenizeData import TockenizeData

class RawData():
    
    def __init__(self,Context):
        self.Context = Context
        self.bagOfWord = self.bagOfWords()

    def returnTarget(self, array):
        if np.sum(array) > 1:
            return "None"

        i = 0
        for a in array:
            if a == 1:
                return self.target[i]
                break;
            i += 1

        return "None"   

        

    def bagOfWords(self):
        self.dataTraining = ReadRawData(self.Context).getData()

        

        self.target = []
        data = []

        for key in self.dataTraining.iterkeys():
            data.append(self.dataTraining[key])
            self.target.append(key)

        flatList = []
        for d1 in data:
            for d2 in d1:
                for d in d2:
                    flatList.append(d)

        freqCounter = {}

        for d in flatList:
            if d in freqCounter.iterkeys():
                freqCounter[d] += 1
            else:
                freqCounter[d] = 1

        return sorted(freqCounter, key=freqCounter.get, reverse=True)

    def convertXToIntegerArray(self, sentence):
        X = TockenizeData.getTockenizedDataWithStem(sentence)
        xData = np.zeros(shape=(len(self.bagOfWord)), dtype=int)
        for x1 in X:
            if x1 in self.bagOfWord:
                xData[self.bagOfWord.index(x1)] = 1

        return xData


    def convertDataToIntegerArray(self):
        
        RawData = []
        
        for key in self.dataTraining.iterkeys():
            for itemList in self.dataTraining[key]:
                RawData.append((itemList,key))

        i = 0
        for X, Y in RawData:
            xData = np.zeros(shape=(len(self.bagOfWord)), dtype=int)
            yData = np.zeros(shape=(len(self.target)), dtype=int)
            yData[self.target.index(Y)] = 1
            xt = []
            for x1 in X:
                xData[self.bagOfWord.index(x1)] = 1

            RawData[i] = (list(xData),list(yData))
            i += 1

        random.shuffle(RawData)
        features = np.array(RawData)

        # create train and test lists
        train_x = list(features[:,0])
        train_y = list(features[:,1])

        return train_x, train_y
            
            

if __name__ == '__main__':
    print RawData("cmpe297").convertDataToIntegerArray()