'use strict';

/* Services */

var p2pServices = angular.module('p2pServices', ['ngResource']);
p2pServices.value('version', '0.1');

p2pServices.factory('Question', ['$resource',
    function($resource){
        return $resource('questions/:questionId.json', {}, {
            query: {method:'GET', params:{questionId:'questions'}, isArray:true}
        });
}]);
