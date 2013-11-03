'use strict';

/* Controllers */
var appControllers = angular.module('p2pControllers', ['ui.bootstrap']);

appControllers.controller('QuestionListCtrl', ['$scope', 'Question',
    function($scope, Question) {
        $scope.questions = Question.query();
}]);

appControllers.controller('QuestionDetailCtrl', ['$scope', '$routeParams', '$location', 'Temp', 'Question',
    function($scope, $routeParams, $location, Temp, Question) {
       $scope.question = Temp.pull();
    $scope.setImage = function(imageUrl) {
        $scope.mainImageUrl = imageUrl;
    };
    $scope.goNext = function (hash) {
        $location.path(hash);
    };
    $scope.addAns = function() {
        Temp.answer();
    };
}]);

appControllers.controller('LoginCtrl', ['$scope', '$location', function($scope, $location) {  
    $scope.goNext = function (hash) {
        $location.path(hash);
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

appControllers.controller('MyAnsCtrl', ['$scope', 'ProfileAnswers',
    function($scope, ProfileAnswers) {
        $scope.items = ProfileAnswers.pull();
}]);

appControllers.controller('MyQnsCtrl', ['$scope', 'Profile',
    function($scope, Profile) {
        $scope.items = Profile.pull();
}]);