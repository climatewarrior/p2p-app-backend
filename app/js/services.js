'use strict';

/* Services */

var p2pServices = angular.module('p2pServices', ['ngResource']);

p2pServices.factory('Question', ['$resource',
    function($resource){
        return $resource('http://localhost:5000/questions/:questionId', {}, {
            query: {method:'GET',
                    params:{questionId:'questions'},
                    isArray:true},
            save: {method:'POST',
                   headers: {
                       'Authorization': 'Basic ' + window.btoa("testUser:testPass")
                  }}
        });
}]);
