'use strict';

/* Controllers */
var appControllers = angular.module('p2pControllers', ['ui.bootstrap']);

appControllers.controller('QuestionListCtrl', ['$scope', 'Question',
    function($scope, Question) {
        $scope.questions = Question.query();
}]);

appControllers.controller('QuestionDetailCtrl', ['$location', '$scope', '$routeParams', 'Question',
    function($location, $scope, $routeParams, Question) {

        $scope.answer = {};

        $scope.question = Question.get({questionId: $routeParams.questionId}, function(question) {
            $scope.mainImageUrl = question.images[0];
        });

        $scope.setImage = function(imageUrl) {
            $scope.mainImageUrl = imageUrl;
        };

        $scope.goNext = function (hash) {
            $location.path(hash);
        };

        $scope.addAns = function() {
            console.log($scope.answer);
            Question.answer({questionId: $routeParams.questionId}, $scope.answer);
        };

    }]);



appControllers.controller('QuestionAskCtrl', ['$scope', '$location', 'Question', function($scope, $location, Question){
    $scope.question = {};
    $scope.alerts = [];

    $scope.addAlert = function() {
        $scope.alerts.push({type: 'success', msg: "Question submitted!"});
    };

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.addQuestion = function () {
        Question.save({}, $scope.question);
        $scope.addAlert();
    };

    $scope.goNext = function (hash) {
        $location.path(hash);
    };

}]);

appControllers.controller('RegisterCtrl', ['$scope', '$location', 'User', function($scope, $location, User){
    $scope.user = {};

    $scope.goNext = function (hash) {
        $location.path(hash);
    };

    $scope.addUser = function() {
        User.save({}, $scope.user);
    };

}]);

appControllers.controller('LoginCtrl', ['$scope', '$location', 'Auth', function($scope, $location, Auth) {

    $scope.user = {};
    $scope.alerts = [];

    $scope.authFailedAlert = function() {
        $scope.alerts.push({type: 'error', msg: "Wrong username or password."});
    };

    $scope.authSuccessAlert = function() {
        $scope.alerts.push({type: 'success', msg: "Logged in."});
    };

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.goNext = function (hash) {
        $location.path(hash);
    };

    $scope.login = function () {

        console.log($scope.user.username);

        var success = function(data, status, headers, config) {
            Auth.setCredentials($scope.user.username, $scope.user.password);
            $scope.authSuccessAlert();
        };

        var error = function(data, status, headers, config) {
            $scope.authFailedAlert();
        };

        Auth.correctCredentials($scope.user.username, $scope.user.password, success, error);
    };

}]);

appControllers.controller('MyAnsCtrl', ['$scope', 'ProfileAnswers',
    function($scope, ProfileAnswers) {
        $scope.items = ProfileAnswers.pull();
}]);

appControllers.controller('MyQnsCtrl', ['$scope', 'Profile', function($scope, Profile) {
        $scope.items = Profile.pull();
}]);
