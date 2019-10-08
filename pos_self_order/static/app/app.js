/// <reference path="../scripts/plugins/angular-1.7.8/angular.js" />
(function () {
    angular.module('ecn', ['ecn.common'])
        .config(config);
    config.$inject = ['$stateProvider', '$urlRouterProvider',];

    function config($stateProvider, $urlRouterProvider) {
        $stateProvider.state('base', {
            url: '',
            templateUrl: '/pos_self_order/static/app/shared/views/baseView.html',
            abstract: true
        }).state('home', {
            url: "/home",
            parent: 'base',
            templateUrl: "/pos_self_order/static/app/components/home/homeView.html",
            controller: "homeController"
        });
        $urlRouterProvider.otherwise('/home');

    }
})();