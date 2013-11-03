'use strict';

/* Services */

var p2pServices = angular.module('p2pServices', ['ngResource']);

p2pServices.factory('Question', ['$resource',
    function($resource){
        return $resource('questions.json', {}, {
            query: {method:'GET',
                    params:{questionId:'questions'},
                    isArray:true},
            save: {method:'POST',
                   headers: {
                       'Authorization': 'Basic ' + window.btoa("testUser:testPass")
                  }},
            answer: {method:'PUT',
                     params:{questionId:'how-do-i-connect-to-itunes-store'}
                    },
        });
}]);


p2pServices.factory('User', ['$resource',
    function($resource){
        return $resource('http://localhost:5000/register', {}, {
            save: {method:'POST'}
        });
}]);

p2pServices.factory('Profile', ['$resource',
    function($resource){
        return $resource('user1-questions.json', {}, {
            pull: {method:'GET',
                    isArray:true},
        });
}]);

p2pServices.factory('ProfileAnswers', ['$resource',
    function($resource){
        return $resource('user1-answers.json', {}, {
            pull: {method:'GET',
                    isArray:true},
        });
}]);

p2pServices.factory('Temp', ['$resource',
    function($resource){
        return $resource('how-do-i-connect-to-itunes-store.json', {}, {
            pull: {method:'GET'},
            answer: {method:'PUT'},
        });
}]);