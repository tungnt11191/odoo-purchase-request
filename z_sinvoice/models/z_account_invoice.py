# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import requests
import json
from odoo.exceptions import UserError, ValidationError
import base64
from datetime import datetime
from .constant import Constant
from datetime import date
import werkzeug.utils
import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'x.invoice.template'
    x_invoice_type = fields.Many2one('z.invoice.invoice.type', 'Loại hóa đơn', require=True)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # x_invoice_type = fields.Many2one('x.invoice.template', 'Loại hóa đơn', copy=False)
    # x_invoice_no = fields.Char(u'Số HĐĐT', copy=False)
    x_transaction_id = fields.Char(u'ID giao dịch HĐĐT', copy=False)
    x_invoice_status = fields.Selection([
        ('status_not_sync', 'Chưa tạo trên SINVOICE'),
        ('status_created', 'Đã tạo trên SINVOICE'),
        ('status_canceled', 'Đã hủy trên SINVOICE'),
        ], string=u'Trạng thái SINVOICE', default='status_not_sync', readonly=True, copy=False)
    # x_template_code = fields.Char(string=u"Ký hiệu mẫu hóa đơn", copy=False)
    # x_invoice_series = fields.Char(string=u"Ký hiệu hóa đơn", copy=False)
    x_created_sinvoice = fields.Datetime(string=u'Ngày tạo HĐĐT', copy=False)
    x_canceled_sinvoice = fields.Datetime(string=u'Ngày hủy HĐĐT', copy=False)
    x_reservation_code = fields.Char(u"Reservation Code", copy=False)
    x_origin_invoice = fields.Char(string=u'Hóa đơn gốc(Hóa đơn điều chỉnh)', copy=False)
    # @api.onchange('x_invoice_type')
    # def _onchange_x_invoice_type(self):
    #     if self.x_invoice_type:
    #         self.x_template_code = self.x_invoice_type.code
    #         self.x_invoice_series = self.x_invoice_type.invoice_symbol

    def validate_tax_code(self, tax_code):
        check = True
        # for c in tax_code:
        #     if not str(c).isdigit():
        #         check = False
        #         break

        if len(tax_code) > 20 or len(tax_code) == 0:
            check = False
        return check

    @api.multi
    def validate_invoice(self, invoice):
        valid = True
        message = ''
        today = date.today()
        if not invoice.x_partner_tax_code:
            valid = False
            message = u'Mã số thuế để trống'
        if invoice.date_invoice and today < invoice.date_invoice:
            valid = False
            message = u'Ngày đồng bộ nhỏ hơn ngày hóa đơn'

        if invoice.x_transaction_id:
            valid = False
            message = u'Hóa đơn đã được tạo hóa đơn điện tử'
        return valid, 'invoice id (' + str(invoice.id) + ')' + ': ' + message

    # adjustmentType :    1 - hoa don goc
    #                     3 - hoa don thay the
    #                     5 - hoa don dieu chinh

    # adjustmentInvoiceType :   0 - khong dieu chinh
    #                           1 - dieu chinh tien
    #                           2 - dieu chinh thong tin
    @api.multi
    def generate_invoice_data(self, invoice, adjustment_type, username, adjustmentInvoiceType = 0, origin_invoice=None):
        payment_method_name = "TM/CK"

        if invoice.payment_term_id:
            if invoice.payment_term_id.x_check_cash_payment:
                payment_method_name = "TM"
            else:
                payment_method_name = "TM/CK"
        # buyer information
        buyer_name = invoice.x_purchase_person.name if invoice.x_purchase_person else ''
        buyer_legal_name = invoice.x_vat_partner if invoice.x_vat_partner else ''

        buyer_address_line = invoice.x_partner_address if invoice.partner_id else ''
        # buyer_district_name = invoice.partner_id.x_district_id.x_name if invoice.partner_id and invoice.partner_id.x_district_id else ''
        # buyer_postal_code = '2342324323'
        # buyer_city_name = invoice.partner_id.state_id.name if invoice.partner_id and invoice.partner_id.state_id else ''
        buyer_country_code = '84'
        # buyer_phone_number = invoice.partner_id.mobile if invoice.partner_id and invoice.partner_id.mobile else ''
        # buyer_email = invoice.partner_id.email if invoice.partner_id and invoice.partner_id.email else ''

        buyer_id_no = "8888899999"  # so CMT
        buyer_id_type = "1"  #1 or 3
        buyer_code = invoice.x_purchase_person.ref if invoice.x_purchase_person and invoice.x_purchase_person.ref else ''
        buyer_birthdate = invoice.partner_id.birthdate.strftime('%Y-%m-%d') if invoice.partner_id and invoice.partner_id.birthdate else ''

        buyer_bank_name = ""
        buyer_bank_account = ""
        if invoice.partner_id and len(invoice.partner_id.bank_ids) > 0:
            buyer_bank_name = invoice.partner_id.bank_ids[0].acc_number
            buyer_bank_account = invoice.partner_id.bank_ids[0].acc_number
        # buyer information

        # seller information
        seller_code = invoice.user_id.name if invoice.user_id else ''
        seller_legal_name = invoice.company_id.name if invoice.company_id else ''
        seller_tax_code = invoice.company_id.vat if invoice.company_id and invoice.company_id.vat else ''
        seller_address_line = invoice.company_id.partner_id.street if invoice.company_id.partner_id and invoice.company_id.partner_id.street else ''
        seller_phone_number = invoice.company_id.partner_id.mobile if invoice.company_id.partner_id and invoice.company_id.partner_id.mobile else ''
        seller_email = invoice.company_id.partner_id.email if invoice.company_id.partner_id and invoice.company_id.partner_id.email else ''
        seller_bank_name = "Ngân hàng Quân đội MB"
        seller_bank_account = "01578987871236547"

        data = {
            "generalInvoiceInfo": {
                "invoiceType": invoice.x_template_symbol.x_invoice_type.code,
                "templateCode": invoice.x_template_symbol.code,
                "invoiceSeries": invoice.x_invoice_symbol,
                "currencyCode": invoice.currency_id.name if invoice.currency_id.name else 'VND',
                "invoiceNote": "",
                "adjustmentType": adjustment_type,
                "paymentStatus": True,
                "paymentType": payment_method_name,
                "paymentTypeName": payment_method_name,
                "cusGetInvoiceRight": True,
                "userName": username
            },
            "buyerInfo": {
                "buyerName": buyer_name,
                "buyerLegalName": buyer_legal_name,
                "buyerAddressLine": buyer_address_line,
                # "buyerPostalCode": buyer_postal_code,
                # "buyerDistrictName": buyer_district_name,
                # "buyerCityName": buyer_city_name,
                # "buyerCountryCode": buyer_country_code,
                # "buyerPhoneNumber": buyer_phone_number,
                # "buyerFaxNumber": buyer_phone_number,
                # "buyerEmail": buyer_email,
                "buyerBankName": buyer_bank_name,
                "buyerBankAccount": buyer_bank_account,
                # "buyerIdNo": buyer_id_no,
                # "buyerIdType": buyer_id_type,
                "buyerCode": buyer_code,
                "buyerBirthDay": buyer_birthdate
            },
            # "sellerInfo": {
            #     "sellerCode": seller_code,
            #     "sellerLegalName": seller_legal_name,
            #     "sellerTaxCode": seller_tax_code,
            #     "sellerAddressLine": seller_address_line,
            #     "sellerPhoneNumber": seller_phone_number,
            #     "sellerEmail": seller_email,
            #     # "sellerBankName": seller_bank_name,
            #     # "sellerBankAccount": seller_bank_account
            # },
            "extAttribute": [],
            "payments": [
                {
                    "paymentMethodName": payment_method_name
                }
            ],
            "deliveryInfo": {},
            "itemInfo": [

            ],
            "discountItemInfo": [],
            "summarizeInfo": {
                "sumOfTotalLineAmountWithoutTax": invoice.x_functional_amount_untaxed,
                # "totalAmountWithoutTax": invoice.x_functional_amount_untaxed,
                "totalTaxAmount": invoice.x_functional_amount_tax,
                "totalAmountWithTax": invoice.x_functional_amount_untaxed + invoice.x_functional_amount_tax,
                "totalAmountAfterDiscount": invoice.x_functional_amount_untaxed,
                "totalAmountWithTaxInWords": invoice.currency_id.amount_to_text(invoice.x_functional_amount_total),
                "discountAmount": invoice.function_sum_amount_discount
            },
            "taxBreakdowns": [
            ],
            "metadata": [],
            "customFields": [],
            "meterReading": [],
            # "invoiceFile": {
            #     "fileContent": "RmlsZSBi4bqjbmcga8OqIMSRxrDhu6NjIGFkZCBsw6puIHThuqFpIHBo4bqnbiBs4bqtcCBow7NhIMSRxqFu",
            #     "fileType": "1"
            # }
        }

        buyer_tax_code = invoice.x_partner_tax_code.strip() if invoice.x_partner_tax_code else ''

        if self.validate_tax_code(buyer_tax_code):
            data['buyerInfo']['buyerTaxCode'] = buyer_tax_code
        else:
            # note = u'Người mua không cung cấp mã số thuế'
            note = buyer_tax_code
            data['metadata'].append({
                "invoiceCustomFieldId": 951,
                "keyTag": "note",
                "valueType": "text",
                "keyLabel": "ghi chú",
                "stringValue": note
            })
        if invoice.x_origin:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 954,
                                        "keyTag": "orderPaper",
                                        "valueType": "text",
                                        "keyLabel": "phiếu giao hàng",
                                        "stringValue": invoice.x_origin
                                    })

        if invoice.x_sale_order_origin:
            data['metadata'].append({
                                        "invoiceCustomFieldId": 953,
                                        "keyTag": "orderNo",
                                        "valueType": "text",
                                        "keyLabel": "đơn đặt hàng",
                                        "stringValue": invoice.x_sale_order_origin
                                    })

        if invoice.payment_term_id:
            payment_method_name = invoice.payment_term_id.name if invoice.payment_term_id else ''
            data['metadata'].append({
                                        "invoiceCustomFieldId": 1681,
                                        "keyTag": "paymentDes",
                                        "valueType": "text",
                                        "keyLabel": "diễn giải hình thức thanh toán",
                                        "stringValue": payment_method_name
                                    })



        if adjustmentInvoiceType != 0:
            data['generalInvoiceInfo']['adjustmentInvoiceType'] = adjustmentInvoiceType
            data['generalInvoiceInfo']['originalInvoiceId'] = invoice.x_origin_invoice
            data['generalInvoiceInfo']['originalInvoiceIssueDate'] = origin_invoice.x_created_sinvoice.date().strftime('%Y-%m-%d')
            data['generalInvoiceInfo']['additionalReferenceDesc'] = u'Điều Chỉnh'
            data['generalInvoiceInfo']['additionalReferenceDate'] = datetime.strftime(datetime.now(), '%Y-%m-%d')

            if adjustmentInvoiceType == 1:
                is_total_amount_pos = False
                is_total_tax_amount_pos = False
                is_total_amt_without_tax_pos = False
                is_discount_amt_pos = False
                if invoice.type == 'out_invoice':
                    is_total_amount_pos = True
                    is_total_tax_amount_pos = True
                    is_total_amt_without_tax_pos = True
                    is_discount_amt_pos = True

                data['summarizeInfo']['isTotalAmountPos'] = is_total_amount_pos
                data['summarizeInfo']['isTotalTaxAmountPos'] = is_total_tax_amount_pos
                data['summarizeInfo']['isTotalAmtWithoutTaxPos'] = is_total_amt_without_tax_pos
                data['summarizeInfo']['isDiscountAmtPos'] = is_discount_amt_pos

        index = 0
        sumOfTotalLineAmountWithoutTax = 0
        total_discount = 0
        for line in invoice.invoice_line_ids:
            index += 1
            itemTotalAmountWithoutTax = round(line.price_unit * line.quantity)
            sumOfTotalLineAmountWithoutTax += itemTotalAmountWithoutTax
            total_discount += line.total_amount_discount_line
            item = {
                     "lineNumber": index,
                     "itemCode": line.product_id.default_code if line.product_id and line.product_id.default_code else '',
                     # "itemName": (line.name if line.name else '') + (u'(Hàng khuyến mại không thu tiền)' if line.x_total_price == 0 else ''),
                     "itemName": (line.name if line.name else ''),
                     "unitName": line.uom_id.name if line.uom_id else '',
                     "unitPrice": line.price_unit,
                     "quantity": line.quantity,
                     # "itemTotalAmountWithoutTax": line.x_functional_price_subtotal,
                     "itemTotalAmountWithoutTax": itemTotalAmountWithoutTax,
                     "itemTotalAmountWithTax": round(line.x_total_price),
                     # "itemTotalAmountAfterDiscount": itemTotalAmountWithoutTax - line.total_amount_discount_line,
                     'itemTotalAmountAfterDiscount': line.x_functional_price_subtotal,
                     # "taxPercentage": round(line.x_rounding_price_tax / line.x_functional_price_subtotal * 100) if line.x_functional_price_subtotal > 0 else 0,
                     "taxAmount": round(line.x_rounding_price_tax),
                     "discount": line.discount,
                     "discount2": line.discount2,
                     "itemDiscount": line.total_amount_discount_line,
                     "itemNote": "",
                     "batchNo": line.x_lot_id.name if line.x_lot_id else '',
                     "expDate": line.x_lot_id.removal_date.strftime('%d-%m-%Y ') if line.x_lot_id else '',
                  }

            # get taxPercentage
            if line.invoice_line_tax_ids:
                for tax in line.invoice_line_tax_ids:
                    if tax.name == 'Hàng không chịu thuế':
                        item['taxPercentage'] = -2
                    else:
                        item['taxPercentage'] = int(tax.amount)

            if adjustmentInvoiceType == 1:
                account_invoice_line_model = self.env['account.invoice.line'].sudo()
                origin_line = account_invoice_line_model.search([('invoice_id', '=', origin_invoice.id),('product_id','=',line.product_id.id)])

                if len(origin_line.ids) > 0:
                    adjustment_tax_amount = line.x_rounding_price_tax - origin_line.x_rounding_price_tax
                    item['adjustmentTaxAmount'] = abs(adjustment_tax_amount)
                    if adjustment_tax_amount < 0:
                        item['isIncreaseItem'] = False
                    else:
                        item['isIncreaseItem'] = True

            data['itemInfo'].append(item)
        data['summarizeInfo']['totalAmountWithoutTax'] = sumOfTotalLineAmountWithoutTax
        data['summarizeInfo']['discountAmount'] = total_discount

        data['metadata'].append({
            "invoiceCustomFieldId": 1721,
            "keyTag": "discountVAT",
            "valueType": "number",
            "keyLabel": "VAT CK",
            "numberValue": invoice.function_sum_amount_discount - total_discount
        })
        data['metadata'].append({
            "invoiceCustomFieldId": 1681,
            "keyTag": "discounttotal",
            "valueType": "number",
            "keyLabel": "Tiền thuế CK",
            "numberValue": invoice.function_sum_amount_discount
        })


        # compute taxBreakdowns
        # account_invoice_tax_model = self.env['account.invoice.tax']
        # taxs = account_invoice_tax_model.search([('invoice_id', '=', invoice.id)])
        for tax in invoice.tax_line_ids:
            item = {
                # 'taxPercentage': int(tax.tax_id.amount),
                'taxableAmount': tax.base,
                'taxAmount': tax.amount,
            }

            if tax.name == 'Hàng không chịu thuế':
                item['taxPercentage'] = -2
            else:
                item['taxPercentage'] = int(tax.tax_id.amount)

            data['taxBreakdowns'].append(item)

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
            # base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            # base64string = base64.encodebytes(str.encode('%s:%s' % (username, password)))
            base64string = base64.b64encode(bytes(username + ':' + password, "utf-8"))
            headers['Authorization'] = "Basic %s" % base64string.decode("utf-8")
            url = self.env['ir.config_parameter'].sudo().get_param('z_sinvoice_for_dap.sinvoice_create_uri')
            data = {}
            if invoice.x_origin_invoice:
                origin_invoice = self.env['account.invoice'].search([('supplier_invoice_number','=',invoice.x_origin_invoice)], order='id asc')
                if len(origin_invoice.ids) > 0:
                    if invoice.x_functional_amount_total != origin_invoice[0].x_functional_amount_total:
                        data = self.generate_invoice_data(invoice=invoice, adjustment_type=5, username=username, adjustmentInvoiceType=1, origin_invoice=origin_invoice[0])
                    else:
                        data = self.generate_invoice_data(invoice=invoice, adjustment_type=5, username=username, adjustmentInvoiceType=2, origin_invoice=origin_invoice[0])
            else:
                data = self.generate_invoice_data(invoice=invoice, adjustment_type=1, username=username, adjustmentInvoiceType=0)

            _logger.info('Hoa don %s : %s', str(invoice.id), json.dumps(data))
            result = requests.post(url, data=json.dumps(data), headers=headers)

            if self.verify_return_code(result.status_code) == 200:
                output = result.json()
                if 'errorCode' in output and output['errorCode'] != None:
                    raise ValidationError('invoice id (' + str(invoice.id) + ')' + ': ' + str(output['errorCode']) + ": " + str(output['description']))
                else:
                    output_result = output['result']
                    values = {
                                'supplier_invoice_number': output_result['invoiceNo'][6:],
                                'x_transaction_id': output_result['transactionID'],
                                'x_invoice_status': 'status_created',
                                'x_created_sinvoice': datetime.now(),
                                'x_reservation_code': output_result['reservationCode']
                              }
                    invoice.write(values)
                    self.env.cr.commit()

    @api.multi
    def show_hddt_data(self):
        user_obj = self.env.user
        username = user_obj.x_sinvoice_username
        for invoice in self:
            data = self.generate_invoice_data(invoice=invoice, adjustment_type=1, username=username, adjustmentInvoiceType=0)
            raise ValidationError(json.dumps(data))


    @api.multi
    def cancel_hddt(self):
        user_obj = self.env.user
        username = user_obj.x_sinvoice_username
        password = user_obj.x_sinvoice_password

        # headers = {"Content-type": "application/json"}
        headers = {}
        base64string = base64.b64encode(bytes(username + ':' + password, "utf-8"))
        headers['Authorization'] = "Basic %s" % base64string.decode("utf-8")

        for invoice in self:
            created_sinvoice_datetime = invoice.x_created_sinvoice.strftime('%Y%m%d%H%M%S')
            canceled_sinvoice_datetime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')

            # url = Constant.SINVOICE_CANCEL_URI + '?supplierTaxCode=' + Constant.SUPPLIER_TAX_CODE + '&templateCode='+invoice.x_template_symbol.code+'&invoiceNo='+invoice.x_invoice_no+'&additionalReferenceDesc=huy&additionalReferenceDate='+canceled_sinvoice_datetime+'&strIssueDate='+created_sinvoice_datetime
            # result = requests.get(url, headers)

            url = self.env['ir.config_parameter'].sudo().get_param('z_sinvoice_for_dap.sinvoice_cancel_uri')
            supplier_tax_code = self.env['ir.config_parameter'].sudo().get_param('z_sinvoice_for_dap.supplier_tax_code')
            data = {
                    "supplierTaxCode": supplier_tax_code,
                    "invoiceNo": invoice.x_invoice_symbol+invoice.supplier_invoice_number,
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
                        'supplier_invoice_number': False,
                        'x_transaction_id': False,
                        'x_reservation_code': False,
                        'x_invoice_status': 'status_canceled',
                        'x_canceled_sinvoice': datetime.now()
                    }
                    invoice.update(values)


