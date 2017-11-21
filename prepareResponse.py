from readData import ReadResponseData

import random

class ResponseData:
    @staticmethod
    def __init__():
        ResponseData.data = ReadResponseData().getData()
        
    @staticmethod
    def getResponseData(target):
        
        length = len(ResponseData.data[target])
        if length == 0:
            return "sorry I do not speak"

        ran = random.randint(0,length-1)
        return ResponseData.data[target][ran]