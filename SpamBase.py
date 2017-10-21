import ConfigLocal as cl
import re
import os

FILE_W_SUCESS = cl.FILE_W_SUCESS
FILE_W_ERROR = cl.FILE_W_ERROR
FILE_W_EXISTS = cl.FILE_W_EXISTS
WF_CONTENT_EMPTY = cl.WF_CONTENT_EMPTY
MESS_W_SUCCESS = cl.MESS_W_SUCCESS
MESS_W_ERROR = cl.MESS_W_ERROR
MESS_W_EXISTS = cl.MESS_W_EXISTS
MESS_C_EMPTY = cl.MESS_C_EMPTY
MESS_UNDEFINED = cl.MESS_UNDEFINED
TYPE_WRITE = 'w'
TYPE_APPEND = 'a'
STOPWORDURL = cl.STOPWORDURL


class SpamBase(object):
    # This function using to analyze words data
    def analyzePhrase(self, phrase):
        # TODO: IMPLEMENT this function to analyze intelligently
        # THIS IS VERY IMPORTANT FUNCTION for naive bayes to classify accurately
        if (not phrase):
            return None
        result = []
        strings = re.split("[\\,\\.\\s\\-\\=\\+\\!\\?\\&\\:\\;\\'\\\"\\(\\)\\[\\]\\{\\}\\<\\>\\|\\”\\“\\/\\\]+",
                           phrase.strip().lower())
        for word in strings:
            if (word):
                result.append(word)
        return result

    # This function using to learn Spam data
    def addLearnSpam(self, text):
        dirSpam = cl.INPUTSPAMURL
        dirHam = cl.INPUTNSPAMURL
        if text:
            if SpamBase.ckExistsInFile(self, text, dirSpam) and SpamBase.ckExistsInFile(self, text, dirHam):
                return SpamBase.writeFile(self, text, dirSpam, TYPE_APPEND)
            else:
                return FILE_W_EXISTS
        else:
            return WF_CONTENT_EMPTY

    # This function using to learn Ham data
    def addLearnHam(self, text):
        dirSpam = cl.INPUTSPAMURL
        dirHam = cl.INPUTNSPAMURL
        if text:
            if SpamBase.ckExistsInFile(self, text, dirSpam) and SpamBase.ckExistsInFile(self, text, dirHam):
                return SpamBase.writeFile(self, text, dirHam, TYPE_APPEND)
            else:
                return FILE_W_EXISTS
        else:
            return WF_CONTENT_EMPTY

    # This function using to add new stop word data
    def addStopWord(self, text):
        if text:
            lstW = SpamBase.analyzePhrase(self, text)
            lstOld = SpamBase.readFile(self, STOPWORDURL)
            for i in range(len(lstW)):
                if not lstOld.__contains__(lstW[i]):
                    SpamBase.writeFile(self, lstW[i], STOPWORDURL, TYPE_APPEND)
            return FILE_W_SUCESS
        else:
            return WF_CONTENT_EMPTY

    # This function do check is exists data in data file
    def ckExistsInFile(self, text, nameFile):
        contentLst = SpamBase.readFile(self, nameFile)
        if contentLst.__contains__(text):
            return False
        else:
            return True

    # This function using to read file stop words
    def readStopWord(self):
        lsWords = SpamBase.readFile(self, STOPWORDURL)
        stopWord = ''
        for i in range(len(lsWords)):
            if i == len(lsWords or i == 0):
                stopWord = stopWord + lsWords[i]
            else:
                stopWord = stopWord + ' ' + lsWords[i]
        return stopWord

    # This function using to remove word in file stop words
    def removeStopWord(self, content):
        if content:
            lsContent = SpamBase.analyzePhrase(self, content)
            lsWords = SpamBase.readFile(self, STOPWORDURL)
            for i in range(len(lsContent)):
                if lsWords.__contains__(lsContent[i]):
                    lsWords.remove(lsContent[i])
            if (SpamBase.clearnFile(self, STOPWORDURL, TYPE_WRITE)):
                for j in range(len(lsWords)):
                    SpamBase.writeFile(self, lsWords[j], STOPWORDURL, TYPE_APPEND)
                return FILE_W_SUCESS
            else:
                return FILE_W_ERROR
        else:
            return WF_CONTENT_EMPTY

    # This function using to read file data
    def readFile(self, nameFile):
        try:
            fileRead = open(nameFile, "r", encoding='utf-8')
            lines = fileRead.read()
            fileRead.close()
            lstTraining = re.split('\\n', lines.strip())
            return lstTraining
        except Exception as e:
            print('Has something wrong with training data file')
            raise

    # This function using to write file data
    def writeFile(self, text, dirFile, type):
        try:
            f = open(dirFile, type, encoding='utf-8')
            if os.path.getsize(dirFile) > 0:
                f.write('\n' + text)
            else:
                f.write(text)
            f.close()
            return FILE_W_SUCESS
        except Exception as e:
            print('Has something wrong with training data file', e)
            return FILE_W_ERROR

    # This function using to clean file data
    def clearnFile(self, dirFile, type):
        try:
            f = open(dirFile, type).close()
            return True
        except Exception as e:
            return False

    # This function using to translate message file data
    def trainMessage(self, content):
        if content == FILE_W_SUCESS:
            return MESS_W_SUCCESS
        elif content == FILE_W_ERROR:
            return MESS_W_ERROR
        elif content == FILE_W_EXISTS:
            return MESS_W_EXISTS
        elif content == WF_CONTENT_EMPTY:
            return MESS_C_EMPTY
        else:
            return MESS_UNDEFINED
