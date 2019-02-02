from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from odoo.http import request
from datetime import datetime
from odoo.tools import html_escape as escape, ustr, image_resize_and_sharpen, image_save_for_web
import unicodedata
import re

class SprogroupassetMail(models.Model):

    _name = "sprogroupasset.mail"

    email_subject = fields.Char(string="Email Subject", required=True)
    email_content = fields.Html(string="Email Content", sanizied=False)

    # email_name = fields.Char(string="Email Name", required=True)
    email_to = fields.Char(string="Recipient", required=True)
    equipment = fields.Many2one('sprogroupasset.equipment', string="Equipment")

    # @api.onchange('exam_id')
    # def _change_share(self):
    #     notification_template = self.env['ir.model.data'].get_object('exam_test_quiz', 'exam_share_email')
    #
    #     self.email_subject = notification_template.subject
    #
    #     temp_content = notification_template.body_html
    #     temp_content = temp_content.replace('__URL__',request.httprequest.host_url + "exam/" + self.exam_id.slug)
    #     temp_content = temp_content.replace('__EXAM__',self.exam_id.name)
    #
    #     self.email_content = temp_content
    #
    #     request.httprequest.host_url + "form/myinsert"
        
    @api.one
    def send_mail(self):
        template = self.env.ref(
            'sprogroupasset.mail_template_sprogroupasset_mail',
            raise_if_not_found=False)
        template.send_mail(self.id)