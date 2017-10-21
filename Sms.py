class Sms(object):
    smsText = ''
    predict = ''
    proOfSpam = 0.01
    proOfHam = 0.01

    def __init__(self):
        pass

    def getSmsText(self):
        return self.smsText

    def getLabel(self):
        return self.label

    def getPredict(self):
        return self.predict

    # This function using to return Json object data
    def toDictionary(self):
        dic = {}
        dic['SpamText'] = self.smsText
        dic['Predic'] = self.predict
        dic['ProOfSpam'] = self.proOfSpam
        dic['ProOfHam'] = self.proOfHam
        return dic
