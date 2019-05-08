odoo.define('website_popup.website_popup', function (require) {
"use strict";
var ajax = require('web.ajax');
var core = require('web.core');
var rootWidget = require('root.widget');
$(document).ready(function() {
    ajax.jsonRpc('http://'+window.location.host+'/website_popup/load_country', 'call', {
        'args': ['test', 1]
    }).done(function (data) {
        var countries = data['countries'];
        var selectbox = $('#interest_country');
        selectbox.empty();
        var list = '';
        for (var j = 0; j < countries.length; j++){
                list += "<option value='" +countries[j].id+ "'>" +countries[j].name+ "</option>";
        }
        selectbox.html(list);
    });

    ajax.jsonRpc('http://'+window.location.host+'/website_popup/load_blog_category', 'call', {
        'args': ['test', 1]
    }).done(function (data) {
        var categories = data['categories'];
        var selectbox = $('#interest_category');
        selectbox.empty();
        var list = '';
        for (var j = 0; j < categories.length; j++){
                list += "<option value='" +categories[j].id+ "'>" +categories[j].name+ "</option>";
        }
        selectbox.html(list);
    });

    $(document.body).on('click', '.btn-confirm-survey', function (e) {
        e.preventDefault();
        var data = $('#form_popup_survey').serialize();
        sessionStorage.setItem('popup_survey', data);
        $('#survey_modal').modal('hide');
    });
    if(! sessionStorage.getItem('popup_survey')){
        $('#survey_modal').modal('show');
    } else {
//        var surveyData     = {};
//        $.each(sessionStorage.getItem('popup_survey'), function(key, value) {
//            var data = value.split('=');
//            surveyData[data[0]] = decodeURIComponent(data[1]);
//        });

        alert("you have selected " + sessionStorage.getItem('popup_survey'));
    }
});
});
