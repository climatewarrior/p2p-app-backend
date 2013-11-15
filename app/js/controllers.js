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

        $scope.addAns = function() {
            console.log($scope.answer);
            Question.answer({questionId: $routeParams.questionId},
                            {"answer":{
                                "content":$scope.answer}});
            $location.path("/profile");
        };

    }]);

appControllers.controller('ProfileCtrl', ['$scope', '$location', '$routeParams', 'User', function($scope, $location, $routeParams, User) {

        $scope.goNext = function (hash) {
            $location.path(hash);
        };
        $scope.user = User.get({username:$routeParams.username});
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
        $location.path("/profile");
    };

    $scope.goNext = function (hash) {
        $location.path(hash);
    };

    $scope.myPictures = [];
    $scope.$watch('myPicture', function(value) {
        if(value) {
            myPictures.push(value);
        }
    }, true);

}]);

appControllers.controller('RegisterCtrl', ['$scope', '$location', 'User', function($scope, $location, User){
    $scope.user = {};

    $scope.goNext = function (hash) {
        $location.path(hash);
    };

    $scope.addUser = function() {
        console.log($scope.user);
        User.save({}, $scope.user);
        $location.path("/login");
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

            $location.path("/questions");
        };

        var error = function(data, status, headers, config) {
            $scope.authFailedAlert();
        };

        Auth.correctCredentials($scope.user.username, $scope.user.password, success, error);
    };

}]);


appControllers.controller('ProfileCtrl', ['$scope', '$location', '$routeParams', 'User', function($scope, $location, $routeParams, User) {

        $scope.goNext = function (hash) {
            $location.path(hash);
        };
        $scope.user = User.get({username:$routeParams.username});
    }]);
	
appControllers.controller('MyAnsCtrl', ['$scope', '$location', '$routeParams', 'ProfileAnswers', function($scope, $location, $routeParams, ProfileAnswers) {

        $scope.goNext = function (hash) {
            $location.path(hash);
        };
        $scope.ProfileAnswers = ProfileAnswers.get({username:$routeParams.username});
    }]);

appControllers.controller('MyQnsCtrl', ['$scope', '$location', '$routeParams', 'Profile', function($scope, $location, $routeParams, Profile) {

        $scope.goNext = function (hash) {
            $location.path(hash);
        };
        $scope.Profile = Profile.get({username:$routeParams.username});
    }]);	


