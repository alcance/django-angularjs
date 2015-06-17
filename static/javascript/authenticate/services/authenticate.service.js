/*
* Authenticate Factory
* @namespace djangoangular.authenticate.services
*/
(function () {
    'use strict';

    angular
        .module('djangoangular.authenticate.services')
        .factory('Authenticate', Authenticate);

    Authenticate.$inject = ['$cookies', '$http'];

    /*
    * @namespace Authenticate
    * @returns (Factory)
    */

    function Authenticate($cookies, $http) {
        /*
        * @name Authenticate
        * @returns The Factory to be returned
        */
        var Authenticate = {
            register: register
        };

        return Authenticate

        ///////////////////

        /**
        * @name register
        * @desc Try to register a new user
        * @param (string) username The username entered by the user
        * @param (string) password The password entered by the user
        * @param (string) email The email entered by the user
        * @returns (Promise)
        * @memberOf djangoangular.authenticate.services.Authenticate
        */
        function register(email, password, username) {
            return $http.post('api/v1/accounts', {
                username: username,
                password: password,
                email: email
            });
        }
    }
})();
