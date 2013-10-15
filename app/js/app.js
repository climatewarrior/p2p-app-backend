'use strict';


// Declare app level module which depends on filters, and services
var p2pApp = angular.module('p2pApp', [
  'ngRoute',
  'p2pFilters',
  'p2pServices',
  'p2pDirectives',
  'p2pControllers'
]);

p2pApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/questions', {templateUrl: 'partials/question-list.html', controller: 'QuestionListCtrl'});
  $routeProvider.when('/questions/:questionId', {templateUrl: 'partials/question-detail.html', controller: 'QuestionDetailCtrl'});
  $routeProvider.when('/view3', {templateUrl: 'partials/partial3.html', controller: 'Accordion'});
  $routeProvider.otherwise({redirectTo: '/questions'});
}]);
