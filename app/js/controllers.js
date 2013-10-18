'use strict';

/* Controllers */
var appControllers = angular.module('p2pControllers', ['ui.bootstrap']);

appControllers.controller('QuestionListCtrl', ['$scope', 'Question',
    function($scope, Question) {
        $scope.questions = Question.query();
        $scope.orderProp = 'age';
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

appControllers.controller('TabsCtrl', ['$scope', function($scope) {

        $scope.tabs = [
            { title:"Questions", content:"", active: true},
            { title:"Users", content:""},
            { title:"Unanswered", content:""},
            { title:"Ask", content:"" }
        ];

        $scope.navType = 'pills';

}]);

appControllers.controller('QuestionAskCtrl', ['$scope', '$location',function($scope, $location){
$scope.goNext = function (hash) { 
$location.path(hash);
};

}]);

appControllers.controller('RegisterCtrl', ['$scope', '$location',function($scope, $location){
$scope.goNext = function (hash) { 
$location.path(hash);
};

}]);

appControllers.controller('ButtonsCtrl', ['$scope', '$location',function($scope, $location){ 
$scope.goNext = function (hash) { 
$location.path(hash);
};

}]);
