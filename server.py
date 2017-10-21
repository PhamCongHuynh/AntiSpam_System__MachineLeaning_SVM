from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from SpamSystem import SpamSystem
from flask_cors import CORS, cross_origin
import ConfigLocal as cl
import os
app = Flask(__name__)
CORS(app)
api = Api(app)

class SpamSample(Resource):
    def post(self):
        proSms = SpamSystem()
        proSms.cleanData()
        proSms.predictSvmDataFile("test.txt")
        data = proSms.smsLst
        stopWords = proSms.callStopWord()
        result = {'records': data , 'stopword': stopWords}
        return jsonify(result)

class SpamSms(Resource):
    def post(self):
        if (request.json):
            proSms = SpamSystem()
            proSms.cleanData()
            proSms.predictSvmSmsData(request.json['sms'])
            data = proSms.smsLst
            result = {'records': data}
            return jsonify(result)

class SpamAdd(Resource):
    def post(self):
        if (request.json):
            text = request.json['sms']
            proSms = SpamSystem()
            flag = proSms.callSpamLearn(text)
            if(flag == cl.FILE_W_SUCESS):
                proSms.trainData()
            mess = proSms.callTrainMessage(flag)
            proSms.cleanData()
            proSms.predictSvmSmsData(text)
            data = proSms.smsLst
            result = {'records': data ,'message':mess}
            return jsonify(result)

class HamAdd(Resource):
    def post(self):
        if (request.json):
            text = request.json['sms']
            proSms = SpamSystem()
            flag = proSms.callHamLearn(text)
            if(flag == cl.FILE_W_SUCESS):
                proSms.trainData()
            mess = proSms.callTrainMessage(flag)
            proSms.cleanData()
            proSms.predictSvmSmsData(text)
            data = proSms.smsLst
            stopWords = proSms.callStopWord()
            result = {'records': data ,'message':mess}
            return jsonify(result)

class StopWord(Resource):
    def post(self):
        proSms = SpamSystem()
        data = proSms.smsLst
        stopWords = proSms.callStopWord()
        result = {'records': data ,'stopword': stopWords}
        return jsonify(result)

class AddStopWord(Resource):
    def post(self):
        if (request.json):
            text = request.json['sms']
            proSms = SpamSystem()
            data = proSms.smsLst
            flag = proSms.callAddStopWord(text)
            mess = proSms.callTrainMessage(flag)
            stopWords = proSms.callStopWord()
            result = {'records': data ,'stopword': stopWords,'swInfo': mess}
            return jsonify(result)

class removeStopWord(Resource):
    def post(self):
        if (request.json):
            text = request.json['sms']
            proSms = SpamSystem()
            data = proSms.smsLst
            flag = proSms.callRemoveStopWord(text)
            mess = proSms.callTrainMessage(flag)
            stopWords = proSms.callStopWord()
            result = {'records': data ,'stopword': stopWords,'swInfo': mess}
            return jsonify(result)
    def deleteSW(self):
        if (request.json):
            text = request.json['sms']
            proSms = SpamSystem()
            data = proSms.smsLst
            flag = proSms.callRemoveStopWord(text)
            mess = proSms.callTrainMessage(flag)
            stopWords = proSms.callStopWord()
            result = {'records': data ,'stopword': stopWords,'swInfo': mess}
            return jsonify(result)

@app.route('/index')
def index():
    return redirect(os.getcwd()+"\\templates\\index.html", code=200)

api.add_resource(SpamSample, '/')
api.add_resource(SpamSms, '/CheckSms')
api.add_resource(SpamAdd, '/AddSpamLearn')
api.add_resource(HamAdd, '/AddHamLearn')
api.add_resource(StopWord, '/StopWord')
api.add_resource(AddStopWord, '/AddStopWord')
api.add_resource(removeStopWord, '/RemoveStopWord')


if __name__ == '__main__':
    app.run(host=cl.HOST,port=cl.PORT)