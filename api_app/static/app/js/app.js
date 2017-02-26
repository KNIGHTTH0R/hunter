'use strict';


// Declare app level module which depends on filters, and services
var app = angular.module('myApp', [
    'ngRoute',
    'myApp.filters',
    'myApp.services',
    'myApp.directives',
    'myApp.controllers'
]).
    config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/plugin', {templateUrl: 'app/partials/plugin.html?v=9', controller: 'PluginCtrl'});
        $routeProvider.when('/achievements', {templateUrl: 'app/partials/achievements.html?v=9', controller: 'AchievementsCtrl'});
        $routeProvider.when('/player', {templateUrl: 'app/partials/player.html?v=9', controller: 'PlayerCtrl'});
        $routeProvider.when('/player/:param1', {templateUrl: 'app/partials/player.html?v=9', controller: 'PlayerCtrl'});
        $routeProvider.when('/settings', {templateUrl: 'app/partials/settings.html?v=9', controller: 'SettingsCtrl'});
        $routeProvider.when('/about', {templateUrl: 'app/partials/about.html?v=9', controller: 'AboutCtrl'});
        $routeProvider.when('/instructions', {templateUrl: 'app/partials/instructions.html?v=9', controller: 'InstrCtrl'});
        $routeProvider.otherwise({redirectTo: '/plugin'});
    }]);

    app.run(function($rootScope, $http, UserService, $location) {
        $rootScope.googleMapsUrl="https://maps.googleapis.com/maps/api/js?key=AIzaSyD2yRg4ZAhBINo7CY7kcs2swDJxMXDoffo";
        $rootScope.TEAM_TO_CSS = {2: 'deepskyblue', 1: 'limegreen', 3: '#FECE5A', 'RESISTANCE': 'deepskyblue', 'ALIENS': 'limegreen'};
        $rootScope.TEAM_NAME = {1: 'ENLIGHTENED', 2: 'RESISTANCE', 3: 'NEUTRAL'};
        $rootScope.BADGE_GRADUATE = {
            1: 'BRONZE',
            2: 'SILVER',
            3: 'GOLD',
            4: 'PLATINUM',
            5: 'BLACK'
        };

        var zeroPad = function(number,pad) {
          number = number.toString();
          var zeros = pad - number.length;
          return Array(zeros>0?zeros+1:0).join("0") + number;
        };

        $rootScope.unixTimeToString = function(time) {
              if(!time) return null;
              var d = new Date(typeof time === 'string' ? parseInt(time) : time);
              var time = d.toLocaleTimeString();
              var date = d.getFullYear()+'-'+zeroPad(d.getMonth()+1,2)+'-'+zeroPad(d.getDate(),2);
              return date + ' ' + time;
        };

        $rootScope.unixTimeDiffDays = function(time) {
          if(!time) return null;
          var nowdate = new Date().getTime();
          var diff = Math.floor((nowdate - time)/86400000);
          return diff;
        };

        $rootScope.getUrl = function(late6, lnge6) {
            var url = 'https://www.ingress.com/intel?ll='+late6/1E6+','+lnge6/1E6+'&z=17&pll='+late6/1E6+','+lnge6/1E6;
            return url;
        };

        $rootScope.playersearch = function(player) {
            console.log(player);
            $rootScope.findValue = player;
            $location.path('/player/'+$rootScope.findValue)
        };

        $rootScope.plains = {
            1: ' deployed a Resonator on ',
            2: ' captured ',
            3: ' destroyed a Resonator on ',
            4: ' linked ',
            5: ' created a Control Field @',
            6: ' destroyed the Link ',
            7: ' destroyed a Control Field @',
            8: ' deployed a Portal Fracker on ',
            9: ' deployed a Beacon on ',
        };

        $rootScope.user = [];

        loadRemoteData();

        function applyRemoteData( newUser ) {
            $rootScope.user = newUser;
        }

        function loadRemoteData() {
            UserService.getUser()
                .then(
                    function( user ) {
                        applyRemoteData( user );
                    });
        }
    });

    app.service(
            "UserService",
            function( $http, $q ) {
                return({
                    getUser: getUser
                });

                function getUser() {
                    var request = $http({
                        method: "get",
                        url: "/api/user",
                    });
                    return( request.then( handleSuccess, handleError ) );
                }

                function handleError( response ) {
                    if (
                        ! angular.isObject( response.data ) ||
                        ! response.data.message
                        ) {
                        return( $q.reject( "An unknown error occurred." ) );
                    }
                    return( $q.reject( response.data.message ) );
                }
                function handleSuccess( response ) {
                    return( response.data.result );
                }
            }
        );

    app.directive('loading',   ['$http', '$rootScope' ,function ($http, $rootScope)
    {
        return {
            restrict: 'A',
            link: function (scope, elm, attrs)
            {
                scope.isLoading = function () {
                    return $http.pendingRequests.length > 0;
                };

                scope.$watch(scope.isLoading, function (v)
                {
                    if(v){
                        $rootScope.error = null;
                        elm.show();
                    }else{
                        elm.hide();
                    }
                });
            }
        };

    }]);