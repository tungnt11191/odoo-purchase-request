/**
 * INSPINIA - Responsive Admin Theme
 *
 * Inspinia theme use AngularUI Router to manage routing and views
 * Each view are defined as state.
 * Initial there are written state for all view in theme.
 *
 */
function config($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, IdleProvider, KeepaliveProvider) {

    // Configure Idle settings
    IdleProvider.idle(5); // in seconds
    IdleProvider.timeout(120); // in seconds

    $urlRouterProvider.otherwise("/dashboards/dashboard_1");

    $ocLazyLoadProvider.config({
        // Set to true if you want to see what and when is dynamically loaded
        debug: false
    });

    $stateProvider

        .state('dashboards', {
            abstract: true,
            url: "/dashboards",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
        })
        .state('dashboards.dashboard_1', {
            url: "/dashboard_1",
            templateUrl: "/pos_self_order/static/assets/views/dashboard_1.html",
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {

                            serie: true,
                            name: 'angular-flot',
                            files: [ '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.time.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.tooltip.min.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.spline.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.resize.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.pie.js', '/pos_self_order/static/assets/js/plugins/flot/curvedLines.js', '/pos_self_order/static/assets/js/plugins/flot/angular-flot.js', ]
                        },
                        {
                            name: 'angles',
                            files: ['/pos_self_order/static/assets/js/plugins/chartJs/angles.js', '/pos_self_order/static/assets/js/plugins/chartJs/Chart.min.js']
                        },
                        {
                            name: 'angular-peity',
                            files: ['/pos_self_order/static/assets/js/plugins/peity/jquery.peity.min.js', '/pos_self_order/static/assets/js/plugins/peity/angular-peity.js']
                        }
                    ]);
                }
            }
        })
        .state('dashboards.dashboard_2', {
            url: "/dashboard_2",
            templateUrl: "/pos_self_order/static/assets/views/dashboard_2.html",
            data: { pageTitle: 'Dashboard 2' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            name: 'angular-flot',
                            files: [ '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.time.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.tooltip.min.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.spline.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.resize.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.pie.js', '/pos_self_order/static/assets/js/plugins/flot/curvedLines.js', '/pos_self_order/static/assets/js/plugins/flot/angular-flot.js' ]
                        },
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/jvectormap/jquery-jvectormap-2.0.2.min.js', '/pos_self_order/static/assets/js/plugins/jvectormap/jquery-jvectormap-2.0.2.css']
                        },
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/jvectormap/jquery-jvectormap-world-mill-en.js']
                        },
                        {
                            name: 'ui.checkbox',
                            files: ['/pos_self_order/static/assets/bootstrap/angular-bootstrap-checkbox.js']
                        }
                    ]);
                }
            }
        })
        .state('dashboards.dashboard_3', {
            url: "/dashboard_3",
            templateUrl: "/pos_self_order/static/assets/views/dashboard_3.html",
            data: { pageTitle: 'Dashboard 3' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'angles',
                            files: ['/pos_self_order/static/assets/js/plugins/chartJs/angles.js', '/pos_self_order/static/assets/js/plugins/chartJs/Chart.min.js']
                        },
                        {
                            name: 'angular-peity',
                            files: ['/pos_self_order/static/assets/js/plugins/peity/jquery.peity.min.js', '/pos_self_order/static/assets/js/plugins/peity/angular-peity.js']
                        },
                        {
                            name: 'ui.checkbox',
                            files: ['/pos_self_order/static/assets/bootstrap/angular-bootstrap-checkbox.js']
                        }
                    ]);
                }
            }
        })
        .state('dashboards_top', {
            abstract: true,
            url: "/dashboards_top",
            templateUrl: "/pos_self_order/static/assets/views/common/content_top_navigation.html",
        })
        .state('dashboards_top.dashboard_4', {
            url: "/dashboard_4",
            templateUrl: "/pos_self_order/static/assets/views/dashboard_4.html",
            data: { pageTitle: 'Dashboard 4' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'angles',
                            files: ['/pos_self_order/static/assets/js/plugins/chartJs/angles.js', '/pos_self_order/static/assets/js/plugins/chartJs/Chart.min.js']
                        },
                        {
                            name: 'angular-peity',
                            files: ['/pos_self_order/static/assets/js/plugins/peity/jquery.peity.min.js', '/pos_self_order/static/assets/js/plugins/peity/angular-peity.js']
                        },
                        {
                            serie: true,
                            name: 'angular-flot',
                            files: [ '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.time.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.tooltip.min.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.spline.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.resize.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.pie.js', '/pos_self_order/static/assets/js/plugins/flot/curvedLines.js', '/pos_self_order/static/assets/js/plugins/flot/angular-flot.js', ]
                        }
                    ]);
                }
            }
        })
        .state('dashboards.dashboard_4_1', {
            url: "/dashboard_4_1",
            templateUrl: "/pos_self_order/static/assets/views/dashboard_4_1.html",
            data: { pageTitle: 'Dashboard 4' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'angles',
                            files: ['/pos_self_order/static/assets/js/plugins/chartJs/angles.js', '/pos_self_order/static/assets/js/plugins/chartJs/Chart.min.js']
                        },
                        {
                            name: 'angular-peity',
                            files: ['/pos_self_order/static/assets/js/plugins/peity/jquery.peity.min.js', '/pos_self_order/static/assets/js/plugins/peity/angular-peity.js']
                        },
                        {
                            serie: true,
                            name: 'angular-flot',
                            files: [ '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.time.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.tooltip.min.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.spline.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.resize.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.pie.js', '/pos_self_order/static/assets/js/plugins/flot/curvedLines.js', '/pos_self_order/static/assets/js/plugins/flot/angular-flot.js', ]
                        }
                    ]);
                }
            }
        })
        .state('dashboards.dashboard_5', {
            url: "/dashboard_5",
            templateUrl: "/pos_self_order/static/assets/views/dashboard_5.html",
            data: { pageTitle: 'Dashboard 5' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            name: 'angular-flot',
                            files: [ '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.time.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.tooltip.min.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.spline.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.resize.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.pie.js', '/pos_self_order/static/assets/js/plugins/flot/curvedLines.js', '/pos_self_order/static/assets/js/plugins/flot/angular-flot.js', ]
                        },
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/sparkline/jquery.sparkline.min.js']
                        }
                    ]);
                }
            }
        })
        .state('layouts', {
            url: "/layouts",
            templateUrl: "/pos_self_order/static/assets/views/layouts.html",
            data: { pageTitle: 'Layouts' },
        })
        .state('charts', {
            abstract: true,
            url: "/charts",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
        })
        .state('charts.flot_chart', {
            url: "/flot_chart",
            templateUrl: "/pos_self_order/static/assets/views/graph_flot.html",
            data: { pageTitle: 'Flot chart' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            name: 'angular-flot',
                            files: [ '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.time.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.tooltip.min.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.spline.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.resize.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.pie.js', '/pos_self_order/static/assets/js/plugins/flot/curvedLines.js', '/pos_self_order/static/assets/js/plugins/flot/angular-flot.js', ]
                        }
                    ]);
                }
            }
        })
        .state('charts.rickshaw_chart', {
            url: "/rickshaw_chart",
            templateUrl: "/pos_self_order/static/assets/views/graph_rickshaw.html",
            data: { pageTitle: 'Rickshaw chart' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            reconfig: true,
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/rickshaw/vendor/d3.v3.js','/pos_self_order/static/assets/js/plugins/rickshaw/rickshaw.min.js']
                        },
                        {
                            reconfig: true,
                            name: 'angular-rickshaw',
                            files: ['/pos_self_order/static/assets/js/plugins/rickshaw/angular-rickshaw.js']
                        }
                    ]);
                }
            }
        })
        .state('charts.peity_chart', {
            url: "/peity_chart",
            templateUrl: "/pos_self_order/static/assets/views/graph_peity.html",
            data: { pageTitle: 'Peity graphs' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'angular-peity',
                            files: ['/pos_self_order/static/assets/js/plugins/peity/jquery.peity.min.js', '/pos_self_order/static/assets/js/plugins/peity/angular-peity.js']
                        }
                    ]);
                }
            }
        })
        .state('charts.sparkline_chart', {
            url: "/sparkline_chart",
            templateUrl: "/pos_self_order/static/assets/views/graph_sparkline.html",
            data: { pageTitle: 'Sparkline chart' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/sparkline/jquery.sparkline.min.js']
                        }
                    ]);
                }
            }
        })
        .state('charts.chartjs_chart', {
            url: "/chartjs_chart",
            templateUrl: "/pos_self_order/static/assets/views/chartjs.html",
            data: { pageTitle: 'Chart.js' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/chartJs/Chart.min.js']
                        },
                        {
                            name: 'angles',
                            files: ['/pos_self_order/static/assets/js/plugins/chartJs/angles.js']
                        }
                    ]);
                }
            }
        })
        .state('charts.chartist_chart', {
            url: "/chartist_chart",
            templateUrl: "/pos_self_order/static/assets/views/chartist.html",
            data: { pageTitle: 'Chartist' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            name: 'angular-chartist',
                            files: ['/pos_self_order/static/assets/js/plugins/chartist/chartist.min.js', '/pos_self_order/static/assets/css/plugins/chartist/chartist.min.css', '/pos_self_order/static/assets/js/plugins/chartist/angular-chartist.min.js']
                        }
                    ]);
                }
            }
        })
        .state('charts.c3charts', {
            url: "/c3charts",
            templateUrl: "/pos_self_order/static/assets/views/c3charts.html",
            data: { pageTitle: 'c3charts' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/css/plugins/c3/c3.min.css', '/pos_self_order/static/assets/js/plugins/d3/d3.min.js', '/pos_self_order/static/assets/js/plugins/c3/c3.min.js']
                        },
                        {
                            serie: true,
                            name: 'gridshore.c3js.chart',
                            files: ['/pos_self_order/static/assets/js/plugins/c3/c3-angular.min.js']
                        }
                    ]);
                }
            }
        })
        .state('mailbox', {
            abstract: true,
            url: "/mailbox",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
        })
        .state('mailbox.inbox', {
            url: "/inbox",
            templateUrl: "/pos_self_order/static/assets/views/mailbox.html",
            data: { pageTitle: 'Mail Inbox' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/iCheck/custom.css','/pos_self_order/static/assets/js/plugins/iCheck/icheck.min.js']
                        }
                    ]);
                }
            }
        })
        .state('mailbox.email_view', {
            url: "/email_view",
            templateUrl: "/pos_self_order/static/assets/views/mail_detail.html",
            data: { pageTitle: 'Mail detail' }
        })
        .state('mailbox.email_compose', {
            url: "/email_compose",
            templateUrl: "/pos_self_order/static/assets/views/mail_compose.html",
            data: { pageTitle: 'Mail compose' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/summernote/summernote.css','/pos_self_order/static/assets/css/plugins/summernote/summernote-bs3.css','/pos_self_order/static/assets/js/plugins/summernote/summernote.min.js']
                        },
                        {
                            name: 'summernote',
                            files: ['/pos_self_order/static/assets/css/plugins/summernote/summernote.css','/pos_self_order/static/assets/css/plugins/summernote/summernote-bs3.css','/pos_self_order/static/assets/js/plugins/summernote/summernote.min.js','/pos_self_order/static/assets/js/plugins/summernote/angular-summernote.min.js']
                        }
                    ]);
                }
            }
        })
        .state('mailbox.email_template', {
            url: "/email_template",
            templateUrl: "/pos_self_order/static/assets/views/email_template.html",
            data: { pageTitle: 'Mail compose' }
        })
        .state('widgets', {
            url: "/widgets",
            templateUrl: "/pos_self_order/static/assets/views/widgets.html",
            data: { pageTitle: 'Widhets' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            name: 'angular-flot',
                            files: [ '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.time.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.tooltip.min.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.spline.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.resize.js', '/pos_self_order/static/assets/js/plugins/flot/jquery.flot.pie.js', '/pos_self_order/static/assets/js/plugins/flot/curvedLines.js', '/pos_self_order/static/assets/js/plugins/flot/angular-flot.js', ]
                        },
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/iCheck/custom.css','/pos_self_order/static/assets/js/plugins/iCheck/icheck.min.js']
                        },
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/jvectormap/jquery-jvectormap-2.0.2.min.js', '/pos_self_order/static/assets/js/plugins/jvectormap/jquery-jvectormap-2.0.2.css']
                        },
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/jvectormap/jquery-jvectormap-world-mill-en.js']
                        },
                        {
                            name: 'ui.checkbox',
                            files: ['/pos_self_order/static/assets/bootstrap/angular-bootstrap-checkbox.js']
                        }
                    ]);
                }
            }
        })
        .state('metrics', {
            url: "/metrics",
            templateUrl: "/pos_self_order/static/assets/views/metrics.html",
            data: { pageTitle: 'Metrics' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/sparkline/jquery.sparkline.min.js']
                        }
                    ]);
                }
            }
        })
        .state('forms', {
            abstract: true,
            url: "/forms",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
        })
        .state('forms.basic_form', {
            url: "/basic_form",
            templateUrl: "/pos_self_order/static/assets/views/form_basic.html",
            data: { pageTitle: 'Basic form' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/iCheck/custom.css','/pos_self_order/static/assets/js/plugins/iCheck/icheck.min.js']
                        }
                    ]);
                }
            }
        })
        .state('forms.advanced_plugins', {
            url: "/advanced_plugins",
            templateUrl: "/pos_self_order/static/assets/views/form_advanced.html",
            data: { pageTitle: 'Advanced form' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/moment/moment.min.js']
                        },
                        {
                            name: 'ui.knob',
                            files: ['/pos_self_order/static/assets/js/plugins/jsKnob/jquery.knob.js','/pos_self_order/static/assets/js/plugins/jsKnob/angular-knob.js']
                        },
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/ionRangeSlider/ion.rangeSlider.css','/pos_self_order/static/assets/css/plugins/ionRangeSlider/ion.rangeSlider.skinFlat.css','/pos_self_order/static/assets/js/plugins/ionRangeSlider/ion.rangeSlider.min.js']
                        },
                        {
                            insertBefore: '#loadBefore',
                            name: 'localytics.directives',
                            files: ['/pos_self_order/static/assets/css/plugins/chosen/bootstrap-chosen.css','/pos_self_order/static/assets/js/plugins/chosen/chosen.jquery.js','/pos_self_order/static/assets/js/plugins/chosen/chosen.js']
                        },
                        {
                            name: 'nouislider',
                            files: ['/pos_self_order/static/assets/css/plugins/nouslider/jquery.nouislider.css','/pos_self_order/static/assets/js/plugins/nouslider/jquery.nouislider.min.js','/pos_self_order/static/assets/js/plugins/nouslider/angular-nouislider.js']
                        },
                        {
                            name: 'datePicker',
                            files: ['/pos_self_order/static/assets/css/plugins/datapicker/angular-datapicker.css','/pos_self_order/static/assets/js/plugins/datapicker/angular-datepicker.js']
                        },
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/jasny/jasny-bootstrap.min.js']
                        },
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/clockpicker/clockpicker.css', '/pos_self_order/static/assets/js/plugins/clockpicker/clockpicker.js']
                        },
                        {
                            name: 'ui.switchery',
                            files: ['/pos_self_order/static/assets/css/plugins/switchery/switchery.css','/pos_self_order/static/assets/js/plugins/switchery/switchery.js','/pos_self_order/static/assets/js/plugins/switchery/ng-switchery.js']
                        },
                        {
                            name: 'colorpicker.module',
                            files: ['/pos_self_order/static/assets/css/plugins/colorpicker/colorpicker.css','/pos_self_order/static/assets/js/plugins/colorpicker/bootstrap-colorpicker-module.js']
                        },
                        {
                            name: 'ngImgCrop',
                            files: ['/pos_self_order/static/assets/js/plugins/ngImgCrop/ng-img-crop.js','/pos_self_order/static/assets/css/plugins/ngImgCrop/ng-img-crop.css']
                        },
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/daterangepicker/daterangepicker.js', '/pos_self_order/static/assets/css/plugins/daterangepicker/daterangepicker-bs3.css']
                        },
                        {
                            name: 'daterangepicker',
                            files: ['/pos_self_order/static/assets/js/plugins/daterangepicker/angular-daterangepicker.js']
                        },
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/awesome-bootstrap-checkbox/awesome-bootstrap-checkbox.css']
                        },
                        {
                            name: 'ui.select',
                            files: ['/pos_self_order/static/assets/js/plugins/ui-select/select.min.js', '/pos_self_order/static/assets/css/plugins/ui-select/select.min.css']
                        },
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/touchspin/jquery.bootstrap-touchspin.min.css', '/pos_self_order/static/assets/js/plugins/touchspin/jquery.bootstrap-touchspin.min.js']
                        },
                        {
                            name: 'ngTagsInput',
                            files: ['/pos_self_order/static/assets/js/plugins/ngTags//ng-tags-input.min.js', '/pos_self_order/static/assets/css/plugins/ngTags/ng-tags-input-custom.min.css']
                        },
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/dualListbox/jquery.bootstrap-duallistbox.js','/pos_self_order/static/assets/css/plugins/dualListbox/bootstrap-duallistbox.min.css']
                        },
                        {
                            name: 'frapontillo.bootstrap-duallistbox',
                            files: ['/pos_self_order/static/assets/js/plugins/dualListbox/angular-bootstrap-duallistbox.js']
                        }

                    ]);
                }
            }
        })
        .state('forms.wizard', {
            url: "/wizard",
            templateUrl: "/pos_self_order/static/assets/views/form_wizard.html",
            controller: wizardCtrl,
            data: { pageTitle: 'Wizard form' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/steps/jquery.steps.css']
                        }
                    ]);
                }
            }
        })
        .state('forms.wizard.step_one', {
            url: '/step_one',
            templateUrl: '/pos_self_order/static/assets/views/wizard/step_one.html',
            data: { pageTitle: 'Wizard form' }
        })
        .state('forms.wizard.step_two', {
            url: '/step_two',
            templateUrl: '/pos_self_order/static/assets/views/wizard/step_two.html',
            data: { pageTitle: 'Wizard form' }
        })
        .state('forms.wizard.step_three', {
            url: '/step_three',
            templateUrl: '/pos_self_order/static/assets/views/wizard/step_three.html',
            data: { pageTitle: 'Wizard form' }
        })
        .state('forms.file_upload', {
            url: "/file_upload",
            templateUrl: "/pos_self_order/static/assets/views/form_file_upload.html",
            data: { pageTitle: 'File upload' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/dropzone/basic.css','/pos_self_order/static/assets/css/plugins/dropzone/dropzone.css','/pos_self_order/static/assets/js/plugins/dropzone/dropzone.js']
                        },
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/jasny/jasny-bootstrap.min.js', '/pos_self_order/static/assets/css/plugins/jasny/jasny-bootstrap.min.css' ]
                        }
                    ]);
                }
            }
        })
        .state('forms.text_editor', {
            url: "/text_editor",
            templateUrl: "/pos_self_order/static/assets/views/form_editors.html",
            data: { pageTitle: 'Text editor' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'summernote',
                            files: ['/pos_self_order/static/assets/css/plugins/summernote/summernote.css','/pos_self_order/static/assets/css/plugins/summernote/summernote-bs3.css','/pos_self_order/static/assets/js/plugins/summernote/summernote.min.js','/pos_self_order/static/assets/js/plugins/summernote/angular-summernote.min.js']
                        }
                    ]);
                }
            }
        })
        .state('forms.autocomplete', {
            url: "/autocomplete",
            templateUrl: "/pos_self_order/static/assets/views/autocomplete.html",
            data: { pageTitle: 'Autocomplete' }

        })
        .state('forms.markdown', {
            url: "/markdown",
            templateUrl: "/pos_self_order/static/assets/views/markdown.html",
            data: { pageTitle: 'Markdown' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/bootstrap-markdown/bootstrap-markdown.js','/pos_self_order/static/assets/js/plugins/bootstrap-markdown/markdown.js','/pos_self_order/static/assets/css/plugins/bootstrap-markdown/bootstrap-markdown.min.css']
                        }
                    ]);
                }
            }
        })
        .state('app', {
            abstract: true,
            url: "/app",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
        })
        .state('app.contacts', {
            url: "/contacts",
            templateUrl: "/pos_self_order/static/assets/views/contacts.html",
            data: { pageTitle: 'Contacts' }
        })
        .state('app.contacts_2', {
            url: "/contacts_2",
            templateUrl: "/pos_self_order/static/assets/views/contacts_2.html",
            data: { pageTitle: 'Contacts 2' }
        })
        .state('app.profile', {
            url: "/profile",
            templateUrl: "/pos_self_order/static/assets/views/profile.html",
            data: { pageTitle: 'Profile' }
        })
        .state('app.profile_2', {
            url: "/profile_2",
            templateUrl: "/pos_self_order/static/assets/views/profile_2.html",
            data: { pageTitle: 'Profile_2'},
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/sparkline/jquery.sparkline.min.js']
                        }
                    ]);
                }
            }
        })
        .state('app.projects', {
            url: "/projects",
            templateUrl: "/pos_self_order/static/assets/views/projects.html",
            data: { pageTitle: 'Projects' }
        })
        .state('app.project_detail', {
            url: "/project_detail",
            templateUrl: "/pos_self_order/static/assets/views/project_detail.html",
            data: { pageTitle: 'Project detail' }
        })
        .state('app.activity_stream', {
            url: "/activity_stream",
            templateUrl: "/pos_self_order/static/assets/views/activity_stream.html",
            data: { pageTitle: 'Activity stream' }
        })
        .state('app.file_manager', {
            url: "/file_manager",
            templateUrl: "/pos_self_order/static/assets/views/file_manager.html",
            data: { pageTitle: 'File manager' }
        })
        .state('app.calendar', {
            url: "/calendar",
            templateUrl: "/pos_self_order/static/assets/views/calendar.html",
            data: { pageTitle: 'Calendar' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            insertBefore: '#loadBefore',
                            files: ['/pos_self_order/static/assets/css/plugins/fullcalendar/fullcalendar.css','/pos_self_order/static/assets/js/plugins/fullcalendar/fullcalendar.min.js','/pos_self_order/static/assets/js/plugins/fullcalendar/gcal.js']
                        },
                        {
                            name: 'ui.calendar',
                            files: ['/pos_self_order/static/assets/js/plugins/fullcalendar/calendar.js']
                        }
                    ]);
                }
            }
        })
        .state('app.faq', {
            url: "/faq",
            templateUrl: "/pos_self_order/static/assets/views/faq.html",
            data: { pageTitle: 'FAQ' }
        })
        .state('app.timeline', {
            url: "/timeline",
            templateUrl: "/pos_self_order/static/assets/views/timeline.html",
            data: { pageTitle: 'Timeline' }
        })
        .state('app.pin_board', {
            url: "/pin_board",
            templateUrl: "/pos_self_order/static/assets/views/pin_board.html",
            data: { pageTitle: 'Pin board' }
        })
        .state('app.invoice', {
            url: "/invoice",
            templateUrl: "/pos_self_order/static/assets/views/invoice.html",
            data: { pageTitle: 'Invoice' }
        })
        .state('app.blog', {
            url: "/blog",
            templateUrl: "/pos_self_order/static/assets/views/blog.html",
            data: { pageTitle: 'Blog' }
        })
        .state('app.article', {
            url: "/article",
            templateUrl: "/pos_self_order/static/assets/views/article.html",
            data: { pageTitle: 'Article' }
        })
        .state('app.issue_tracker', {
            url: "/issue_tracker",
            templateUrl: "/pos_self_order/static/assets/views/issue_tracker.html",
            data: { pageTitle: 'Issue Tracker' }
        })
        .state('app.clients', {
            url: "/clients",
            templateUrl: "/pos_self_order/static/assets/views/clients.html",
            data: { pageTitle: 'Clients' }
        })
        .state('app.teams_board', {
            url: "/teams_board",
            templateUrl: "/pos_self_order/static/assets/views/teams_board.html",
            data: { pageTitle: 'Teams board' }
        })
        .state('app.social_feed', {
            url: "/social_feed",
            templateUrl: "/pos_self_order/static/assets/views/social_feed.html",
            data: { pageTitle: 'Social feed' }
        })
        .state('app.vote_list', {
            url: "/vote_list",
            templateUrl: "/pos_self_order/static/assets/views/vote_list.html",
            data: { pageTitle: 'Vote list' }
        })
        .state('pages', {
            abstract: true,
            url: "/pages",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html"
        })
        .state('pages.search_results', {
            url: "/search_results",
            templateUrl: "/pos_self_order/static/assets/views/search_results.html",
            data: { pageTitle: 'Search results' }
        })
        .state('pages.empy_page', {
            url: "/empy_page",
            templateUrl: "/pos_self_order/static/assets/views/empty_page.html",
            data: { pageTitle: 'Empty page' }
        })
        .state('logins', {
            url: "/logins",
            templateUrl: "/pos_self_order/static/assets/views/login.html",
            data: { pageTitle: 'Login', specialClass: 'gray-bg' }
        })
        .state('login_two_columns', {
            url: "/login_two_columns",
            templateUrl: "/pos_self_order/static/assets/views/login_two_columns.html",
            data: { pageTitle: 'Login two columns', specialClass: 'gray-bg' }
        })
        .state('register', {
            url: "/register",
            templateUrl: "/pos_self_order/static/assets/views/register.html",
            data: { pageTitle: 'Register', specialClass: 'gray-bg' }
        })
        .state('lockscreen', {
            url: "/lockscreen",
            templateUrl: "/pos_self_order/static/assets/views/lockscreen.html",
            data: { pageTitle: 'Lockscreen', specialClass: 'gray-bg' }
        })
        .state('forgot_password', {
            url: "/forgot_password",
            templateUrl: "/pos_self_order/static/assets/views/forgot_password.html",
            data: { pageTitle: 'Forgot password', specialClass: 'gray-bg' }
        })
        .state('errorOne', {
            url: "/errorOne",
            templateUrl: "/pos_self_order/static/assets/views/errorOne.html",
            data: { pageTitle: '404', specialClass: 'gray-bg' }
        })
        .state('errorTwo', {
            url: "/errorTwo",
            templateUrl: "/pos_self_order/static/assets/views/errorTwo.html",
            data: { pageTitle: '500', specialClass: 'gray-bg' }
        })
        .state('ui', {
            abstract: true,
            url: "/ui",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
        })
        .state('ui.typography', {
            url: "/typography",
            templateUrl: "/pos_self_order/static/assets/views/typography.html",
            data: { pageTitle: 'Typography' }
        })
        .state('ui.icons', {
            url: "/icons",
            templateUrl: "/pos_self_order/static/assets/views/icons.html",
            data: { pageTitle: 'Icons' }
        })
        .state('ui.buttons', {
            url: "/buttons",
            templateUrl: "/pos_self_order/static/assets/views/buttons.html",
            data: { pageTitle: 'Buttons' }
        })
        .state('ui.tabs_panels', {
            url: "/tabs_panels",
            templateUrl: "/pos_self_order/static/assets/views/tabs_panels.html",
            data: { pageTitle: 'Panels' }
        })
        .state('ui.tabs', {
            url: "/tabs",
            templateUrl: "/pos_self_order/static/assets/views/tabs.html",
            data: { pageTitle: 'Tabs' }
        })
        .state('ui.notifications_tooltips', {
            url: "/notifications_tooltips",
            templateUrl: "/pos_self_order/static/assets/views/notifications.html",
            data: { pageTitle: 'Notifications and tooltips' }
        })
        .state('ui.helper_classes', {
            url: "/helper_classes",
            templateUrl: "/pos_self_order/static/assets/views/helper_classes.html",
            data: { pageTitle: 'Helper css classes' }
        })
        .state('ui.badges_labels', {
            url: "/badges_labels",
            templateUrl: "/pos_self_order/static/assets/views/badges_labels.html",
            data: { pageTitle: 'Badges and labels and progress' }
        })
        .state('ui.video', {
            url: "/video",
            templateUrl: "/pos_self_order/static/assets/views/video.html",
            data: { pageTitle: 'Responsible Video' }
        })
        .state('ui.draggable', {
            url: "/draggable",
            templateUrl: "/pos_self_order/static/assets/views/draggable.html",
            data: { pageTitle: 'Draggable panels' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'ui.sortable',
                            files: ['/pos_self_order/static/assets/js/plugins/ui-sortable/sortable.js']
                        }
                    ]);
                }
            }
        })
        .state('grid_optionss', {
            url: "/grid_options",
            templateUrl: "/pos_self_order/static/assets/views/grid_options.html",
            data: { pageTitle: 'Grid options' }
        })
        .state('miscellaneous', {
            abstract: true,
            url: "/miscellaneous",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
        })
        .state('miscellaneous.google_maps', {
            url: "/google_maps",
            templateUrl: "/pos_self_order/static/assets/views/google_maps.html",
            data: { pageTitle: 'Google maps' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'ui.event',
                            files: ['/pos_self_order/static/assets/js/plugins/uievents/event.js']
                        },
                        {
                            name: 'ui.map',
                            files: ['/pos_self_order/static/assets/js/plugins/uimaps/ui-map.js']
                        },
                    ]);
                }
            }
        })
        .state('miscellaneous.datamaps', {
            url: "/datamaps",
            templateUrl: "/pos_self_order/static/assets/views/datamaps.html",
            data: { pageTitle: 'Datamaps' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/d3/d3.min.js','/pos_self_order/static/assets/js/plugins/topojson/topojson.js','/pos_self_order/static/assets/js/plugins/datamaps/datamaps.all.min.js']
                        },
                        {
                            name: 'datamaps',
                            files: ['/pos_self_order/static/assets/js/plugins/angular-datamaps/angular-datamaps.min.js']
                        },
                    ]);
                }
            }
        })
        .state('miscellaneous.socialbuttons', {
            url: "/socialbuttons",
            templateUrl: "/pos_self_order/static/assets/views/socialbuttons.html",
            data: { pageTitle: 'Social buttons' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/bootstrapSocial/bootstrap-social.css']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.code_editor', {
            url: "/code_editor",
            templateUrl: "/pos_self_order/static/assets/views/code_editor.html",
            data: { pageTitle: 'Code Editor' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/css/plugins/codemirror/codemirror.css','/pos_self_order/static/assets/css/plugins/codemirror/ambiance.css','/pos_self_order/static/assets/js/plugins/codemirror/codemirror.js','/pos_self_order/static/assets/js/plugins/codemirror/mode/javascript/javascript.js']
                        },
                        {
                            name: 'ui.codemirror',
                            files: ['/pos_self_order/static/assets/js/plugins/ui-codemirror/ui-codemirror.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.modal_window', {
            url: "/modal_window",
            templateUrl: "/pos_self_order/static/assets/views/modal_window.html",
            data: { pageTitle: 'Modal window' }
        })
        .state('miscellaneous.chat_view', {
            url: "/chat_view",
            templateUrl: "/pos_self_order/static/assets/views/chat_view.html",
            data: { pageTitle: 'Chat view' }
        })
        .state('miscellaneous.nestable_list', {
            url: "/nestable_list",
            templateUrl: "/pos_self_order/static/assets/views/nestable_list.html",
            data: { pageTitle: 'Nestable List' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'ui.tree',
                            files: ['/pos_self_order/static/assets/css/plugins/uiTree/angular-ui-tree.min.css','/pos_self_order/static/assets/js/plugins/uiTree/angular-ui-tree.min.js']
                        },
                    ]);
                }
            }
        })
        .state('miscellaneous.notify', {
            url: "/notify",
            templateUrl: "/pos_self_order/static/assets/views/notify.html",
            data: { pageTitle: 'Notifications for angularJS' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'cgNotify',
                            files: ['/pos_self_order/static/assets/css/plugins/angular-notify/angular-notify.min.css','/pos_self_order/static/assets/js/plugins/angular-notify/angular-notify.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.timeline_2', {
            url: "/timeline_2",
            templateUrl: "/pos_self_order/static/assets/views/timeline_2.html",
            data: { pageTitle: 'Timeline version 2' }
        })
        .state('miscellaneous.forum_view', {
            url: "/forum_view",
            templateUrl: "/pos_self_order/static/assets/views/forum_view.html",
            data: { pageTitle: 'Forum - general view' }
        })
        .state('miscellaneous.forum_post_view', {
            url: "/forum_post_view",
            templateUrl: "/pos_self_order/static/assets/views/forum_post_view.html",
            data: { pageTitle: 'Forum - post view' }
        })
        .state('miscellaneous.diff', {
            url: "/diff",
            templateUrl: "/pos_self_order/static/assets/views/diff.html",
            data: { pageTitle: 'Text Diff' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/diff_match_patch/javascript/diff_match_patch.js']
                        },
                        {
                            name: 'diff-match-patch',
                            files: ['/pos_self_order/static/assets/js/plugins/angular-diff-match-patch/angular-diff-match-patch.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.pdf_viewer', {
            url: "/pdf_viewer",
            templateUrl: "/pos_self_order/static/assets/views/pdf_viewer.html",
            data: { pageTitle: 'PDF viewer' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/pdfjs/pdf.js']
                        },
                        {
                            name: 'pdf',
                            files: ['/pos_self_order/static/assets/js/plugins/pdfjs/angular-pdf.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.sweet_alert', {
            url: "/sweet_alert",
            templateUrl: "/pos_self_order/static/assets/views/sweet_alert.html",
            data: { pageTitle: 'Sweet alert' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/sweetalert/sweetalert.min.js', '/pos_self_order/static/assets/css/plugins/sweetalert/sweetalert.css']
                        },
                        {
                            name: 'oitozero.ngSweetAlert',
                            files: ['/pos_self_order/static/assets/js/plugins/sweetalert/angular-sweetalert.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.idle_timer', {
            url: "/idle_timer",
            templateUrl: "/pos_self_order/static/assets/views/idle_timer.html",
            data: { pageTitle: 'Idle timer' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'cgNotify',
                            files: ['/pos_self_order/static/assets/css/plugins/angular-notify/angular-notify.min.css','/pos_self_order/static/assets/js/plugins/angular-notify/angular-notify.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.live_favicon', {
            url: "/live_favicon",
            templateUrl: "/pos_self_order/static/assets/views/live_favicon.html",
            data: { pageTitle: 'Live favicon' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/tinycon/tinycon.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.spinners', {
            url: "/spinners",
            templateUrl: "/pos_self_order/static/assets/views/spinners.html",
            data: { pageTitle: 'Spinners' }
        })
        .state('miscellaneous.spinners_usage', {
            url: "/spinners_usage",
            templateUrl: "/pos_self_order/static/assets/views/spinners_usage.html",
            data: { pageTitle: 'Spinners usage' }
        })
        .state('miscellaneous.validation', {
            url: "/validation",
            templateUrl: "/pos_self_order/static/assets/views/validation.html",
            data: { pageTitle: 'Validation' }
        })
        .state('miscellaneous.agile_board', {
            url: "/agile_board",
            templateUrl: "/pos_self_order/static/assets/views/agile_board.html",
            data: { pageTitle: 'Agile board' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'ui.sortable',
                            files: ['/pos_self_order/static/assets/js/plugins/ui-sortable/sortable.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.masonry', {
            url: "/masonry",
            templateUrl: "/pos_self_order/static/assets/views/masonry.html",
            data: { pageTitle: 'Masonry' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/masonry/masonry.pkgd.min.js']
                        },
                        {
                            name: 'wu.masonry',
                            files: ['/pos_self_order/static/assets/js/plugins/masonry/angular-masonry.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.toastr', {
            url: "/toastr",
            templateUrl: "/pos_self_order/static/assets/views/toastr.html",
            data: { pageTitle: 'Toastr' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            insertBefore: '#loadBefore',
                            name: 'toaster',
                            files: ['/pos_self_order/static/assets/js/plugins/toastr/toastr.min.js', '/pos_self_order/static/assets/css/plugins/toastr/toastr.min.css']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.i18support', {
            url: "/i18support",
            templateUrl: "/pos_self_order/static/assets/views/i18support.html",
            data: { pageTitle: 'i18support' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            insertBefore: '#loadBefore',
                            name: 'toaster',
                            files: ['/pos_self_order/static/assets/js/plugins/toastr/toastr.min.js', '/pos_self_order/static/assets/css/plugins/toastr/toastr.min.css']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.truncate', {
            url: "/truncate",
            templateUrl: "/pos_self_order/static/assets/views/truncate.html",
            data: { pageTitle: 'Truncate' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/dotdotdot/jquery.dotdotdot.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.password_meter', {
            url: "/password_meter",
            templateUrl: "/pos_self_order/static/assets/views/password_meter.html",
            data: { pageTitle: 'Password meter' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/pwstrength/pwstrength-bootstrap.min.js', '/pos_self_order/static/assets/js/plugins/pwstrength/zxcvbn.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.clipboard', {
            url: "/clipboard",
            templateUrl: "/pos_self_order/static/assets/views/clipboard.html",
            data: { pageTitle: 'Clipboard' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/ngclipboard/clipboard.min.js']
                        },
                        {
                            name: 'ngclipboard',
                            files: ['/pos_self_order/static/assets/js/plugins/ngclipboard/ngclipboard.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.text_spinners', {
            url: "/text_spinners",
            templateUrl: "/pos_self_order/static/assets/views/text_spinners.html",
            data: { pageTitle: 'Text spinners' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/textSpinners/spinners.css']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.loading_buttons', {
            url: "/loading_buttons",
            templateUrl: "/pos_self_order/static/assets/views/loading_buttons.html",
            data: { pageTitle: 'Loading buttons' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            name: 'angular-ladda',
                            files: ['/pos_self_order/static/assets/js/plugins/ladda/spin.min.js', '/pos_self_order/static/assets/js/plugins/ladda/ladda.min.js', '/pos_self_order/static/assets/css/plugins/ladda/ladda-themeless.min.css','/pos_self_order/static/assets/js/plugins/ladda/angular-ladda.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.tour', {
            url: "/tour",
            templateUrl: "/pos_self_order/static/assets/views/tour.html",
            data: { pageTitle: 'Tour' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            insertBefore: '#loadBefore',
                            files: ['/pos_self_order/static/assets/js/plugins/bootstrap-tour/bootstrap-tour.min.js', '/pos_self_order/static/assets/css/plugins/bootstrap-tour/bootstrap-tour.min.css']
                        },
                        {
                            name: 'bm.bsTour',
                            files: ['/pos_self_order/static/assets/js/plugins/angular-bootstrap-tour/angular-bootstrap-tour.min.js']
                        }
                    ]);
                }
            }
        })
        .state('miscellaneous.tree_view', {
            url: "/tree_view",
            templateUrl: "/pos_self_order/static/assets/views/tree_view.html",
            data: { pageTitle: 'Tree view' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/jsTree/style.min.css','/pos_self_order/static/assets/js/plugins/jsTree/jstree.min.js']
                        },
                        {
                            name: 'ngJsTree',
                            files: ['/pos_self_order/static/assets/js/plugins/jsTree/ngJsTree.min.js']
                        }
                    ]);
                }
            }
        })
        .state('tables', {
            abstract: true,
            url: "/tables",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html"
        })
        .state('tables.static_table', {
            url: "/static_table",
            templateUrl: "/pos_self_order/static/assets/views/table_basic.html",
            data: { pageTitle: 'Static table' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'angular-peity',
                            files: ['/pos_self_order/static/assets/js/plugins/peity/jquery.peity.min.js', '/pos_self_order/static/assets/js/plugins/peity/angular-peity.js']
                        },
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/iCheck/custom.css','/pos_self_order/static/assets/js/plugins/iCheck/icheck.min.js']
                        }
                    ]);
                }
            }
        })
        .state('tables.data_tables', {
            url: "/data_tables",
            templateUrl: "/pos_self_order/static/assets/views/table_data_tables.html",
            data: { pageTitle: 'Data Tables' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/dataTables/datatables.min.js','/pos_self_order/static/assets/css/plugins/dataTables/datatables.min.css']
                        },
                        {
                            serie: true,
                            name: 'datatables',
                            files: ['/pos_self_order/static/assets/js/plugins/dataTables/angular-datatables.min.js']
                        },
                        {
                            serie: true,
                            name: 'datatables.buttons',
                            files: ['/pos_self_order/static/assets/js/plugins/dataTables/angular-datatables.buttons.min.js']
                        }
                    ]);
                }
            }
        })
        .state('tables.foo_table', {
            url: "/foo_table",
            templateUrl: "/pos_self_order/static/assets/views/foo_table.html",
            data: { pageTitle: 'Foo Table' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/footable/footable.all.min.js', '/pos_self_order/static/assets/css/plugins/footable/footable.core.css']
                        },
                        {
                            name: 'ui.footable',
                            files: ['/pos_self_order/static/assets/js/plugins/footable/angular-footable.js']
                        }
                    ]);
                }
            }
        })
        .state('tables.nggrid', {
            url: "/nggrid",
            templateUrl: "/pos_self_order/static/assets/views/nggrid.html",
            data: { pageTitle: 'ng Grid' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            name: 'ngGrid',
                            files: ['/pos_self_order/static/assets/js/plugins/nggrid/ng-grid-2.0.3.min.js']
                        },
                        {
                            insertBefore: '#loadBefore',
                            files: ['/pos_self_order/static/assets/js/plugins/nggrid/ng-grid.css']
                        }
                    ]);
                }
            }
        })
        .state('commerce', {
            abstract: true,
            url: "/commerce",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html",
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/footable/footable.all.min.js', '/pos_self_order/static/assets/css/plugins/footable/footable.core.css']
                        },
                        {
                            name: 'ui.footable',
                            files: ['/pos_self_order/static/assets/js/plugins/footable/angular-footable.js']
                        }
                    ]);
                }
            }
        })
        .state('commerce.products_grid', {
            url: "/products_grid",
            templateUrl: "/pos_self_order/static/assets/views/ecommerce_products_grid.html",
            data: { pageTitle: 'E-commerce grid' }
        })
        .state('commerce.product_list', {
            url: "/product_list",
            templateUrl: "/pos_self_order/static/assets/views/ecommerce_product_list.html",
            data: { pageTitle: 'E-commerce product list' }
        })
        .state('commerce.orders', {
            url: "/orders",
            templateUrl: "/pos_self_order/static/assets/views/ecommerce_orders.html",
            data: { pageTitle: 'E-commerce orders' }
        })
        .state('commerce.product', {
            url: "/product",
            templateUrl: "/pos_self_order/static/assets/views/ecommerce_product.html",
            data: { pageTitle: 'Product edit' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/summernote/summernote.css','/pos_self_order/static/assets/css/plugins/summernote/summernote-bs3.css','/pos_self_order/static/assets/js/plugins/summernote/summernote.min.js']
                        },
                        {
                            name: 'summernote',
                            files: ['/pos_self_order/static/assets/css/plugins/summernote/summernote.css','/pos_self_order/static/assets/css/plugins/summernote/summernote-bs3.css','/pos_self_order/static/assets/js/plugins/summernote/summernote.min.js','/pos_self_order/static/assets/js/plugins/summernote/angular-summernote.min.js']
                        }
                    ]);
                }
            }

        })
        .state('commerce.product_details', {
            url: "/product_details",
            templateUrl: "/pos_self_order/static/assets/views/ecommerce_product_details.html",
            data: { pageTitle: 'E-commerce Product detail' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/slick/slick.css','/pos_self_order/static/assets/css/plugins/slick/slick-theme.css','/pos_self_order/static/assets/js/plugins/slick/slick.min.js']
                        },
                        {
                            name: 'slick',
                            files: ['/pos_self_order/static/assets/js/plugins/slick/angular-slick.min.js']
                        }
                    ]);
                }
            }
        })
        .state('commerce.payments', {
            url: "/payments",
            templateUrl: "/pos_self_order/static/assets/views/ecommerce_payments.html",
            data: { pageTitle: 'E-commerce payments' }
        })
        .state('commerce.cart', {
            url: "/cart",
            templateUrl: "/pos_self_order/static/assets/views/ecommerce_cart.html",
            data: { pageTitle: 'Shopping cart' }
        })
        .state('gallery', {
            abstract: true,
            url: "/gallery",
            templateUrl: "/pos_self_order/static/assets/views/common/content.html"
        })
        .state('gallery.basic_gallery', {
            url: "/basic_gallery",
            templateUrl: "/pos_self_order/static/assets/views/basic_gallery.html",
            data: { pageTitle: 'Lightbox Gallery' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/blueimp/jquery.blueimp-gallery.min.js','/pos_self_order/static/assets/css/plugins/blueimp/css/blueimp-gallery.min.css']
                        }
                    ]);
                }
            }
        })
        .state('gallery.bootstrap_carousel', {
            url: "/bootstrap_carousel",
            templateUrl: "/pos_self_order/static/assets/views/carousel.html",
            data: { pageTitle: 'Bootstrap carousel' }
        })
        .state('gallery.slick_gallery', {
            url: "/slick_gallery",
            templateUrl: "/pos_self_order/static/assets/views/slick.html",
            data: { pageTitle: 'Slick carousel' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/css/plugins/slick/slick.css','/pos_self_order/static/assets/css/plugins/slick/slick-theme.css','/pos_self_order/static/assets/js/plugins/slick/slick.min.js']
                        },
                        {
                            name: 'slick',
                            files: ['/pos_self_order/static/assets/js/plugins/slick/angular-slick.min.js']
                        }
                    ]);
                }
            }
        })
        .state('css_animations', {
            url: "/css_animations",
            templateUrl: "/pos_self_order/static/assets/views/css_animation.html",
            data: { pageTitle: 'CSS Animations' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            reconfig: true,
                            serie: true,
                            files: ['/pos_self_order/static/assets/js/plugins/rickshaw/vendor/d3.v3.js','/pos_self_order/static/assets/js/plugins/rickshaw/rickshaw.min.js']
                        },
                        {
                            reconfig: true,
                            name: 'angular-rickshaw',
                            files: ['/pos_self_order/static/assets/js/plugins/rickshaw/angular-rickshaw.js']
                        }
                    ]);
                }
            }

        })
        .state('landing', {
            url: "/landing",
            templateUrl: "/pos_self_order/static/assets/views/landing.html",
            data: { pageTitle: 'Landing page', specialClass: 'landing-page' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['/pos_self_order/static/assets/js/plugins/wow/wow.min.js']
                        }
                    ]);
                }
            }
        })
        .state('outlook', {
            url: "/outlook",
            templateUrl: "/pos_self_order/static/assets/views/outlook.html",
            data: { pageTitle: 'Outlook view', specialClass: 'fixed-sidebar' }
        })
        .state('off_canvas', {
            url: "/off_canvas",
            templateUrl: "/pos_self_order/static/assets/views/off_canvas.html",
            data: { pageTitle: 'Off canvas menu', specialClass: 'canvas-menu' }
        });

}
angular
    .module('inspinia')
    .config(config)
    .run(function($rootScope, $state) {
        $rootScope.$state = $state;
    });
