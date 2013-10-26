'use strict';

/* Services */

var p2pServices = angular.module('p2pServices', ['ngResource']);

p2pServices.factory('Question', ['$resource',
    function($resource){
        return $resource('questions/:questionId.json', {}, {
            query: {method:'GET',
                    params:{questionId:'questions'},
                    isArray:true},
            save: {method:'POST',
                   headers: {
                       'Authorization': 'Basic ' + window.btoa("testUser:testPass")
                  }}
        });
}]);

p2pServices.factory('Profile', ['$resource',
    function($resource){
        return $resource('questions/user1-questions.json', {}, {
            pull: {method:'GET',
                    isArray:true},
        });
}]);
