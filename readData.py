import sys, os

from tockenizeData import TockenizeData

class ReadResponseData:
    @staticmethod
    def __init__():
        ReadResponseData.responseDataFilePath = []
        for path, dirs, files in os.walk("Data"):
            for f in files:
                if "response.txt" in f:
                    ReadResponseData.responseDataFilePath.append(path+"/"+f)

    @staticmethod
    def getData():
        responseData = {}
        for f in ReadResponseData.responseDataFilePath:
            dir,_ = os.path.split(os.path.abspath(f))
            _,dir = os.path.split(dir)
            fileStream = open(f)
            fileEntry = fileStream.readlines()
            lines = []
            for line in fileEntry:
                lines.append(line)
            responseData[dir] = lines

        return responseData
    

class ReadTrainingData:
    
    @staticmethod
    def __init__():
        ReadTrainingData.trainingDataFilePath = []
        for path, dirs, files in os.walk("Data"):
            for f in files:
                if "trainingData.txt" in f:
                    ReadTrainingData.trainingDataFilePath.append(path+"/"+f)

    @staticmethod
    def getData():
        trainingData = {}
        for f in ReadTrainingData.trainingDataFilePath:
            dir,_ = os.path.split(os.path.abspath(f))
            _,dir = os.path.split(dir)
            fileStream = open(f)
            fileEntry = fileStream.readlines()
            lines = []
            for line in fileEntry:
                lines.append(TockenizeData.getTockenizedDataWithStem(line))
            trainingData[dir] = lines

        return trainingData


if __name__ == '__main__':
    print ReadTrainingData().getData()