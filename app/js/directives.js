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


angular.module('p2pDirectives', []).directive('uservote', function () {
    return {
        restrict: 'E',
        scope: { 'votes': '=data' },
        template: template
    };
});
