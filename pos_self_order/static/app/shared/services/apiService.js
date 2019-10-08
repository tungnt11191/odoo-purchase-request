/// <reference path="../../../scripts/plugins/angular-1.7.8/angular.js" />

(function (app) {
    app.factory('apiService', apiService);

    apiService.$inject = ['$http','notificationService'];

    function apiService($http, notificationService) {
        return {
            get: get,
            put: put,
            post: post,
            del: del
        }
        function post(url, data, success, failure) {
            $http.post(url, data).then(function (result) {
                success(result);
            }, function (error) {
                if (error.status == '401') {
                    notificationService.displayError("Authenticate require");
                }
                failure(error);
                notificationService.displayError(error);
            })
        }
        function get(url, params, success, failure) {
            $http.get(url, params).then(function (result) {
                success(result);
            }, function (error) {
                failure(error);
            });
        }
        function put(url, data, success, failure) {
            $http.put(url, data).then(function (result) {
                success(result);
            }, function (error) {
                console.log(error.status)
                if (error.status === 401) {
                    notificationService.displayError('Authenticate is required.');
                }
                else if (failure != null) {
                    failure(error);
                }
            });
        }
        function del(url, data, success, failure) {
            $http.delete(url, data).then(function (result) {
                success(result);
            }, function (error) {
                console.log(error.status)
                if (error.status === 401) {
                    notificationService.displayError('Authenticate is required.');
                }
                else if (failure != null) {
                    failure(error);
                }

            });
        }
    }
})(angular.module('ecn.common'));