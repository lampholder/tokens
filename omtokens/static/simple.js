var app = angular.module('simple', []);

app.factory('Data', function($http) {
    var data = null;
    var ajax = null;
    getBuckets = function(callback) {
        if (null !== data) {
            callback(data);
        }
        else if (null === ajax) {
            ajax = $http.get('/buckets').then(function(result) {
                data = result.data;
                callback(data);
            });
        }
        else {
            ajax.then(function(result) {
                getBuckets(callback);
            })
        }
    };

    return {
        // public API
        getBuckets: getBuckets
    };
});

app.controller('OtherSimpleCtrl', function($scope, Data) {
    Data.getBuckets(function(data) {
        $scope.data = data.bucketData;
    });

    $scope.isBucket = function(cell) {
        return cell.hasOwnProperty('whcode');
    }
});

app.controller('SimpleCtrl', function($scope, Data) {
    Data.getBuckets(function(data) {
        $scope.data = data.bucketData;
    });
});

app.directive('tokencell', function() {
    return {
        restrict: 'E',
        scope: {
            cell: '='
        },
        template: '<span ng-if="false == cell.hasOwnProperty(\'whcode\')">{{cell}}</span> ' +
                  '<span ng-show="true == cell.hasOwnProperty(\'whcode\')"><tokens-ui cell=cell></tokesn-ui>' +
                         '</span>'
    };
});

app.directive('tokensUi', function() {
    return {
        restrict: 'E',
        scope: {
            cell: '='
        },
        template: '<input type="text" ng-model="cell.count"></input><span>woo</span>',
        link: function(scope, element, attrs) {
            scope.incr = function() {
                cell.count = 15;
            }
            scope.decr = function() {
                cell.count -= 1;
            }
            element.find('span').bind('click', function() {
                scope.incr();
            });
        }
    }
});