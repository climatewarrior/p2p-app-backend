'use strict';

/* Controllers */
var appControllers = angular.module('p2pControllers', ['ui.bootstrap']);

appControllers.controller('PhoneListCtrl', ['$scope', 'Question',
    function($scope, Question) {
        $scope.questions = Question.query();
        $scope.orderProp = 'age';
}]);

appControllers.controller('MyCtrl1', [function() {

}]);

appControllers.controller('MyCtrl2', [function() {

}]);

appControllers.controller('Accordion', ['$scope', function($scope) {
        $scope.oneAtATime = true;

        $scope.groups = [
            {
                title: "Dynamic Group Header - 1",
                content: "Dynamic Group Body - 1"
            },
            {
                title: "Dynamic Group Header - 2",
                content: "Dynamic Group Body - 2"
            }
        ];

        $scope.items = ['Item 1', 'Item 2', 'Item 3'];

        $scope.addItem = function() {
            var newItemNo = $scope.items.length + 1;
            $scope.items.push('Item ' + newItemNo);
        };
    }
]);
