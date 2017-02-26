'use strict';

/* Controllers */

angular.module('myApp.controllers', [])
    .controller('PluginCtrl', ['$scope', '$location', function($scope, $location) {
        $scope.$parent.title = "Plugin page";
    }])
    .controller('AchievementsCtrl', ['$scope', '$http', function($scope, $http) {
        $scope.$parent.title = "Achievements";

        function initialize(late6, lnge6) {
            if (late6 && lnge6) {
                var lat = late6 / 1E6;
                var lng = lnge6 / 1E6;
                var z = 6;
            } else if (readCookie('ingress-guard.intelmap.lat') && readCookie('ingress-guard.intelmap.lng')) {
                var lat = parseFloat(readCookie('ingress-guard.intelmap.lat')) || 34.010550;
                var lng = parseFloat(readCookie('ingress-guard.intelmap.lng')) || -118.085861;
                var z = parseInt(readCookie('ingress-guard.intelmap.zoom')) || 10;
            } else {
                var lat = 34.010550;
                var lng = -118.085861;
                var z = 10;
            }

            var ingressGMapOptions = {
                backgroundColor: '#0e3d4e',
                styles: [{
                    featureType: "all",
                    elementType: "all",
                    stylers: [{
                        visibility: "on"
                    }, {
                        hue: "#131c1c"
                    }, {
                        saturation: "-50"
                    }, {
                        invert_lightness: true
                    }]
                }, {
                    featureType: "water",
                    elementType: "all",
                    stylers: [{
                        visibility: "on"
                    }, {
                        hue: "#005eff"
                    }, {
                        invert_lightness: true
                    }]
                }, {
                    featureType: "poi",
                    stylers: [{
                        visibility: "off"
                    }]
                }, {
                    featureType: "transit",
                    elementType: "all",
                    stylers: [{
                        visibility: "off"
                    }]
                }]
            };

            var e = new google.maps.LatLng(lat, lng),
                t = {
                    zoom: z,
                    center: e,
                    panControl: !0,
                    scrollwheel: 1,
                    scaleControl: !0,
                    overviewMapControl: !0,
                    overviewMapControlOptions: {
                        opened: !0
                    },
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    backgroundColor: '#0e3d4e',
                    styles: [{
                        featureType: "all",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }, {
                            hue: "#131c1c"
                        }, {
                            saturation: "-50"
                        }, {
                            invert_lightness: true
                        }]
                    }, {
                        featureType: "water",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }, {
                            hue: "#005eff"
                        }, {
                            invert_lightness: true
                        }]
                    }, {
                        featureType: "poi",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit",
                        elementType: "all",
                        stylers: [{
                            visibility: "off"
                        }]
                    }],
                };

            $scope.map = new google.maps.Map(document.getElementById("latlongmap"), t),
                $scope.geocoder = new google.maps.Geocoder,
                $scope.marker = new google.maps.Marker({
                    position: e,
                    map: $scope.map
                }), google.maps.event.addListener($scope.map, "click", function(e) {
                    $scope.marker.setPosition(e.latLng);
                    var t = e.latLng,
                        o = "(" + t.lat().toFixed(6) + ", " + t.lng().toFixed(6) + ")";
                    lat = t.lat().toFixed(6);
                    lng = t.lng().toFixed(6);
                    storeMapPosition(lat, lng)
                })
        }

        // cookies
        var writeCookie = function(name, val) {
            var d = new Date(Date.now() + 10 * 365 * 24 * 60 * 60 * 1000).toUTCString();
            document.cookie = name + "=" + val + '; expires=' + d + '; path=/';
        }

        var storeMapPosition = function storeMapPosition(lat, lng) {
            if (lat >= -90 && lat <= 90)
                writeCookie('ingress-guard.intelmap.lat', lat);

            if (lng >= -180 && lng <= 180)
                writeCookie('ingress-guard.intelmap.lng', lng);

            writeCookie('ingress-guard.intelmap.zoom', $scope.map.getZoom());
        }

        var readCookie = function(name) {
            var C, i, c = document.cookie.split('; ');
            var cookies = {};
            for (i = c.length - 1; i >= 0; i--) {
                C = c[i].split('=');
                cookies[C[0]] = unescape(C[1]);
            }
            return cookies[name];
        }
        initialize();

        $scope.getAchievements = function() {
            if (readCookie('ingress-guard.intelmap.lat') && readCookie('ingress-guard.intelmap.lng')) {
                var lat = parseFloat(readCookie('ingress-guard.intelmap.lat')) || 34.010550;
                var lng = parseFloat(readCookie('ingress-guard.intelmap.lng')) || -118.085861;
                var z = parseInt(readCookie('ingress-guard.intelmap.zoom')) || 10;
            } else {
                var lat = 34.010550;
                var lng = -118.085861;
                var z = 10;
            }
            var faction = $('input[name=optradio]:checked', '#faction').val()

            if ($('input[name=attent]').is(':checked')) {
                var attention = true;
            }
            else {
                var attention = false;
            }

            var days_min = $('#days').val()
            if (days_min) {
                var days_min = days_min;
            } else {
                var days_min = 60;
            }

            var request = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'achievements',
                    late6: lat * 1E6,
                    lnge6: lng * 1E6,
                    zoom: 7,
                    team: faction,
                    days: days_min,
                    attention: attention,
                })
            }).then(function(response) {
                $scope.achieveTableData = response.data.result.achievements;
            }, function(response) {});
        }

        $scope.showOnMap = function getRportals(lat, lng, z, faction) {
            initialize();

            if (readCookie('ingress-guard.intelmap.lat') && readCookie('ingress-guard.intelmap.lng')) {
                var lat = parseFloat(readCookie('ingress-guard.intelmap.lat')) || 34.010550;
                var lng = parseFloat(readCookie('ingress-guard.intelmap.lng')) || -118.085861;
                var z = parseInt(readCookie('ingress-guard.intelmap.zoom')) || 10;
            } else {
                var lat = 34.010550;
                var lng = -118.085861;
                var z = 10;
            }

            var faction = $('input[name=optradio]:checked', '#faction').val()
            var days_min = $('#days').val()
            var iconEnlImage = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAApCAYAAADAk4LOAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAo1SURBVHjanJR5UJNnHscfp7ud7mxnt7u2M+3O9pruzPZ9k5CTHCQByRtCwpWDkIQr5BDU1a7Fiq0V3ogXiCBauVGQQ0AOkUMIoVLvWl1t3e1qW+tVtdt2tVKsMqXW7/4R1OqI2n1nPvPMvL/n9/vM87zzfckL8unkT8I/EPmcV4i1XkLMVSJiqhQRY6WAuJoY4ns3i8RV8mhztchirhFlm6qEBaYq4cKk+lBrepuab64SEUutmCRUCIh7WySxN8pJwgYBMZYJiaVWTCw1YkKmkpgqhcRRFybJbI0pSKjmf2jdFPq9vVF2I6VVAUeT/KekOuk1y0bxcVOlsMRcIw77fyQvGSuENZaNoh/S25WYO2zAwn0WLNpvxaIDiVi034qF+yyY924MPN0zYK2T3IjbELLZ1TnjL48kMVWKwhMqhKfT29V4fXcCcg5aMH9fLObs0iJrJBKZIzOQNRKJ2bsYzN8bg5yDFmTvMcLZoYapSnTeVCWKNpYL75Y8L5tOnuM/ReRzXiGJmyRmU6VwLHMHg5yDFszbrYd3OByegBplHy1B2UdL4A2EwxsIvvME1PAOh2PurmjkHLQga0ALY6XwekKZMOUuycvqZ8jzsulE/rdXpOZa0eiswSgsOJCAzOEIuAdV8PjV8PjV2HmuC+M/XkPpkYXwDqnhGVLfrrkHlZg5HIEF+xMwZygaxnLB98ZyocpSIyaWWjEh+kIe0Rfyfhe7NuS4uycC2Qfi4RlS3xEMBhk83QIAuImbaDm+Dp5B1e1aUKSCZ0iN7ANx8PTMQPw7gs/i1wt+H1vMJySuVEBi1/KXJNVLkb0/HjMDEXDtUME9oA6yI7jekpwePY4bN39E48fFcA/c2ecaUMG1QwXvUDhe3x8Pe4MM0QVc9iXVM4TElvCfiS0J+XqWX4s5I1o4e8KQ0auEq191F/5TbQCA7GEz6o4V4sOv9sHVr0RGvxIZfUpk9AZx9oRh9giD2QEtDEUh/w31vvwsiSkKSbNUSzBvrx6uPhWc25Vw9iiR0TPZ2KdCRp8KQ6e3AgAW7bQja0CL1/xxyNzBYNe5HuTstMPZEwZnT7DX1afCa3v1sNRKEFfKdxJ9AbcprV2J2e9pkdqlQNq2MKR3hwVlk0JnjxJdJ2oBAL2fNcDbGwnndiXKD7MAgAtjZ5DtT0R6dxjStoUhtUuB2SNapLWroC/kNRN9Ifegpy8cXn8EUtrlSO1UIK0rDOnbJukOg7dXg+whC3KG7WDf82DeQBzSu1W4MHYG/s+3ovmf63Bu9CRKDuQgtVOBlA45vP4IuPvCoS/kHSL61byz3sEIuPrVSOlQILUzSFqnAit3zcXhC7twZfwSrk1cxcWxMxg+1YW8EQ/SusLQe6IRR77cg/qjawAARy7umZQo4O5XwzsYAf1q3jmiX8276PVHIKNXCUeLDMltcszarseeswO49Vy69hXOXPkEX109j5s3fwIA7DrTB1fXDKzbvxinvj2BzUeLkdUdjeQ2ORytMmT0KuH1R0C/mneRRK/kHsroCX7cxQNO9J/YgtHxywCA/hNb8Ea/DeltKqS0KZC6NQx/7zOj9Vg5rk98j2+vf4OaQ6uQ2qpAcqscya0yOFpksDdLkdGngnO7CtEruYeJbhmnzdEih9uvRmZHNDYdKoL/03bk+t1IbpEjuy8Js7oMcLap4e7Q4C2/E2/7XZi33Yi6w2uwft8SOFrkcDQHhzu2yGBvksLtV8PRIoNuGaeTGFbz5hnLhPAEwuFolsLeFMTRLIOjWYbi3Yvw0cX3ce7KSZy6fBzvnuzGwr4UOLbIscTvwenLn6DjWA3SWlQ/65XCGwiHsUyImDUh80nUMi4VvYo34epXIbVdAVvjHZG9SQZHkwzuNg3e6E2Gu00LR5McjiY5FvTYcPnaN6h+fyUOnB3GgbMBeLYysDVKkdqhgKtfhehVvAndCi6HROVzpjEsHbA1SJHRr4J1cyiSJrE1SGFvkMHeIENasxqNh9dj/5kAGg6XImurHhe/O4eWI+X4x/m9qPugGEmbQ2GtD4VrhwpJm6VgWNqvW86dRnTLuITx0cmGIl6w2CCFtS70DvWhsNXJMLfdiIkbP2Dnpz3wtETBVi8DO5AVDOi/mmGtC0VinQS2Rincg2oYinjQsHQis5QmRJNHEU0e9aQmjzqV3CZHaocC5hoxLLV3SKyVYHZrPMbGr+DtXjestaFIrJUgZbMa/uMdcDUxsNSKYa4RI61LgeRWGTR51AmGpZ5gWIoQhqUJw9IkMpfKj1svQEafMji85m6yWmIxNj6KJb1eWGrE8DTrkFgbitR6dXBPtRiJmyTI6FMibi0fmjzqTW0+h2jzOYRE5XNu8SLD0peT2+RwtMhgqhLBXC2+TeaWoOTtHi/M1WJ0Ht2EWS3xt+umKhFSJnsZlvoP46OfZXw0YXw0Ibrl3NtE5lEFsWv5SO8Og7laBFOFCKbKIJlNMRgbH8Xibg9MlSIEjm/D+hE2WK8QwVIjhnN7GGJKQqBh6dxbp9Dmcwi5ZZvkOQ1Lf21vlsLeLEVCuRDGiiAzGw0YGx/Fm9tcMFYIcfKbf2PFwHwYK4RIKBfCPpkxhqXPa/M5Tz9IQiLzKDamOARpXQqYKoUwlgWZ2WDAd+NXsGBrMtYGluDL0S+QUhsMnKlShLROBQxrQqDJoxf+XHBfCeOjn2ZY6oKtUQpbYyhiS/iIKxXAvVGPS1e/RtsHNRgbH8W6gA9xpQLElvBhawzmSsNSpxkf/dS9M8m9Vm0+h2hYOsewJgQp7XLErxcgppgPZ3UUro5/BwA4+Pl7iC3hI6aYj/j1AqRslUO/mgfGR7+mW8Yl93K/kxDGRz+lYanT1k0SWOskMKwOQXqlFtcnrmHixg+YuzkJMWtCYCgKCYZwowSaPOpTTS71pCaXIvcylYRoWHquvpAHxxYp4kr5SK+Mwo2fbqDvaBsMRUFB3DoB7FukiC7gITKXyryfQJNLEaJbwZ2K3zIs9Ym5Oph6V2UMvrh0Cq4qA/SFPEQX8JBYK4a5SgwNS33M+KjfMD6K3A8yVYHxUUTDUt7oVVzYGkKRUhGJ5duybwtiSviwNYRCt4ILbT7HqSvgEd2q+0O0SzlTk895QpNHHTNOhk23iovoAh50q7iw1IhhLBciMo86qsmlHp/8B94XMtU9/owU3QourPUSGIpCoFvOQcyaEFjrJIhawQXjo23apTR5EORhG7RL6V8zLH04YYMQpgoRdMs5MFWIEP+OAIyPPhi/QfCrhDIBeRAkYYPggRjLBURfyDNH5XNgrhYjtoQPc7UYUcs5iHjrVWPEm38lD4NEr+Q9nBXcxzQsvTd2LR/WTRLElfIxY/Gru19SPv3Yn0P/SJ6XPphHuS6iXUoThqUMUcs4MJWLELWcg8hcSi9Me5HwU14ggodAGJZ6NHzUNMZHD0ct44Dx0QHGR0+LmjpjdzFl4qdAy7D0BOOjtb+k75dKHmd89MzJ9ZH7/jcAhElqPD31+5YAAAAASUVORK5CYII=';
            var iconResImage = 'data:image/png;base64,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';

            if (faction == 1) {
                var icn = iconEnlImage;
            } else {
                var icn = iconResImage;
            }

            if (days_min) {
                var days_min = days_min;
            } else {
                var days_min = 60;
            }

            if ($('input[name=attent]').is(':checked')) {
                var attention = true;
            }
            else {
                var attention = false;
            }

            var form_data = {
                request: 'achievements',
                late6: lat * 1E6,
                lnge6: lng * 1E6,
                zoom: z,
                team: faction,
                days: days_min,
                attention: attention,
            };

            function customFunction() {
                var iwOuter = $('.gm-style-iw');
                var iwBackground = iwOuter.prev();

                iwBackground.children(':nth-child(1)').css({
                    'display': 'none'
                });
                iwBackground.children(':nth-child(2)').css({
                    'display': 'none'
                });
                iwBackground.children(':nth-child(3)').children(':nth-child(2)').children(':nth-child(1)').css({
                    'background-color': '#167'
                });
                iwBackground.children(':nth-child(3)').children(':nth-child(1)').children(':nth-child(1)').css({
                    'background-color': '#167'
                });

                iwBackground.children(':nth-child(4)').css({
                    'display': 'none'
                });

                var iwCloseBtn = iwOuter.next();

                iwCloseBtn.css({
                    opacity: '1',
                    right: '52px',
                    top: '17px'
                });
            };
            var infoWindow = new google.maps.InfoWindow(),
                marker;
            var LatLngList = [];
            $.ajax({
                type: "POST",
                url: '/api',
                data: JSON.stringify(form_data),
                contentType: "application/json",

                success: function(response) {
                    response.result.achievements.forEach(function(row, i) {
                        $scope.tdiff = $scope.unixTimeDiffDays(row.timestamp)
                        LatLngList[i] = new google.maps.LatLng(row.late6 / 1E6, row.lnge6 / 1E6)
                        var marker = new google.maps.Marker({
                            position: new google.maps.LatLng(row.late6 / 1E6, row.lnge6 / 1E6),
                            map: $scope.map,
                            title: row.player + ' days:' + $scope.tdiff,
                            icon: {
                                url: icn
                            },
                        });

                        if (row.team == 1) {
                            $scope.color_team = 'enl';
                        } else {
                            $scope.color_team = 'res';
                        }

                        if (row.ada) {
                            $scope.ada = '<p style="color: red;">Ada (Jarvis) detected</p><br>'
                        } else {
                            $scope.ada = ''
                        }

                        $scope.cont = '<div id="iw-container"><div class="iw-title"><span class="' + $scope.color_team +
                            '">' + row.name + '</span></div>' + '<div class="iw-content">' +
                            '<div class="iw-subTitle"><img src="' + row.img + '" alt="Portal name: ' + row.name +
                            '" width="83"><span style="color: #cca844;">Owner:</span> <span class="' +
                            $scope.color_team + '"><a class="' + $scope.color_team + '" href="/#/player/' +
                            row.player + '">' + row.player + '</a></span></div>' + '<p>Days: ' + $scope.tdiff +
                            '</p>' + '<a target="_blank" href="https://www.ingress.com/intel?ll=' +
                            row.late6 / 1E6 + ',' + row.lnge6 / 1E6 + '&z=17&pll=' +
                            row.late6 / 1E6 + ',' + row.lnge6 / 1E6 + '">Intel link</a>' +
                            '<div class="iw-address">' + $scope.ada + '<p style="color: #cca844;">' +
                            row.address + '</p></div>' + '</div>' + '</div>';

                        google.maps.event.addListener(marker, 'click', (function(marker, cont) {
                            return function() {
                                infoWindow.setContent(cont);
                                infoWindow.open($scope.map, marker);
                                customFunction();
                            }
                        })(marker, $scope.cont));
                    });

                    var latlngbounds = new google.maps.LatLngBounds();

                    LatLngList.forEach(function(latLng) {
                        latlngbounds.extend(latLng);
                    });

                    $scope.map.setCenter(latlngbounds.getCenter());
                    $scope.map.fitBounds(latlngbounds);
                },
                dataType: "json"
            })
        }
    }])
    .controller('PlayerCtrl', ['$rootScope','$scope', '$http', '$routeParams', function($rootScope, $scope, $http, $routeParams) {
        $scope.$parent.title = "Player Search";

        var player = $routeParams.param1;

        $scope.achievesearch = function(player) {
            $scope.findPlayerValue = player;
            var request_portal = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'player',
                    player: $scope.findPlayerValue
                })
            }).then(function(response) {
                $scope.showAchieveData = response.data.result.achievements;
                if (!$scope.showAchieveData[0] && !response.data.result.hidden) {
                    $rootScope.$broadcast('error', {'error': 'Agent don`t exists or haven`t achievements.'});
                }
                else {
                    $scope.showHidden = response.data.result.hidden;
                }
            }, function(response) {});
        };

        if (player) {
            $scope.findPlayerValue = player;
            var search = $scope.achievesearch(player);
        }

        $scope.playernamesearch = function(player) {
            $scope.findNameValue = player;
            var request_portal = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'player_info',
                    player: $scope.findNameValue,
                })
            }).then(function(response) {
                $scope.showNameData = response.data.result.player_info;
                if (!$scope.showNameData[0]) {
                    $rootScope.$broadcast('error', {'error': 'Agent name was not found in database'});
                }

            }, function(response) {});
        };

        $scope.profilesearch = function(player) {
            $scope.findValue = player;
            $scope.error = null;
            var request_portal = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'get_profile',
                    player: $scope.findValue,
                })}).then(function (response) {
                $scope.error = response.data.result.profile.error;
                $rootScope.$broadcast('error', {'error': $scope.error});
                if (!$scope.error) {
                    $scope.showProfileData = response.data.result.profile;
                }
            }, function (response) {});
        };

        function initialize(late6, lnge6) {
            if (late6 && lnge6) {
                var lat = late6 / 1E6;
                var lng = lnge6 / 1E6;
                var z = 6;
            } else if (readCookie('ingress-guard.intelmap.lat') && readCookie('ingress-guard.intelmap.lng')) {
                var lat = parseFloat(readCookie('ingress-guard.intelmap.lat')) || 34.010550;
                var lng = parseFloat(readCookie('ingress-guard.intelmap.lng')) || -118.085861;
                var z = parseInt(readCookie('ingress-guard.intelmap.zoom')) || 10;
            } else {
                var lat = 34.010550;
                var lng = -118.085861;
                var z = 10;
            }


            var ingressGMapOptions = {
                backgroundColor: '#0e3d4e',
                styles: [{
                    featureType: "all",
                    elementType: "all",
                    stylers: [{
                        visibility: "on"
                    }, {
                        hue: "#131c1c"
                    }, {
                        saturation: "-50"
                    }, {
                        invert_lightness: true
                    }]
                }, {
                    featureType: "water",
                    elementType: "all",
                    stylers: [{
                        visibility: "on"
                    }, {
                        hue: "#005eff"
                    }, {
                        invert_lightness: true
                    }]
                }, {
                    featureType: "poi",
                    stylers: [{
                        visibility: "off"
                    }]
                }, {
                    featureType: "transit",
                    elementType: "all",
                    stylers: [{
                        visibility: "off"
                    }]
                }]
            };

            var e = new google.maps.LatLng(lat, lng),
                t = {
                    zoom: z,
                    center: e,
                    panControl: !0,
                    scrollwheel: 1,
                    scaleControl: !0,
                    overviewMapControl: !0,
                    overviewMapControlOptions: {
                        opened: !0
                    },
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    // ingress style
                    backgroundColor: '#0e3d4e',
                    styles: [{
                        featureType: "all",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }, {
                            hue: "#131c1c"
                        }, {
                            saturation: "-50"
                        }, {
                            invert_lightness: true
                        }]
                    }, {
                        featureType: "water",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }, {
                            hue: "#005eff"
                        }, {
                            invert_lightness: true
                        }]
                    }, {
                        featureType: "poi",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit",
                        elementType: "all",
                        stylers: [{
                            visibility: "off"
                        }]
                    }],
                };

            $scope.map = new google.maps.Map(document.getElementById("latlongmap"), t),
                $scope.geocoder = new google.maps.Geocoder,
                $scope.marker = new google.maps.Marker({
                    position: e,
                    map: $scope.map
                }), google.maps.event.addListener($scope.map, "click", function(e) {
                    $scope.marker.setPosition(e.latLng);
                    var t = e.latLng,
                        o = "(" + t.lat().toFixed(6) + ", " + t.lng().toFixed(6) + ")";
                    lat = t.lat().toFixed(6);
                    lng = t.lng().toFixed(6);
                    storeMapPosition(lat, lng)
                })
        }

        // cookies
        var writeCookie = function(name, val) {
            var d = new Date(Date.now() + 10 * 365 * 24 * 60 * 60 * 1000).toUTCString();
            document.cookie = name + "=" + val + '; expires=' + d + '; path=/';
        }

        var storeMapPosition = function storeMapPosition(lat, lng) {
            if (lat >= -90 && lat <= 90)
                writeCookie('ingress-guard.intelmap.lat', lat);

            if (lng >= -180 && lng <= 180)
                writeCookie('ingress-guard.intelmap.lng', lng);

            writeCookie('ingress-guard.intelmap.zoom', $scope.map.getZoom());
        }

        var readCookie = function(name) {
            var C, i, c = document.cookie.split('; ');
            var cookies = {};
            for (i = c.length - 1; i >= 0; i--) {
                C = c[i].split('=');
                cookies[C[0]] = unescape(C[1]);
            }
            return cookies[name];
        }


        $scope.showPlayerMap = function() {

            var iconEnlImage = 'data:image/png;base64,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';
            var iconResImage = 'data:image/png;base64,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';

            var infoWindow = new google.maps.InfoWindow(),
                marker;

            function customFunction() {

                var iwOuter = $('.gm-style-iw');

                var iwBackground = iwOuter.prev();

                iwBackground.children(':nth-child(1)').css({
                    'display': 'none'
                });
                iwBackground.children(':nth-child(2)').css({
                    'display': 'none'
                });
                iwBackground.children(':nth-child(3)').children(':nth-child(2)').children(':nth-child(1)').css({
                    'background-color': '#167'
                });
                iwBackground.children(':nth-child(3)').children(':nth-child(1)').children(':nth-child(1)').css({
                    'background-color': '#167'
                });

                // Remove the white background DIV
                iwBackground.children(':nth-child(4)').css({
                    'display': 'none'
                });

                var iwCloseBtn = iwOuter.next();

                iwCloseBtn.css({
                    opacity: '1',
                    right: '52px',
                    top: '17px'
                });


            };

            var LatLngList = []
            $.ajax({
                type: "POST",
                url: '/api',
                data: JSON.stringify({
                    request: 'player',
                    player: $scope.findPlayerValue,
                }),
                contentType: "application/json",

                beforeSend: function() {

                    $('#hunter_btn').prop('disabled', true)
                    $('#drawtools_btn').prop('disabled', true)

                    $('#spaning').css('visibility', 'visible');

                },
                success: function(response) {
                    $('#agent_table').remove();
                    $('#latlongmap').css('visibility', 'visible').css('height', '600px').css('width', '100%');
                    initialize(50, 50);
                    response.result.achievements.forEach(function(row, i) {
                        if (row.team == 1) {
                            var icn = iconEnlImage;
                        } else {
                            var icn = iconResImage;
                        }

                        if (row.team == 1) {
                            var color_team = 'enl';
                        } else {
                            var color_team = 'res';
                        }

                        if (row.ada) {
                            var ada = '<p style="color: red;">Ada (Jarvis) detected</p><br>'
                        } else {
                            var ada = ''
                        }

                        LatLngList[i] = new google.maps.LatLng(row.late6 / 1E6, row.lnge6 / 1E6)
                        var tdiff = $scope.unixTimeDiffDays(row.timestamp)
                        var marker = new google.maps.Marker({
                            position: new google.maps.LatLng(row.late6 / 1E6, row.lnge6 / 1E6),
                            map: $scope.map,
                            label: tdiff.toString(),
                            title: row.player + ' days:' + tdiff,
                            icon: {
                                url: icn
                            },
                        });

                        var cont = '<div id="iw-container">' +
                            '<div class="iw-title"><span class="' + color_team + '">' + row.name + '</span></div>' +
                            '<div class="iw-content">' +
                            '<div class="iw-subTitle"><img src="' + row.img + '" alt="Portal name: ' + row.name +
                            '" width="83"><span style="color: #cca844;">Owner:</span> <span class="' +
                            color_team + '"><a class="' + color_team + '" href="/#/player/' + row.player + '">'
                            + row.player + '</a></span></div>' + '<p>Days: ' + tdiff + '</p>' +
                            '<a target="_blank" href="https://www.ingress.com/intel?ll=' +
                            row.late6 / 1E6 + ',' + row.lnge6 / 1E6 + '&z=17&pll=' +
                            row.late6 / 1E6 + ',' + row.lnge6 / 1E6 + '">Intel link</a>' +
                            '<div class="iw-address">' + ada + '<p style="color: #cca844;">' + row.address + '</p></div>' +
                            '</div>' + '</div>';

                        google.maps.event.addListener(marker, 'click', (function(marker, cont) {
                            return function() {

                                infoWindow.setContent(cont);
                                infoWindow.open($scope.map, marker);
                                customFunction();
                            }
                        })(marker, cont));

                    });

                    var latlngbounds = new google.maps.LatLngBounds();

                    LatLngList.forEach(function(latLng) {
                        latlngbounds.extend(latLng);
                    });

                    $scope.map.setCenter(latlngbounds.getCenter());
                    $scope.map.fitBounds(latlngbounds);
                },
                dataType: "json"
            })
        }

    }])
    .controller('SettingsCtrl', ['$rootScope', '$scope', '$http', function($rootScope, $scope, $http) {
        $scope.$parent.title = "Settings";
        function initialize(late6, lnge6) {
            $scope.initData = true;
            var lat = 34.010550;
            var lng = -118.085861;
            var z = 10;

            var ingressGMapOptions = {
                backgroundColor: '#0e3d4e',
                styles: [{
                    featureType: "all",
                    elementType: "all",
                    stylers: [{
                        visibility: "on"
                    }, {
                        hue: "#131c1c"
                    }, {
                        saturation: "-50"
                    }, {
                        invert_lightness: true
                    }]
                }, {
                    featureType: "water",
                    elementType: "all",
                    stylers: [{
                        visibility: "on"
                    }, {
                        hue: "#005eff"
                    }, {
                        invert_lightness: true
                    }]
                }, {
                    featureType: "poi",
                    stylers: [{
                        visibility: "off"
                    }]
                }, {
                    featureType: "transit",
                    elementType: "all",
                    stylers: [{
                        visibility: "off"
                    }]
                }]
            };

            var e = new google.maps.LatLng(lat, lng),
                t = {
                    zoom: z,
                    center: e,
                    panControl: !0,
                    scrollwheel: 1,
                    scaleControl: !0,
                    overviewMapControl: !0,
                    overviewMapControlOptions: {
                        opened: !0
                    },
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    backgroundColor: '#0e3d4e',
                    styles: [{
                        featureType: "all",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }, {
                            hue: "#131c1c"
                        }, {
                            saturation: "-50"
                        }, {
                            invert_lightness: true
                        }]
                    }, {
                        featureType: "water",
                        elementType: "all",
                        stylers: [{
                            visibility: "on"
                        }, {
                            hue: "#005eff"
                        }, {
                            invert_lightness: true
                        }]
                    }, {
                        featureType: "poi",
                        stylers: [{
                            visibility: "off"
                        }]
                    }, {
                        featureType: "transit",
                        elementType: "all",
                        stylers: [{
                            visibility: "off"
                        }]
                    }],
                };

            $scope.map = new google.maps.Map(document.getElementById("latlongmap"), t),
                $scope.geocoder = new google.maps.Geocoder,
                $scope.marker = new google.maps.Marker({
                    position: e,
                    map: $scope.map
                }), google.maps.event.addListener($scope.map, "click", function(e) {
                    $scope.marker.setPosition(e.latLng);
                    var t = e.latLng,
                        o = "(" + t.lat().toFixed(6) + ", " + t.lng().toFixed(6) + ")";
                    lat = t.lat().toFixed(6);
                    lng = t.lng().toFixed(6);
                    storeMapPosition(lat, lng)
                })
        }
        $scope.showInventory = function(agent_id) {
            var request_inventory = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'inventory',
                    agent_id: agent_id
                })}).then(function (response) {
                $scope.showInventoryData = response.data.result.items[0].description;
                $scope.showInventoryData.agent_id = agent_id;

            }, function (response) {});
        };

        $scope.removeaccount = function(agent_name) {
            var request_inventory = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'account_remove',
                    agent_name: agent_name
                })}).then(function (response) {

                $scope.error = response.data.result.accounts.error;
                $rootScope.$broadcast('error', {'error': $scope.error});
                if (!$scope.error) {
                    $scope.showAccountsData = response.data.result.accounts;
                };

            }, function (response) {});
        };

        $scope.set_active = function(agent_id) {
            console.log(agent_id);
            var request_inventory = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'set_active',
                    agent_id: agent_id
                })}).then(function (response) {

                $scope.error = response.data.result.accounts.error;
                $rootScope.$broadcast('error', {'error': $scope.error});
                if (!$scope.error) {
                    $scope.showAccountsData = response.data.result.accounts;
                }

            }, function (response) {});
        };

        $scope.hideAchievements = function(agent_id) {
            var request_inventory = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'hide',
                    agent_id: agent_id
                })}).then(function (response) {

                $scope.error = response.data.result.accounts.error;
                $rootScope.$broadcast('error', {'error': $scope.error});
                if (!$scope.error) {
                    $scope.showAccountsData = response.data.result.accounts;
                };

            }, function (response) {});
        };

        $scope.addaccount = function(agent_name) {
            var request_accounts = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'add_account',
                    agent_name: agent_name
                })
            }).then(function(response) {
                $scope.error = response.data.result.accounts.error;
                $rootScope.$broadcast('error', {'error': $scope.error});
                if (!$scope.error) {
                    $scope.showAccountsData = response.data.result.accounts;
                };
            }, function(response) {});
        };

        $scope.getaccounts = function() {
            var request_accounts = $http({
                method: "post",
                url: "/api",
                data: JSON.stringify({
                    request: 'accounts',
                })
            }).then(function(response) {
                $scope.showAccountsData = response.data.result.accounts;
            }, function(response) {});
        };
        $scope.getaccounts();

        $scope.showInventoryOnMap = function getRportals(agent_id) {
            initialize();

            function customFunction() {
                var iwOuter = $('.gm-style-iw');
                var iwBackground = iwOuter.prev();

                iwBackground.children(':nth-child(1)').css({
                    'display': 'none'
                });
                iwBackground.children(':nth-child(2)').css({
                    'display': 'none'
                });
                iwBackground.children(':nth-child(3)').children(':nth-child(2)').children(':nth-child(1)').css({
                    'background-color': '#167'
                });
                iwBackground.children(':nth-child(3)').children(':nth-child(1)').children(':nth-child(1)').css({
                    'background-color': '#167'
                });

                iwBackground.children(':nth-child(4)').css({
                    'display': 'none'
                });

                var iwCloseBtn = iwOuter.next();

                iwCloseBtn.css({
                    opacity: '1',
                    right: '52px',
                    top: '17px'
                });
            };
            var infoWindow = new google.maps.InfoWindow(),
                marker;
            var LatLngList = [];
            $.ajax({
                type: "POST",
                url: '/api',
                data: JSON.stringify({
                    request: 'inventory',
                    agent_id: agent_id
                }),
                contentType: "application/json",

                success: function(response) {

                    response.result.items[0].description.portalKeys.forEach(function(row, i) {
                        LatLngList[i] = new google.maps.LatLng(row.portalLocation[0] / 1E6, row.portalLocation[1] / 1E6)
                        var marker = new google.maps.Marker({
                            position: new google.maps.LatLng(row.portalLocation[0] / 1E6, row.portalLocation[1] / 1E6),
                            map: $scope.map,
                            title: row.portalTitle,
//                            icon: {
//                                url: icn
//                            },
                        });


                        $scope.cont = '<div id="iw-container"><div class="iw-title"><span class="' + $scope.color_team +
                            '">' + row.portalTitle + '</span></div>' + '<div class="iw-content">' +
                            '<div class="iw-subTitle"><img src="' + row.portalImageUrl + '" alt="Portal name: ' + row.portalTitle +
                            '" width="83"><span style="color: #cca844;">Owner:</span> <span class="' +
                            $scope.color_team + '"></span></div><a target="_blank" href="https://www.ingress.com/intel?ll=' +
                            row.portalLocation[0] / 1E6 + ',' + row.portalLocation[1] / 1E6 + '&z=17&pll=' +
                            row.portalLocation[0] / 1E6 + ',' + row.portalLocation[1] / 1E6 + '">Intel link</a>' +
                            '<div class="iw-address"><p style="color: #cca844;">' +
                            row.portalAddress + '</p></div>' + '</div>' + '</div>';

                        google.maps.event.addListener(marker, 'click', (function(marker, cont) {
                            return function() {
                                infoWindow.setContent(cont);
                                infoWindow.open($scope.map, marker);
                                customFunction();
                            }
                        })(marker, $scope.cont));
                    });

                    var latlngbounds = new google.maps.LatLngBounds();

                    LatLngList.forEach(function(latLng) {
                        latlngbounds.extend(latLng);
                    });

                    $scope.map.setCenter(latlngbounds.getCenter());
                    $scope.map.fitBounds(latlngbounds);
                },
                dataType: "json"
            })
        }
    }])
    .controller('AboutCtrl', ['$scope', function($scope) {
        $scope.$parent.title = "About";
    }])
    .controller('InstrCtrl', ['$scope', function($scope) {
        $scope.$parent.title = "Instr";
    }])
    .controller('AppCtrl', ['$rootScope', '$scope', '$location', function($rootScope, $scope, $location) {
        $rootScope.error = null;
        $rootScope.$on('error', function (event, data) {
            $rootScope.error = data;
        });
        $scope.isActive = function(viewLocation) {
            return viewLocation === $location.path();
        };
    }])