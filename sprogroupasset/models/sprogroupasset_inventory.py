
from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT



class SprogroupassetInventoryEquipmentRel(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.inventory.equipment.rel'
    _description = 'Sprogroupasset Inventory Equipment Rel'
    _order = 'id'

    name = fields.Char('Name')
    inventory_id = fields.Many2one('sprogroupasset.inventory', 'Inventory')
    equipment_id = fields.Many2one('sprogroupasset.equipment', 'Equipment', required=True)
    description = fields.Html('Description')
    state = fields.Selection([('chua_kiem_ke', 'Non-Inventory'), ('du', 'Enough'), ('thieu', 'Not enough')], string='Inventory State',
                                    default="chua_kiem_ke")

    start_date = fields.Date('Start Date', compute = '_compute_start_date')
    end_date = fields.Date('End Date', compute = '_compute_end_date')

    @api.one
    @api.depends('inventory_id')
    def _compute_start_date(self):
        if(self.inventory_id):
            self.start_date = self.inventory_id.start_date
    @api.one
    @api.depends('inventory_id')
    def _compute_end_date(self):
        if(self.inventory_id):
            self.end_date = self.inventory_id.end_date
class SprogroupassetInventory(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.inventory'
    _description = 'Sprogroupasset Inventory'
    _inherit = ['mail.thread']
    _order = 'id'

    name = fields.Char('Name', required=True)
    user_id = fields.Many2one('res.users', string='Performer', track_visibility='onchange',default=lambda self: self.env.user)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    description = fields.Html('Description')
    equipment_rel_ids = fields.One2many('sprogroupasset.inventory.equipment.rel', 'inventory_id')
    category_id = fields.Many2one('sprogroupasset.equipment.category', string='Load equipment from equipment type',track_visibility='onchange')
    inventory_status_da_kiem_ke = fields.Char('Inventory Status Inventoried', compute='_compute_inventory_status')
    inventory_status_chua_kiem_ke = fields.Char('Inventory Status Non-Inventory', compute='_compute_inventory_status')
    inventory_status_du = fields.Char('Inventory Status Enough', compute='_compute_inventory_status')
    inventory_status_thieu = fields.Char('Inventory Status Not-Enough', compute='_compute_inventory_status')
    use_in_location = fields.Many2one('hr.department', string='Department')

    @api.one
    @api.depends('equipment_rel_ids')
    def _compute_inventory_status(self):
        if(self.equipment_rel_ids):
            chua_kiem_ke = 0
            du = 0
            thieu = 0
            for equipment_rel in self.equipment_rel_ids:
                if(equipment_rel.state == 'chua_kiem_ke'):
                    chua_kiem_ke = chua_kiem_ke + 1
                elif(equipment_rel.state == 'du'):
                    du = du + 1
                elif(equipment_rel.state == 'thieu'):
                    thieu = thieu + 1

            self.inventory_status_chua_kiem_ke = str(chua_kiem_ke) + ' / ' + str(len(self.equipment_rel_ids))
            self.inventory_status_da_kiem_ke = str(len(self.equipment_rel_ids) - chua_kiem_ke) + ' / ' + str(len(self.equipment_rel_ids))
            self.inventory_status_du = str(du) + ' / ' + str(len(self.equipment_rel_ids))
            self.inventory_status_thieu = str(thieu) + ' / ' + str(len(self.equipment_rel_ids))

        else :
            self.inventory_status = '0/0'

    # @api.onchange('category_id')
    def _onchange_category_id_bak(self):
        # self.equipment_rel_ids = [2,3,4]
        if(self.category_id):
            equipment_array = []
            for equipment_rel in self.equipment_rel_ids:
                new_rel = (0, 0, {
                    'state': 'chua_kiem_ke',
                    'equipment_id': equipment_rel.equipment_id.id,
                })

                equipment_array += [new_rel]

            equipments = self.env['sprogroupasset.equipment'].search([('category_id', '=', self.category_id.id)])

            for id in equipments.ids:

                new_rel = (0,0,{
                                            'state': 'chua_kiem_ke',
                                            'equipment_id': id,
                                        })
                if (new_rel not in equipment_array):
                    equipment_array += [new_rel]
            self.equipment_rel_ids=equipment_array

    @api.onchange('equipment_rel_ids')
    def _onchange_equipment_rel_ids(self):
        Change = True


    @api.multi
    def load_equipment(self):
        category_id = self.category_id
        use_in_location = self.use_in_location

        equipment_array = []

        # load previous selected
        # for equipment_rel in self.equipment_rel_ids:
        #     new_rel = (0, 0, {
        #         'state': 'chua_kiem_ke',
        #         'equipment_id': equipment_rel.equipment_id.id,
        #     })
        #
        #     equipment_array += [new_rel]

        data_search = []
        self.equipment_rel_ids = None
        if(category_id.id != False):
            data_search += [('category_id' , '=' ,category_id.id )]
        if (use_in_location.id != False):
            departmnet_array = self.get_department(use_in_location.id)
            data_search += [('use_in_location.id', 'in', departmnet_array)]

        equipments = self.env['sprogroupasset.equipment'].search(data_search)

        for id in equipments.ids:

            new_rel = (0, 0, {
                'state': 'chua_kiem_ke',
                'equipment_id': id,
            })
            if (new_rel not in equipment_array):
                equipment_array += [new_rel]

        self.equipment_rel_ids = equipment_array


    def get_department(self, parent_id):
        department_array = [parent_id]
        departments = self.env['hr.department'].search([('parent_id', '=', parent_id)])
        for department in departments:
            department_array += self.get_department(department.id)

        return department_array