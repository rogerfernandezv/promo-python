var promoApp = angular.module('promocoesApp',[]);

promoApp.controller('PromocoesController', function($scope, $http, $timeout, $window, $rootScope, srvAuth){
  var todoList = this;
  //var url = "http://192.168.10.10:5000/promojson";
  var url = "http://promocao-rogerdev.rhcloud.com/postsprom";
  $scope.getData = function(){
    $http.get(url).
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
