(function (app) {
    app.controller('rootController', rootController);

    rootController.$inject = ['$state', '$scope','$rootScope','apiService'];

    function rootController($state, $scope, $rootScope,apiService) {
        $scope.sideBar = "/pos_self_order/static/app/shared/views/navigation.html";
        $rootScope.total_quantity = 0;
        $rootScope.total_amount = 0;
        $rootScope.customer_info = {
            'security_code': '',
            'customer_name': '',
            'customer_number' : 0
        }
        $rootScope.order = {
            'customer' : $scope.customer_info,
            'order_line': []
        }

        $rootScope.re_compute_total_quantity = function(){
            var total_quantity = 0;
            var lines = $rootScope.order.order_line;
            for(order_line in lines) {
                total_quantity+=lines[order_line].quantity;
            }
            $rootScope.total_quantity = total_quantity;

        }
    }
})(angular.module('ecn'));