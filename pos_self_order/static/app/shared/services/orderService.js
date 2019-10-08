/// <reference path="../../../scripts/plugins/angular-1.7.8/angular.js" />

(function (app) {
    app.factory('orderService', orderService);

    orderService.$inject = ['$http','notificationService'];

    function orderService($http, notificationService) {
        var service = {
            order: []
        };

        return service;
    }
})(angular.module('ecn.common'));