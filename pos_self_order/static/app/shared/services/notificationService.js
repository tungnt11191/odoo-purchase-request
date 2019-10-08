(function (app) {
    app.factory('notificationService', notificationService);
    notificationService.$inject = ['toaster'];
    function notificationService(toaster) {
        toaster.options = {
            "debug": false,
            "positionClass": "toast-top-right",
            "onclick": null,
            "fadeIn": 300,
            "fadeOut": 1000,
            "timeOut": 3000,
            "extendedTimeOut": 1000
        };

        function display(type,message){
            toaster.pop({
                type: type,
                title: message,
            });
        }
        function displaySuccess(message) {
            toaster.success(message);
        }

        function displayError(error) {
            if (Array.isArray(error)) {
                error.each(function (err) {
//                    toaster.error(err);
                    display('error');
                });
            }
            else {
//                toaster.error(error);
                display('error');
            }
        }

        function displayWarning(message) {
            toaster.warning(message);
        }
        function displayInfo(message) {
            toaster.info(message);
        }

        return {
            displaySuccess: displaySuccess,
            displayError: displayError,
            displayWarning: displayWarning,
            displayInfo: displayInfo
        }
    }
})(angular.module('ecn.common'));