class ZInvoiceInvoiceType(models.Model):
    _name = 'z.invoice.invoice.type'
    _description = 'Invoice Type'

    name = fields.Char(string=u'Tên', require=True)
    code = fields.Char(string=u'Mã', require=True)
    description = fields.Char(string=u'Mô tả')


class ZinvoiceCreateSinvoice(models.TransientModel):
    _name = "z.invoice.create.sinvoice.wizard"
    _description = "Create bulk sinvoice"

    def _default_invoice_ids(self):
        model_name = self._context.get('active_model')
        invoice_ids = self._context.get('active_ids')
        output = []
        records = self.env[model_name].browse(invoice_ids)
        for r in records:
            item = {'model': model_name, 'source_id': r.id}
            output.append((0, 0, item))
        return output

    invoice_ids = fields.One2many('z.invoice.create.sinvoice.line', 'wizard_id', string='Invoices', default=_default_invoice_ids)

    @api.multi
    def create_sinvoice(self):
        self.ensure_one()
        self.invoice_ids.create_sinvoice()
        return {'type': 'ir.actions.act_window_close'}


class ZinvoiceCreateSinvoiceLine(models.TransientModel):
    _name = 'z.invoice.create.sinvoice.line'
    _description = 'Invoice Line'

    wizard_id = fields.Many2one('z.invoice.create.sinvoice.wizard', string='Wizard', required=True, ondelete='cascade')
    # invoice_id = fields.Many2one('account.invoice', string='Invoice', ondelete='cascade', required=True)
    model = fields.Char(string='Model')
    source_id = fields.Integer(string='Ref')

    @api.multi
    def create_sinvoice(self):
        for line in self:
            record = self.env[line.model].browse(line.source_id)
            record.create_hddt()
