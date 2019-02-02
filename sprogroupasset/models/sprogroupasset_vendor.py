
from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class SprogroupassetVendor(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.vendor'
    _description = 'Sprogroupasset Vendor'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    address = fields.Char('Address')
    website = fields.Char('Website')
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')
    description = fields.Html('Description')
