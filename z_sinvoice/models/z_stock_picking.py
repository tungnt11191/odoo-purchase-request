# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import requests
import json
from odoo.exceptions import UserError, ValidationError
import base64
from datetime import datetime
from .constant import Constant
from datetime import date
import werkzeug.utils


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    x_invoice_type = fields.Many2one('z.invoice.invoice.type', u'Loại HĐĐT', copy=False)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_partner_tax_code = fields.Char(string=_(u"Mã số thuế"), size=128)
    x_template_symbol = fields.Many2one('x.invoice.template', string=_(u"Ký hiệu mẫu hóa đơn"))
    x_invoice_symbol = fields.Char(string=_(u"Ký hiệu hóa đơn"), size=128)
    x_supplier_invoice_number = fields.Char(string=_(u"Số hóa đơn"),
                                            help=_("The reference of this invoice as provided by the supplier."))
    x_transaction_id = fields.Char(u'ID giao dịch HĐĐT', copy=False)
    x_invoice_status = fields.Selection([
        ('status_not_sync', 'Chưa tạo trên SINVOICE'),
        ('status_created', 'Đã tạo trên SINVOICE'),
        ('status_canceled', 'Đã hủy trên SINVOICE'),
    ], string=u'Trạng thái SINVOICE', default='status_not_sync', readonly=True, copy=False)
    x_created_sinvoice = fields.Datetime(string=u'Ngày tạo HĐĐT', copy=False)
    x_canceled_sinvoice = fields.Datetime(string=u'Ngày hủy HĐĐT', copy=False)
    x_reservation_code = fields.Char(u"Reservation Code", copy=False)
    x_origin_invoice = fields.Char(string=u'Hóa đơn gốc(Hóa đơn điều chỉnh)', compute='_compute_origin_invoice', store=True, copy=False)
    x_economic_contract_number = fields.Char(string=u'Hợp đồng kinh tế số', copy=False)
    x_transportation_method = fields.Char(string=u'Phương tiện vận chuyển', copy=False)
    x_about = fields.Char(string=u'Về việc', copy=False)
    x_contract_number = fields.Char(string=u'Hợp đồng số', copy=False)
    x_able_to_sync = fields.Boolean('Able to sync', compute='_compute_able_to_sync')

    @api.multi
    @api.depends('picking_type_id', 'picking_type_id.x_invoice_type')
    def _compute_able_to_sync(self):
        for picking in self:
            if not picking.picking_type_id or not picking.picking_type_id.x_invoice_type.id:
                picking.x_able_to_sync = False
            else:
                picking.x_able_to_sync = True

    @api.multi
    @api.depends('origin')
    def _compute_origin_invoice(self):
        for picking in self:
            if picking.origin:
                origin_picking = self.env['stock.picking'].search([('name', '=', picking.origin)], limit=1)
                picking.x_origin_invoice = origin_picking.x_supplier_invoice_number
            else:
                picking.x_origin_invoice = False

    @api.onchange('x_template_symbol')
    def _onchange_x_template_symbol(self):
        if self.x_template_symbol:
            self.x_invoice_symbol = self.x_template_symbol.invoice_symbol

    @api.multi
    def validate_invoice(self, invoice):
        valid = True
        message = ''
        today = date.today()
        if not invoice.x_partner_tax_code:
            valid = False
            message = u'Mã số thuế để trống'

        if invoice.x_transaction_id:
            valid = False
            message = u'Hóa đơn đã được tạo hóa đơn điện tử'

        # in stock picking
        if not invoice.picking_type_id or not invoice.picking_type_id.x_invoice_type:
            valid = False
            message = u'Không có chức năng đồng bộ hóa đơn điện tử tại phiếu kho'

        return valid, message


    # adjustmentType :    1 - hoa don goc
    #                     3 - hoa don thay the
    #                     5 - hoa don dieu chinh

    # adjustmentInvoiceType :   0 - khong dieu chinh
    #                           1 - dieu chinh tien
    #                           2 - dieu chinh thong tin
    @api.multi
    def generate_invoice_date(self, invoice, adjustment_type, username, adjustmentInvoiceType = 0, origin_invoice=None):
        # transporter information
        # buyer_name = invoice.implemented_by_id.name if invoice.implemented_by_id else ''
        # if buyer_name == '':
        #     buyer_name = invoice.company_id.partner_id.name if invoice.company_id and invoice.company_id.partner_id else ''

        # transporter information

        # buyer information
        buyer_name = invoice.partner_id.name if invoice.partner_id else ''
        buyer_tax_code = invoice.x_partner_tax_code.strip() if invoice.x_partner_tax_code else ''
        buyer_address_line = invoice.partner_id.street if invoice.partner_id and invoice.partner_id.street else ''
        buyer_district_name = invoice.partner_id.x_district_id.x_name if invoice.partner_id and invoice.partner_id.x_district_id else ''
        buyer_city_name = invoice.partner_id.state_id.name if invoice.partner_id and invoice.partner_id.state_id else ''
        buyer_country_code = '84'
        buyer_phone_number = invoice.partner_id.mobile if invoice.partner_id and invoice.partner_id.mobile else ''
        buyer_email = invoice.partner_id.email if invoice.partner_id and invoice.partner_id.email else ''
        # buyer information

        # seller information
        seller_code = invoice.company_id.name if invoice.company_id else ''
        seller_legal_name = invoice.company_id.name if invoice.company_id else ''
        seller_tax_code = invoice.company_id.vat if invoice.company_id and invoice.company_id.vat else ''
        seller_address_line = invoice.company_id.partner_id.street if invoice.company_id.partner_id and invoice.company_id.partner_id.street else ''
        seller_phone_number = invoice.company_id.partner_id.mobile if invoice.company_id.partner_id and invoice.company_id.partner_id.mobile else ''
        seller_email = invoice.company_id.partner_id.email if invoice.company_id.partner_id and invoice.company_id.partner_id.email else ''


        data = {
            "generalInvoiceInfo": {
                "invoiceType": invoice.x_template_symbol.x_invoice_type.code,
                "templateCode": invoice.x_template_symbol.code,
                "invoiceSeries": invoice.x_invoice_symbol,
                "currencyCode": invoice.currency_id.name if invoice.currency_id.name else 'VND',
                "invoiceNote": "",
                "adjustmentType": adjustment_type,
                "paymentStatus": True,
                "cusGetInvoiceRight": True,
                "userName": username
            },
            "buyerInfo": {
                "buyerName": buyer_name,
                "buyerLegalName": buyer_name,
                "buyerTaxCode": buyer_tax_code,
                "buyerAddressLine": buyer_address_line,
                "buyerDistrictName": buyer_district_name,
                "buyerCityName": buyer_city_name,
                "buyerCountryCode": buyer_country_code,
                "buyerPhoneNumber": buyer_phone_number,
                "buyerFaxNumber": buyer_phone_number,
                "buyerEmail": buyer_email,
            },
            "sellerInfo": {
                "sellerCode": seller_code,
                "sellerLegalName": seller_legal_name,
                "sellerTaxCode": seller_tax_code,
                "sellerAddressLine": seller_address_line,
                "sellerPhoneNumber": seller_phone_number,
                "sellerEmail": seller_email,
            },
            # "deliveryInfo": {
            #     "deliveryOrderNumber": invoice.name,
            #     "deliveryOrderDate":  invoice.scheduled_date.strftime('%Y%m%d%H%M%S'),
            #     "deliveryOrderBy": invoice.company_id.partner_id.name,
            #     "deliveryBy": buyer_name,
            #     "fromWarehouseName": invoice.location_id.name,
            #     "toWarehouseName": invoice.location_dest_id.name,
            #     "transportationMethod": invoice.x_transportation_method,
            #     "containerNumber": "30A1-xxxxx",
            #     "deliveryOrderContent": invoice.x_about
            # },
            "extAttribute": [],
            "itemInfo": [

            ],
            "discountItemInfo": [],
            "summarizeInfo": {
                "sumOfTotalLineAmountWithoutTax": 0,
                "totalAmountWithoutTax": 0,
                "totalTaxAmount": 0,
                "totalAmountWithTax": 0,
                "totalAmountAfterDiscount": 0,
                "totalAmountWithTaxInWords": u'Không đồng',
                "discountAmount": 0
            },
            "taxBreakdowns": [
            ],
            "metadata": [],
            "customFields": [],
            "meterReading": []
        }

        if invoice.x_economic_contract_number:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 16,
                                        "keyTag": "economicContractNo",
                                        "valueType": "text",
                                        "keyLabel": "Căn cứ hợp đồng kinh tế số",
                                        "stringValue": invoice.x_economic_contract_number
                                    })
        if invoice.x_transportation_method:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 16,
                                        "keyTag": "vehicle",
                                        "valueType": "text",
                                        "keyLabel": "Phương tiện vận chuyển",
                                        "stringValue": invoice.x_transportation_method
                                    })
        if invoice.x_contract_number:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 16,
                                        "keyTag": "contractNo",
                                        "valueType": "text",
                                        "keyLabel": "Hợp đồng số",
                                        "stringValue": invoice.x_contract_number
                                    })
        if invoice.x_about:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 16,
                                        "keyTag": "commandDes",
                                        "valueType": "text",
                                        "keyLabel": "Về việc",
                                        "stringValue": invoice.x_about
                                    })
        if invoice.location_id:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 16,
                                        "keyTag": "importAt",
                                        "valueType": 'text',
                                        "keyLabel": "Nhập tại kho",
                                        "stringValue": invoice.location_id.name
                                    })

        if invoice.location_dest_id:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 16,
                                        "keyTag": "exportAt",
                                        "valueType": 'text',
                                        "keyLabel": "Xuất tại kho",
                                        "stringValue": invoice.location_dest_id.name
                                    })

        if invoice.scheduled_date:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 16,
                                        "keyTag": "commandDate",
                                        "valueType": 'date',
                                        "keyLabel": "Ngày điều động",
                                        "stringValue":  invoice.scheduled_date.strftime('%Y%m%d%H%M%S')
                                    })

        if adjustmentInvoiceType != 0:
            data['generalInvoiceInfo']['adjustmentInvoiceType'] = adjustmentInvoiceType
            data['generalInvoiceInfo']['originalInvoiceId'] = invoice.x_origin_invoice
            data['generalInvoiceInfo']['originalInvoiceIssueDate'] = origin_invoice.x_created_sinvoice.date().strftime('%Y-%m-%d')
            data['generalInvoiceInfo']['additionalReferenceDesc'] = u'Điều Chỉnh'
            data['generalInvoiceInfo']['additionalReferenceDate'] = datetime.strftime(datetime.now(), '%Y-%m-%d')

        index = 0
        for line in invoice.move_ids_without_package:
            index += 1

            item = {
                     "lineNumber": index,
                     "itemCode": line.product_id.default_code if line.product_id and line.product_id.default_code else '',
                     "itemName": line.product_id.name if line.product_id and line.product_id.name else '',
                     "unitName": line.uom_id.name if line.uom_id else '',
                     "quantity": line.quantity_done,
                     "itemTotalAmountWithoutTax": 0,
                     "itemTotalAmountWithTax": 0,
                     "taxAmount": 0,
                     "itemNote": "",
                     "batchNo": "",
                     "expDate": ""
                  }

            batchNo = ''
            expDate = ''
            # get lot and expire date
            for move_line in line.move_line_ids:
                batchNo += (move_line.lot_id.name if move_line.lot_id else '') + ' , '
                expDate += (move_line.lot_id.removal_date.strftime('%d-%m-%Y') if move_line.lot_id else '') + ' , '

            item['batchNo'] = batchNo
            item['expDate'] = expDate

            data['itemInfo'].append(item)
        return data

    @api.multi
    def verify_return_code(self, status_code):
        if status_code == 500:
            raise ValidationError(u'Error, Username or Password incorrect')
        elif status_code == 400:
            raise ValidationError(u'The request parameters are incomplete or missing')
        elif status_code == 403:
            raise ValidationError(u'The action or the request URI is not allowed by the system')
        elif status_code == 404:
            raise ValidationError(u'The resource referenced by the URI was not found')
        elif status_code == 422:
            raise ValidationError(u'One of the requested action has generated an error')
        elif status_code == 429:
            raise ValidationError(u'Your application is making too many requests and is being rate limited')
        elif status_code == 200:
            return status_code
        return status_code

    @api.multi
    def create_hddt(self):
        for invoice in self:
            valid, message = self.validate_invoice(invoice)
            if not valid:
                raise ValidationError(message)

            user_obj = self.env.user
            username = user_obj.x_sinvoice_username
            password = user_obj.x_sinvoice_password

            headers = {"Content-type": "application/json"}
            base64string = base64.b64encode(bytes(username + ':' + password, "utf-8"))
            headers['Authorization'] = "Basic %s" % base64string.decode("utf-8")
            url = Constant.SINVOICE_CREATE_URI

            data = {}

            # neu ton tai hoa don goc thi dieu chinh, neu khong thi tao moi
            if invoice.x_origin_invoice:
                origin_invoice = self.env['stock.picking'].search([('x_supplier_invoice_number','=',invoice.x_origin_invoice)], order='id asc')
                if len(origin_invoice.ids) > 0:
                    data = self.generate_invoice_date(invoice=invoice, adjustment_type=5, username=username, adjustmentInvoiceType=2, origin_invoice=origin_invoice[0])
            else:
                data = self.generate_invoice_date(invoice=invoice, adjustment_type=1, username=username, adjustmentInvoiceType=0)

            result = requests.post(url, data=json.dumps(data), headers=headers)

            if self.verify_return_code(result.status_code) == 200:
                output = result.json()
                if 'errorCode' in output and output['errorCode'] != None:
                    raise ValidationError(str(output['errorCode']) + ": " + str(output['description']))
                else:
                    output_result = output['result']
                    values = {
                                'x_supplier_invoice_number': output_result['invoiceNo'][6:],
                                'x_transaction_id': output_result['transactionID'],
                                'x_invoice_status': 'status_created',
                                'x_created_sinvoice': datetime.now(),
                                'x_reservation_code': output_result['reservationCode']
                              }
                    invoice.update(values)


    @api.multi
    def cancel_hddt(self):
        user_obj = self.env.user
        username = user_obj.x_sinvoice_username
        password = user_obj.x_sinvoice_password

        headers = {}
        base64string = base64.b64encode(bytes(username + ':' + password, "utf-8"))
        headers['Authorization'] = "Basic %s" % base64string.decode("utf-8")

        for invoice in self:
            created_sinvoice_datetime = invoice.x_created_sinvoice.strftime('%Y%m%d%H%M%S')
            canceled_sinvoice_datetime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')

            url = Constant.SINVOICE_CANCEL_URI
            data = {
                    "supplierTaxCode": Constant.SUPPLIER_TAX_CODE,
                    "invoiceNo": invoice.x_invoice_symbol+invoice.x_supplier_invoice_number,
                    "strIssueDate": created_sinvoice_datetime,
                    "additionalReferenceDesc": 'huy',
                    "additionalReferenceDate": canceled_sinvoice_datetime
                }

            werkzeug.url_encode(data)
            result = requests.get(url, params=data, headers=headers)

            if self.verify_return_code(result.status_code) == 200:
                output = result.json()
                if 'errorCode' in output and output['errorCode'] != None:
                    raise ValidationError(str(output['errorCode']) + ": " + str(output['description']))
                else:
                    values = {
                        'x_supplier_invoice_number': False,
                        'x_transaction_id': False,
                        'x_reservation_code': False,
                        'x_invoice_status': 'status_canceled',
                        'x_canceled_sinvoice': datetime.now()
                    }
                    invoice.update(values)
