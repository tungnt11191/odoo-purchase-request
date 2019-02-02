# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging
import xlrd
import tempfile
from xlrd import xlsx
import os
from odoo.tools.misc import xlwt

import io
from tempfile import TemporaryFile

import itertools
from odoo import api, fields, models, tools, _
from xlsxwriter.workbook import Workbook
_logger = logging.getLogger(__name__)

class SprogroupassetEquipmentExport(models.Model):
    _name = "sprogroupasset.equipment.export"
    _description = "Equipment Export"

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    file_name = fields.Char('File Name')
    file = fields.Binary('File')
    export_type = fields.Selection(
        [('equipment', 'Bang tong hop thiet bi'), ('cho_muon', 'Bang tong hop cho muon'), ('dieu_chuyen', 'Bang tong hop dieu chuyen'), ('provide', 'Bang tong hop cap Ts')],
        string='Loai Export',
        default="equipment")
    def print_excel_report(self):
        this = self[0]
        ctx = dict(self.env.context)
        filename = 'report.xls'

        if(this.export_type == 'equipment'):
            file_data = self.generate_equipment(this)
        elif(this.export_type == 'cho_muon'):
            file_data = self.generate_cho_muon_dieu_chuyen(this,'muon')
        elif(this.export_type == 'dieu_chuyen'):
            file_data = self.generate_cho_muon_dieu_chuyen(this,'dieu_chuyen')
        elif(this.export_type == 'provide'):
            file_data = self.generate_provide(this)

        this.write({ 'file': file_data, 'file_name': filename})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sprogroupasset.equipment.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def generate_equipment(self , export_date):
        if (export_date.start_date == False and export_date.end_date == False):
            equipments = self.env['sprogroupasset.equipment'].search([])
        elif (export_date.start_date == False and export_date.end_date != False):
            equipments = self.env['sprogroupasset.equipment'].search([('create_date', '<=', export_date.end_date)])
        elif (export_date.start_date != False and export_date.end_date == False):
            equipments = self.env['sprogroupasset.equipment'].search([('create_date', '>=', export_date.start_date)])
        else:
            equipments = self.env['sprogroupasset.equipment'].search(
                [('create_date', '>=', export_date.start_date), ('create_date', '<=', export_date.end_date)])

        workbook = xlwt.Workbook(encoding="UTF-8")

        worksheet = workbook.add_sheet('Equipment')

        style = xlwt.easyxf(
            'font:height 200, bold False, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')

        # Create header
        worksheet.write(0, 0, 'STT', style)
        worksheet.write(0, 1, _('Nguoi giu'), style)
        worksheet.write(0, 2, _('Ten'), style)
        worksheet.write(0, 3, _('Ma'), style)
        worksheet.write(0, 4, _('Ngay Giao'), style)
        worksheet.write(0, 5, _('Ngay Bh tiep'), style)
        worksheet.write(0, 6, _('Nha CC'), style)
        worksheet.write(0, 7, _('Note'), style)
        worksheet.write(0, 8, _('Phong Ban'), style)
        worksheet.write(0, 9, _('Su dung tai'), style)

        index = 1
        for equipment in equipments:
            worksheet.write(index, 0, index, style)

            if (equipment.owner_user_id.id != False):
                worksheet.write(index, 1, equipment.owner_user_id.name, style)

            if (equipment.name != False):
                worksheet.write(index, 2, equipment.name, style)

            if (equipment.code != False):
                worksheet.write(index, 3, equipment.code, style)

            if (equipment.assign_date != False):
                worksheet.write(index, 4, equipment.assign_date, style)

            if (equipment.next_guarantee_date != False):
                worksheet.write(index, 5, equipment.next_guarantee_date, style)

            if (equipment.vendor_id.id != False):
                worksheet.write(index, 6, equipment.vendor_id.name, style)

            if (equipment.note != False):
                worksheet.write(index, 7, equipment.note, style)

            if (equipment.use_in_location.id != False):
                worksheet.write(index, 8, equipment.use_in_location.name, style)

            if (equipment.location != False):
                worksheet.write(index, 9, equipment.location, style)

            component_index = 10
            for component in equipment.component_ids:
                worksheet.write(index, component_index, component.category.name + ': ' + component.name, style)
                component_index = component_index + 1

            index = index + 1

        fp = io.BytesIO()

        workbook.save(fp)
        fp.seek(0)
        file_data = base64.encodestring(fp.read())
        return file_data

    def generate_cho_muon_dieu_chuyen(self , export_date, borrow_type):
        if (export_date.start_date == False and export_date.end_date == False):
            borrow_requests = self.env['sprogroupasset.borrow.request'].search([('borrow_type', '=', borrow_type)])
        elif (export_date.start_date == False and export_date.end_date != False):
            borrow_requests = self.env['sprogroupasset.borrow.request'].search([('create_date', '<=', export_date.end_date),('borrow_type', '=', borrow_type)])
        elif (export_date.start_date != False and export_date.end_date == False):
            borrow_requests = self.env['sprogroupasset.borrow.request'].search([('create_date', '>=', export_date.start_date),('borrow_type', '=',borrow_type)])
        else:
            borrow_requests = self.env['sprogroupasset.borrow.request'].search(
                [('create_date', '>=', export_date.start_date), ('create_date', '<=', export_date.end_date),('borrow_type', '=', borrow_type)])

        workbook = xlwt.Workbook(encoding="UTF-8")

        worksheet = workbook.add_sheet('Equipment')

        style = xlwt.easyxf(
            'font:height 200, bold False, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')

        # Create header
        worksheet.write(0, 0, 'STT', style)
        worksheet.write(0, 1, _('Ngay Yeu Cau'), style)
        worksheet.write(0, 2, _('Nguoi Yeu Cau'), style)
        worksheet.write(0, 3, _('Ten TS'), style)
        worksheet.write(0, 4, _('Trang Thai'), style)

        index = 1
        for equipment in borrow_requests:
            worksheet.write(index, 0, index, style)

            if (equipment.request_date != False):
                worksheet.write(index, 1, equipment.request_date, style)

            if (equipment.owner_user_id.id != False):
                worksheet.write(index, 2, equipment.owner_user_id.name, style)

            if (equipment.equipment_id.id != False):
                worksheet.write(index, 3, equipment.equipment_id.name, style)

            if (equipment.stage_id.id != False):
                worksheet.write(index, 4, equipment.stage_id.name, style)

            index = index + 1

        fp = io.BytesIO()

        workbook.save(fp)
        fp.seek(0)
        file_data = base64.encodestring(fp.read())

        return file_data

    def generate_provide(self , export_date):
        if (export_date.start_date == False and export_date.end_date == False):
            borrow_requests = self.env['sprogroupasset.provide.request'].search([])
        elif (export_date.start_date == False and export_date.end_date != False):
            borrow_requests = self.env['sprogroupasset.provide.request'].search([('create_date', '<=', export_date.end_date)])
        elif (export_date.start_date != False and export_date.end_date == False):
            borrow_requests = self.env['sprogroupasset.provide.request'].search([('create_date', '>=', export_date.start_date)])
        else:
            borrow_requests = self.env['sprogroupasset.provide.request'].search([('create_date', '>=', export_date.start_date), ('create_date', '<=', export_date.end_date)])

        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet('Equipment')

        style = xlwt.easyxf(
            'font:height 200, bold False, name Arial; align: horiz center, vert center;borders: top medium,right medium,bottom medium,left medium')

        # Create header
        worksheet.write(0, 0, 'STT', style)
        worksheet.write(0, 1, _('Ngay Yeu Cau'), style)
        worksheet.write(0, 2, _('Nguoi Yeu Cau'), style)
        worksheet.write(0, 3, _('Ten TS'), style)
        worksheet.write(0, 4, _('Trang Thai'), style)

        index = 1
        for equipment in borrow_requests:
            worksheet.write(index, 0, index, style)

            if (equipment.request_date != False):
                worksheet.write(index, 1, equipment.request_date, style)

            if (equipment.owner_user_id.id != False):
                worksheet.write(index, 2, equipment.owner_user_id.name, style)

            if (equipment.name != False):
                worksheet.write(index, 3, equipment.name, style)

            if (equipment.stage_id.id != False):
                worksheet.write(index, 4, equipment.stage_id.name, style)

            index = index + 1

        fp = io.BytesIO()

        workbook.save(fp)
        fp.seek(0)
        file_data = base64.encodestring(fp.read())

        return file_data