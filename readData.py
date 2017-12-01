import sys, os

from tockenizeData import TockenizeData

class ReadResponseData:
    @staticmethod
    def __init__(Context):
        ReadResponseData.responseDataFilePath = []
        for path, dirs, files in os.walk("Data/Dataset/"+Context):
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
            responseData[str(dir).lower()] = lines

        return responseData
    

class ReadRawData:
    
    @staticmethod
    def __init__(Context):
        ReadRawData.RawDataFilePath = []
        for path, dirs, files in os.walk("Data/Dataset/"+Context):
            for f in files:
                if "rawData.txt" in f:
                    ReadRawData.RawDataFilePath.append(path+"/"+f)

    @staticmethod
    def getData():
        RawData = {}
        for f in ReadRawData.RawDataFilePath:
            dir,_ = os.path.split(os.path.abspath(f))
            _,dir = os.path.split(dir)
            fileStream = open(f)
            fileEntry = fileStream.readlines()
            lines = []
            for line in fileEntry:
                lines.append(TockenizeData.getTockenizedDataWithStem(str(line).lower()))
            RawData[str(dir).lower()] = lines

        return RawData


if __name__ == '__main__':
    print ReadRawData("cmpe297").getData()