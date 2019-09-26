# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Constant:
    SUPPLIER_TAX_CODE = '0100274124'
    SINVOICE_URI = 'https://demo-sinvoice.viettel.vn:8443'
    SINVOICE_CREATE_URI = SINVOICE_URI + '/' + 'InvoiceAPI/InvoiceWS/createInvoice' + '/' + SUPPLIER_TAX_CODE
    SINVOICE_CREATE_DRAFT_URI = SINVOICE_URI + '/' + 'InvoiceAPI/InvoiceWS/createOrUpdateInvoiceDraft' + '/' + SUPPLIER_TAX_CODE
    SINVOICE_CANCEL_URI = SINVOICE_URI + '/' + 'InvoiceAPI/InvoiceWS/cancelTransactionInvoice'
