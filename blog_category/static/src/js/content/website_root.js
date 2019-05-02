odoo.define('blog_category.website_root_inherit', function (require) {
'use strict';

var core = require('web.core');
var Widget = require('web.Widget');
var SummernoteManager = require('web_editor.rte.summernote');
var WebsiteNewMenu = require('website.newMenu');
var wUtils = require('website.utils');
var Dialog = require("web.Dialog");
var websiteRootData = require('website.WebsiteRoot');

websiteRootData.WebsiteRoot.include({
    /**
     * Allows the URL input to propose existing website pages.
     *
     * @override
     */
    events: _.extend({}, websiteRootData.WebsiteRoot.prototype.events || {}, {
        'click .js_multi_blog_category_switch': '_multiBlogCategorySwitch',
        'click .js_multi_blog_country_switch': '_multiCountrySwitch',
    }),

	_multiBlogCategorySwitch: function (ev) {
        ev.preventDefault();
        var self = this;
        var current_element = $(ev.currentTarget);
        var current_li = $(ev.currentTarget).parent().parent();
        this._rpc({
            route: '/blog_category/change_category',
            params: {
                id: $(current_li).data('id'),
                object: $(current_li).data('object'),
                category_id: current_element.data('category_id')
            },
        })
        .done(function (result) {
            if(result){
                var current_chosen_category = current_li.find('#chosen_category')[0];
                $(current_chosen_category).text(current_element.data('category_name'));
            } else {
                alert("Cannot change category");
            }
        })
        .fail(function (err, data) {
            return new Dialog(self, {
                title: data.data ? data.data.arguments[0] : "",
                $content: $('<div/>', {
                    html: (data.data ? data.data.arguments[1] : data.statusText)
                        + '<br/>'
                        + _.str.sprintf(
                            _t('It might be possible to edit the relevant items or fix the issue in <a href="%s">the classic Odoo interface</a>'),
                            '/web#return_label=Website&model=' + $(current_li).data('object') + '&id=' + $data.data('id')
                        ),
                }),
            }).open();
        });
    },


	_multiCountrySwitch: function (ev) {
        ev.preventDefault();
        var self = this;
        var current_element = $(ev.currentTarget);
        var current_li = $(ev.currentTarget).parent().parent();
        this._rpc({
            route: '/blog_category/change_country',
            params: {
                id: $(current_li).data('id'),
                object: $(current_li).data('object'),
                country_id: current_element.data('country_id')
            },
        })
        .done(function (result) {
            if(result){
                var current_chosen_country = current_li.find('#chosen_country')[0];
                $(current_chosen_country).text(current_element.data('country_name'));
            } else {
                alert("Cannot change country");
            }
        })
        .fail(function (err, data) {
            return new Dialog(self, {
                title: data.data ? data.data.arguments[0] : "",
                $content: $('<div/>', {
                    html: (data.data ? data.data.arguments[1] : data.statusText)
                        + '<br/>'
                        + _.str.sprintf(
                            _t('It might be possible to edit the relevant items or fix the issue in <a href="%s">the classic Odoo interface</a>'),
                            '/web#return_label=Website&model=' + $(current_li).data('object') + '&id=' + $data.data('id')
                        ),
                }),
            }).open();
        });
    },
});
});