'use strict';


// Declare app level module which depends on filters, and services
var p2pApp = angular.module('p2pApp', [
  'ngRoute',
  'ngTouch',
  'ngCookies',
  'p2pFilters',
  'p2pServices',
  'p2pDirectives',
  'p2pControllers'
]);

p2pApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/questions', {templateUrl: 'partials/question-list.html', controller: 'QuestionListCtrl'});
  $routeProvider.when('/questions/:questionId', {templateUrl: 'partials/question-detail.html', controller: 'QuestionDetailCtrl'});
  $routeProvider.when('/ask', {templateUrl: 'partials/question-ask.html', controller: 'QuestionAskCtrl'});
  $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: 'LoginCtrl'});
  $routeProvider.when('/register', {templateUrl: 'partials/register.html', controller: 'RegisterCtrl'});
  $routeProvider.when('/myQns', {templateUrl: 'partials/question-my-question.html', controller: 'MyQnsCtrl'});
  $routeProvider.when('/myAns', {templateUrl: 'partials/question-my-answer.html', controller: 'MyAnsCtrl'});
  $routeProvider.when('/profile', {templateUrl: 'partials/profile.html', controller: 'ProfileCtrl'});
  $routeProvider.otherwise({redirectTo: '/login'});
}]);
