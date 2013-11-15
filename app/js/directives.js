'use strict';

/* Directives */

var template =
    ['<div class="muted text-center">',
     '<i class="icon-arrow-up"></i>',
     '<br>',
     '<bold>{{votes}}</bold>',
     '<br>',
     '<i class="icon-arrow-down"></i>',
     '<br>',
     '<i class="icon-star"></i>',
     '</div>'].join('\n')


var p2pDirectives = angular.module('p2pDirectives', [])

p2pDirectives.directive('uservote', function () {
    return {
        restrict: 'E',
        scope: { 'votes': '=data' },
        template: template
    };
});

p2pDirectives.directive('camera', function() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl) {
            elm.on('click', function() {
                navigator.camera.getPicture(function (imageURI) {
                    scope.$apply(function() {
                        ctrl.$setViewValue(imageURI);
                    });
                }, function (err) {
                    ctrl.$setValidity('error', false);
                }, { quality: 50, destinationType: navigator.camera.DestinationType.FILE_URI })
                                           });
                  }
        };
    });
