 var app = angular.module('myApp', []);
 app.controller('spamCtrl', function($scope, $http)
    {
      server = 'http://127.0.0.1:5003';
      function resPostWeb(url, text){
        $http({
            method : "POST",
            url : url,
            data: {
                sms: text
            }
        }).then(function mySuccess(response) {
            if(response.data.message)
            {
                document.getElementById('id01').style.display='block';
                $scope.contentInfo = response.data.message;
            }
            $scope.swInfo = response.data.swInfo;
            $scope.stopword = response.data.stopword;
            $scope.content = response.data.records;
        }, function myError(response) {
            $scope.content = "Something went wrong";
        });
      };
      $scope.doCheck = function()
      {
        var sms = $scope.smsText;
        url = '';
        if(sms)
        {
            url = server + "/CheckSms";
            resPostWeb(url, sms)
        }
        else
        {
            url = server + "/" ;
            resPostWeb(url, '');
        }
      }
      $scope.doAddSpam = function(text)
      {
        url = server + "/AddSpamLearn";
        resPostWeb(url, text);
      }
      $scope.doAddHam = function(text)
      {
        url = server + "/AddHamLearn";
        resPostWeb(url, text);
      }
      $scope.doReviewSW = function()
      {
        url = server + "/StopWord";
        resPostWeb(url, '')
        document.getElementById('id02').style.display='block';
      }
      $scope.doUpdateSW = function()
      {
        var text = $scope.txtStopWord;
        if(text)
        {
            url = server + "/AddStopWord";
            resPostWeb(url, text)
            document.getElementById('id02').style.display='block';
        }
      }
      $scope.doRemoveSW = function()
      {
        var text = $scope.txtStopWord;
        if(text)
        {
            url = server + "/RemoveStopWord";
            resPostWeb(url, text)
            document.getElementById('id02').style.display='block';
        }
      }
    });