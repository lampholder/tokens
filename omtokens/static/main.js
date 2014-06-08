    var App = angular.module('OM_TOKENS', ['ngResource']);

    function TablesController($scope, $http) {
        $http.get('/buckets')
        .then(function(res){
          $scope.tables = res.data;                
        });
 
        //$scope.add = function() {
        //$scope.contacts.push($scope.newcontact);
        //$scope.newcontact = "";
        //}
    }

    function TableController($scope) {

    }