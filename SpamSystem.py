import ConfigLocal as cl
from Sms import Sms
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
DATA_URL = "data.spam"
from SpamBase import SpamBase
from sklearn import svm
import pickle

# Input url file spam training
INPUTSPAMURL = cl.INPUTSPAMURL
# Input url file not spam training
INPUTNSPAMURL = cl.INPUTNSPAMURL
# Output url file output data training
STOPWORDURL = cl.STOPWORDURL
SPAM_MODEL = cl.SPAM_MODEL

class SpamSystem(object):
    # center process training data
    smsLst = []
    def __init__(self):
        pass

    # This function using to prepare data before traning data
    # Output lstAllOfData: all of data in data file ham and spam
    # Label: label data
    # lstStopWord: list content data stop words
    def preDataFile(self):
        # Line in spam file
        lineSpams = SpamBase.readFile(self, INPUTSPAMURL)
        # Line in Ham file
        lineNSpams = SpamBase.readFile(self, INPUTNSPAMURL)
        # Line in stop words file
        lineStopWord = SpamBase.readFile(self, STOPWORDURL)
        lstAllOfData = lineSpams + lineNSpams
        label = []
        for i in range(len(lineSpams) + len(lineNSpams)):
            if i < len(lineSpams):
                label.append(1)
            else:
                label.append(0)
        lstStopWord = []
        for i in range(len(lineStopWord)):
            lstStopWord = lstStopWord + SpamBase.analyzePhrase(self, lineStopWord[i])
        return lstAllOfData, np.array(label), lstStopWord

    # This function using to predict data file label
    # Return none
    # Data output save in list words
    def predictSvmDataFile(self, inputUrl):
        # Encrypt data
        lines = SpamBase.readFile(self, inputUrl)
        for i in range(len(lines)):
            sms = Sms()
            smsLabel = self.checkSMSSpam(lines[i].strip())
            sms.smsText = lines[i]
            sms.proOfHam = "{:10.3f}".format(smsLabel[0][0] * 100)
            sms.proOfSpam = "{:10.3f}".format(smsLabel[0][1] * 100)
            sms.predict = self.decodeLabel(smsLabel)
            self.smsLst.append(sms.toDictionary())

    # This function using to predict sms data  label
    # Return none
    # Data output save in list words
    def predictSvmSmsData(self, smsInput):
        # Save data processed
        sms = Sms()
        smsLabel = self.checkSMSSpam(smsInput.strip())
        sms.smsText = smsInput
        sms.proOfHam = "{:10.3f}".format(smsLabel[0][0] * 100)
        sms.proOfSpam ="{:10.3f}".format(smsLabel[0][1] * 100)
        sms.predict = self.decodeLabel(smsLabel)
        self.smsLst.append(sms.toDictionary())

    # This function using to training data
    # Return none
    # Data output save in svm model
    def trainData(self):
        try:
            # Call method prepare data
            preData, label, lstStopWord = self.preDataFile()
            # Use TF-IDF lib to vector text data
            tfidfVector = TfidfVectorizer(lowercase=True, stop_words=lstStopWord)
            # TF-IDF train data
            X_train_TFIDF = tfidfVector.fit_transform(preData)
            # Create X data and Y label data
            x = np.array(X_train_TFIDF.toarray())
            y = label
            # Svm training data
            svc = svm.SVC(probability=True, kernel=cl.KERNEL_TYPE, C=cl.COST, gamma=cl.GAMMA).fit(x, y)
            # Pickle sve model file
            with open(SPAM_MODEL, 'wb') as f:
                pickle.dump(svc, f)
                pickle.dump(tfidfVector, f)
        except Exception as e:
            print('train Data: ', e)

    # This function using to check content spam
    # Return label data
    def checkSMSSpam(self, sms):
        # Read pickle file
        with open(SPAM_MODEL, 'rb') as f:
            clf = pickle.load(f)
            tfidfVector = pickle.load(f)
        # Convert sms to vector
        smsPredic = np.array(tfidfVector.transform([sms]).toarray())
        # Predict probability spam
        result = clf.predict_proba(smsPredic[0].reshape(1, -1))
        return result

    # This function using to translate label
    # Return label name
    def decodeLabel(self, label):
        if label[0][0] > label[0][1]:
            return cl.NSPAM
        else:
            return cl.SPAM

    def callSpamLearn(self, text):
        text = text.replace('\n', ' ')
        return SpamBase.addLearnSpam(self, text)

    def callHamLearn(self, text):
        text = text.replace('\n', ' ')
        return SpamBase.addLearnHam(self, text)

    def callTrainMessage(self, content):
        return SpamBase.trainMessage(self, content)

    def callStopWord(self):
        return SpamBase.readStopWord(self)

    def callAddStopWord(self, content):
        return SpamBase.addStopWord(self, content)

    def callRemoveStopWord(self, content):
        return SpamBase.removeStopWord(self, content)

    def cleanData(self):
        self.smsLst.clear()

# class Main():
#     def main(self):
#         obj = SpamSystem()
#         # sms = 'Hôm nay (11/9) khách VIP đã đến công ty chung ta, họ sẽ ở lại làm việc đến hết ngày 15/9.Admin xin phép remind mọi người 1 lần nữa về những điều đã lưu ý trong email tuần trước.Rất mong mọi người cùng cố gắng để tạo ấn tượng tốt với khách hàng nhé!'
#         # x = obj.callHamLearn(sms);
#         # print('X', x)
#         # obj.trainData()
#         print(obj.callStopWord())
#         # x = obj.checkSMSSpam('em về mua trước đi nhé, mai anh sẽ mua vietlott ')
#         # print('x', '%.2f' % x[0][0])
#         # sms = 'Sau tất cả, “đứa con tinh thần” của tháng 09/2017 đã chào đời dù có hơi muộn màng so với kế hoạch.'
#         # obj.encrypt_svm_sms_data(sms)
#         # #obj.encrypt_svm_file_data('test.txt')
#         # #obj.smsLst
#         # print( obj.smsLst)
#         # print('data',type(obj.smsLst))
# m = Main()
# m.main()
