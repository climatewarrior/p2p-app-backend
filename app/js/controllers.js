'use strict';

/* Controllers */
var appControllers = angular.module('p2pControllers', ['ui.bootstrap']);

appControllers.controller('QuestionListCtrl', ['$scope', 'Question',
    function($scope, Question) {
        $scope.questions = Question.query();
}]);

appControllers.controller('QuestionDetailCtrl', ['$scope', '$routeParams', 'Question',
    function($scope, $routeParams, Question) {
        $scope.question = Question.get({questionId: $routeParams.questionId}, function(question) {
        $scope.mainImageUrl = question.images[0];
    });
    $scope.setImage = function(imageUrl) {
        $scope.mainImageUrl = imageUrl;
    };
}]);

appControllers.controller('LoginCtrl', [function() {
}]);

appControllers.controller('ButtonsCtrl', ['$scope', '$location',function($scope, $location) {
    $scope.goNext = function (hash) {
        $location.path(hash);
 };

}]);

appControllers.controller('QuestionAskCtrl', ['$scope', 'Question', function($scope, Question){
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

}]);

appControllers.controller('RegisterCtrl', ['$scope', '$location',function($scope, $location){
$scope.goNext = function (hash) {
$location.path(hash);
};

}]);
