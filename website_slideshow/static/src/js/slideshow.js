odoo.define('website_slideshow.website_slideshow', function (require) {
"use strict";
var core = require('web.core');
var ajax = require('web.ajax');
var Dialog = require('web.Dialog');
var widgets = require('web_editor.widget');
var options = require('web_editor.snippets.options');

var _t = core._t;
var qweb = core.qweb;

options.registry.revoslider = options.Class.extend({
    /**
     * @override
     */
    start: function () {
        var self = this;
        var def = this._super.apply(this, arguments);
        return def;
    },
    /**
     * Associates unique ID on slider elements.
     *
     * @override
     */
    onBuilt: function () {
        console.log('onBuilt');
        this.id = 'revoslide_' + new Date().getTime();
        this.$target.find('#revoslide')[0].id = this.id;
    },
    /**
     * Associates unique ID on cloned slider elements.
     *
     * @override
     */
    onClone: function () {
        var id = 'revoslide_' + new Date().getTime();
        this.$target.find('#revoslide')[0].id = this.id;
    },
});

$(document).ready(function() {

    function generate_slide(){
        var output ='<ul>'
        output +=    '<li data-transition="fade">';
        output +=       '<img src="/website_slideshow/static/img/agencyslider.jpg" alt="" width="1920" height="1280"/>';
        output +=       '<div class="tp-caption News-Title"';
        output +=       'data-x="left" data-hoffset="80"';
        output +=       'data-y="top" data-voffset="450"';
        output +=       'data-whitespace="normal"';
        output +=       'data-transform_idle="o:1;"';
        output +=       'data-transform_in="o:0"';
        output +=       'data-transform_out="o:0"';
        output +=       'data-start="500">DISCOVER THE WILD';
        output +=       '</div>';
        output +=   '</li>';
        output +='</ul>'
        return output;
    }

    $('.tungnt_s_slideshow').each(function () {
        console.log('tungnt_s_slideshow')
        var slideshow = this;
            // display the reduction from the pricelist in function of the quantity
        ajax.jsonRpc("/website_slideshow/get_slideshow", 'call', {'slide_name': $(slideshow).attr('id')})
        .then(function (data) {
            console.log(data);
            $(slideshow).append(data);

            $(slideshow).revolution({
                  sliderType:"standard",
                  sliderLayout:"auto",
                  delay:9000,
                  navigation: {
                      arrows:{enable:true}
                  },
                  gridwidth:900,
                  gridheight:720
                });
        });

    });

});


});


