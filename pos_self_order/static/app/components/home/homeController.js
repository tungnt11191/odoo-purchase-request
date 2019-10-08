/// <reference path="../../../scripts/plugins/angular-1.7.8/angular.js" />

(function (app) {
    app.controller('homeController', homeController);
    homeController.$inject = ['apiService', '$scope', 'notificationService', '$http','$state','$rootScope','orderService'];
    function homeController(apiService, $scope, notificationService, $http, $state,$rootScope,orderService) {

        $scope.category_id = 0;
        $scope.products = [];
        $scope.is_form_submmited = false;

        $scope.InputCustomerInfo = InputCustomerInfo;
        $scope.CustomerConfirmOrder = CustomerConfirmOrder;
        function InputCustomerInfo() {
            $scope.is_form_submmited = true;
        }

        function get_pos_categories(){
            apiService.get('/customer/pos/category', null, function (result) {
                var data = result.data;
                $scope.categories = data.categories;
            }, function (e) {
                console.log('Failed.');
            });
        }
        get_pos_categories();

        $scope.onCategorySelected = function (selectedItem) {
           console.log(selectedItem);
           $scope.category_id = selectedItem.id;
           get_pos_products($scope.category_id);
        }

        function get_pos_products(category_id){
            var params = {'jsonrpc': "2.0", 'method': "call", "params": {'category_id': category_id}}
            apiService.get('/customer/pos/product', params, function (result) {
                console.log(result)
                var data = result.data;
                $scope.products = data.products;
            }, function (e) {
                console.log('Failed.');
            });
        }
        get_pos_products($scope.category_id);

        $scope.choose_product = function(product){
            var existed_index = is_exist_product_in_order(product.id);
            if(existed_index > -1){
                $rootScope.order.order_line[existed_index].quantity =  $rootScope.order.order_line[existed_index].quantity + 1;
            } else {
                 $rootScope.order.order_line.push({
                                                product_id: product.id,
                                                product_name: product.name,
                                                price_unit: product.lst_price,
                                                quantity:1,
                                                uom:product.uom_id[1]})
            }

            $rootScope.total_amount += product.lst_price;
            $rootScope.re_compute_total_quantity();
        }

        function is_exist_product_in_order(product_id){
            var lines = $rootScope.order.order_line;
            var index = -1;
            for(order_line in lines) {
                if(lines[order_line].product_id == product_id){
                    return order_line
                }
            }
            return index;
        }

        function CustomerConfirmOrder(){

            var params = {'jsonrpc': "2.0", 'method': "call", "params": {'order': $rootScope.order}}
            apiService.post("/customer/pos/order/create", params, function (result) {
                console.log(result);
                var data = result.data.result;
                if(data!=false){

                }else{
                    notificationService.displayError('Create fail.');
                }
            }, function (error) {
                console.log(error);
                notificationService.displayError('Create fail.');
            })
        }

    }
})(angular.module('ecn'));