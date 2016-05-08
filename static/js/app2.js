var promoApp = angular.module('promocoesApp',[]);

promoApp.controller('PromocoesController', function($scope, $http, $timeout){
  var todoList = this;

  $scope.getData = function(){
    $http.get('http://promocao-rogerdev.rhcloud.com/promojson').
      success(function(data){
        $scope.promos = data;
        window.console.log("capturando");
      }).
      error(function(data){
        window.console.log("erro get json");
      });
  };

    $scope.getData();

    $scope.intervalFunction = function(){
      $timeout(function(){
        $scope.getData();
        $scope.intervalFunction();
      }, 60000);
    };

    $scope.intervalFunction();
});
