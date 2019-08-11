# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import requests
from PIL import Image

import base64
import datetime
import io
import json
import re

from werkzeug import urls

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools import image
from odoo.tools.translate import html_translate
from odoo.exceptions import Warning
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import url_for


class Slide(models.Model):

    _name = 's.slide.slide'
    _inherit = ['mail.thread', 'website.seo.metadata', 'website.published.mixin']
    _description = 'Slides'
    _mail_post_access = 'read'
    _order = "id desc"

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(channel_id, name)', 'The slide name must be unique within a channel')
    ]

    # description
    name = fields.Char('Title', required=True, translate=True)
    active = fields.Boolean(default=True)
    post_id = fields.Many2one('blog.post', string='Post')
    view_id = fields.Many2one('ir.ui.view', string='View')
    description = fields.Text('Description', translate=True)
    sub_slide_ids = fields.One2many('s.slide.insite', 'slide_id', string="Sub Count")
    script = fields.Char(string="Script", compute='_compute_script', store=True)
    model = fields.Char('Model')
    source_id = fields.Integer('Source')
    source_name = fields.Char('Name')

    @api.multi
    @api.depends('sub_slide_ids.script')
    def _compute_script(self):
        for slide in self:
            script = '<ul>'

            for sub in slide.sub_slide_ids:
                script += sub.script

            script += '</ul>'

            slide.script = script

class SlideInsite(models.Model):
    """ Embedding in third party websites. Track view count, generate statistics. """
    _name = 's.slide.insite'
    _description = 'In-site Slides View'
    _rec_name = 'slide_id'

    slide_id = fields.Many2one('s.slide.slide', string="Slideshow", index=True)
    image = fields.Binary('Background Image', attachment=True)
    image_medium = fields.Binary('Medium', compute="_get_image", store=True, attachment=True)
    image_thumb = fields.Binary('Thumbnail', compute="_get_image", store=True, attachment=True)
    layer_ids = fields.One2many('s.slide.layer', 'insite_id', string="Layer")
    script = fields.Char(string="Script", compute='_compute_script', store=True)

    @api.multi
    @api.depends('layer_ids.script', 'image')
    def _compute_script(self):

        for slide in self:
            script = '<li data-index="rs-'+str(slide.id)+'" data-transition="fade" data-slotamount="default" data-hideafterloop="0" data-hideslideonmobile="off"  data-easein="default" data-easeout="default" data-masterspeed="1500"  data-rotate="0"  data-saveperformance="off"  data-title="Intro" data-param1="" data-param2="" data-param3="" data-param4="" data-param5="" data-param6="" data-param7="" data-param8="" data-param9="" data-param10="" data-description="">'
            script += '<img src = "data:image/[a-z]+?;base64,' + slide.image.decode('ascii')+'" alt=""  data-bgposition="center center" data-bgfit="cover" data-bgrepeat="no-repeat" data-bgparallax="5" class="rev-slidebg" data-no-retina>'

            for layer in slide.layer_ids:
                script += layer.script

            script += '</li>'

            slide.script = script

    @api.depends('image')
    def _get_image(self):
        for record in self:
            if record.image:
                record.image_medium = image.crop_image(record.image, type='top', ratio=(4, 3), size=(500, 400))
                record.image_thumb = image.crop_image(record.image, type='top', ratio=(4, 3), size=(200, 200))
            else:
                record.image_medium = False
                record.image_thumb = False


class SlideLayer(models.Model):
    _name = 's.slide.layer'
    _description = 'Layer'

    insite_id = fields.Many2one('s.slide.insite', string="In-site Slide", index=True)
    type = fields.Selection([('text', 'Text'), ('image', 'Image')], string='Type', required=True)
    layer_from = fields.Selection([('top', 'Top'), ('right', 'Right'), ('bottom', 'Bottom'), ('left', 'Left')], string='From', default='top')
    destination_x = fields.Integer(string='X', require=True, default='200')
    destination_y = fields.Integer(string='Y', require=True, default='200')
    title = fields.Char(string='Title')
    image = fields.Binary('Image', attachment=True)
    speed = fields.Integer(string='Speed', default='1200')
    start_time = fields.Integer('Start Time', default='2000')
    script = fields.Char(string="Script", compute='_compute_script', store=True)
    font_size = fields.Integer(string='Font Size', default='30')
    font_style = fields.Char(string='Font Style', default='Time New Roman')
    font_color = fields.Char(string='Font Color', default='#fff')
    image_width = fields.Integer(string='Image Width', default='500')
    image_height = fields.Integer(string='Image Height', default='500')

    @api.multi
    @api.depends('insite_id', 'type', 'layer_from', 'destination_x', 'destination_y', 'title', 'image', 'speed', 'start_time')
    def _compute_script(self):
        for layer in self:
            script = '<div class="tp-caption   tp-resizeme rs-parallaxlevel-3"'
            script += ' id="slide-'+str(layer.insite_id.id)+'-layer-'+str(layer.id)+'"'
            script += ' data-x="[\'left\',\'left\',\'left\',\'left\']" data-hoffset="[\''+str(layer.destination_x)+'\',\'553\',\'127\',\'58\']"'
            script += ' data-y="[\'top\',\'top\',\'top\',\'top\']" data-voffset="[\''+str(layer.destination_y)+'\',\'297\',\'622\',\'529\']"'
            script += '	data-width="none"'
            script += ' data-height="none"'
            script += ' data-whitespace="nowrap"'
            script += ' data-type="'+layer.type+'"'
            script += ' data-responsive_offset="on"'
            script += ' data-frames=\'[{"from":"x:'+layer.layer_from+';","speed":'+str(layer.speed)+',"to":"o:1;","delay":'+str(layer.start_time)+',"ease":"Power3.easeOut"},{"delay":"wait","speed":1500,"to":"opacity:0;","ease":"Power4.easeIn"}]\' '
            script += ' data-textAlign="[\'left\',\'left\',\'left\',\'left\']"'
            script += ' data-paddingtop="[0,0,0,0]"'
            script += ' data-paddingright="[0,0,0,0]"'
            script += ' data-paddingbottom="[0,0,0,0]"'
            script += ' data-paddingleft="[0,0,0,0]"'
            script += ' style="z-index: 9;text-transform:left;border-width:0px;">'
            if layer.type == 'image':
                script += ' <img src = "data:image/[a-z]+?;base64,' + layer.image.decode('ascii')+'" alt="" data-ww="[\''+str(layer.image_width)+'\',\'260px\',\'130px\',\'100px\']" data-hh="[\''+str(layer.image_height)+'\',\'450px\',\'225px\',\'173px\']" width="260" height="450" data-no-retina>'
            elif layer.type == 'text':
                script += '<span style = "color: '+layer.font_color+' ;font-family: '+layer.font_style+';font-size: '+str(layer.font_size)+'px;" >'+layer.title+'</span>'
            script += '</div>'

            layer.script = script
