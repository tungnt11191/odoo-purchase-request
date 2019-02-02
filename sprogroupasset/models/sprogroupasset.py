# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class SprogroupassetStage(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.stage'
    _description = 'Sprogroupasset Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Sprogroupasset Pipe')
    done = fields.Boolean('Request Done')


class SprogroupassetEquipmentCategory(models.Model):
    _name = 'sprogroupasset.equipment.category'
    _inherit = ['mail.alias.mixin', 'mail.thread']
    _description = 'Asset Category'

    @api.one
    @api.depends('equipment_ids')
    def _compute_fold(self):
        self.fold = False if self.equipment_count else True

    name = fields.Char('Category Name', required=True, translate=True)
    technician_user_id = fields.Many2one('res.users', 'Responsible', track_visibility='onchange', default=lambda self: self.env.uid, oldname='user_id')
    color = fields.Integer('Color Index')
    note = fields.Text('Comments', translate=True)
    equipment_ids = fields.One2many('sprogroupasset.equipment', 'category_id', string='Equipments', copy=False)
    equipment_count = fields.Integer(string="Equipment", compute='_compute_equipment_count')
    sprogroupasset_ids = fields.One2many('sprogroupasset.request', 'category_id', copy=False)
    sprogroupasset_count = fields.Integer(string="Sprogroupasset", compute='_compute_sprogroupasset_count')
    alias_id = fields.Many2one(
        'mail.alias', 'Alias', ondelete='cascade', required=True,
        help="Email alias for this equipment category. New emails will automatically "
        "create new sprogroupasset request for this equipment category.")
    fold = fields.Boolean(string='Folded in Sprogroupasset Pipe', compute='_compute_fold', store=True)

    @api.multi
    def _compute_equipment_count(self):
        equipment_data = self.env['sprogroupasset.equipment'].read_group([('category_id', 'in', self.ids)], ['category_id'], ['category_id'])
        mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in equipment_data])
        for category in self:
            category.equipment_count = mapped_data.get(category.id, 0)

    @api.multi
    def _compute_sprogroupasset_count(self):
        sprogroupasset_data = self.env['sprogroupasset.request'].read_group([('category_id', 'in', self.ids)], ['category_id'], ['category_id'])
        mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in sprogroupasset_data])
        for category in self:
            category.sprogroupasset_count = mapped_data.get(category.id, 0)

    @api.model
    def create(self, vals):
        self = self.with_context(alias_model_name='sprogroupasset.request', alias_parent_model_name=self._name)
        if not vals.get('alias_name'):
            vals['alias_name'] = vals.get('name')
        category_id = super(SprogroupassetEquipmentCategory, self).create(vals)
        category_id.alias_id.write({'alias_parent_thread_id': category_id.id, 'alias_defaults': {'category_id': category_id.id}})
        return category_id

    @api.multi
    def unlink(self):
        MailAlias = self.env['mail.alias']
        for category in self:
            if category.equipment_ids or category.sprogroupasset_ids:
                raise UserError(_("You cannot delete an equipment category containing equipments or sprogroupasset requests."))
            MailAlias += category.alias_id
        res = super(SprogroupassetEquipmentCategory, self).unlink()
        MailAlias.unlink()
        return res

    def get_alias_model_name(self, vals):
        return vals.get('alias_model', 'sprogroupasset.equipment')

    def get_alias_values(self):
        values = super(SprogroupassetEquipmentCategory, self).get_alias_values()
        values['alias_defaults'] = {'category_id': self.id}
        return values


class SprogroupassetEquipment(models.Model):
    _name = 'sprogroupasset.equipment'
    _inherit = ['mail.thread']
    _description = 'SPROGROUP Equipment'

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'owner_user_id' in init_values and self.owner_user_id:
            return 'sprogroupasset.mt_mat_assign'
        return super(SprogroupassetEquipment, self)._track_subtype(init_values)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name and record.serial_no:
                result.append((record.id, record.name + '/' + record.serial_no))
            if record.name and not record.serial_no:
                result.append((record.id, record.name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('name', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    name = fields.Char('Equipment Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    technician_user_id = fields.Many2one('res.users', string='Technician', track_visibility='onchange', oldname='user_id')

    @api.one
    @api.depends('name')
    def _check_readonly_owner(self):
        current_user = self.env['res.users'].browse(self.env.context['uid'])
        self.is_manager = self.is_sprogroupasset_manager(current_user)

    is_manager = fields.Boolean(string='Is Manager?',compute = '_check_readonly_owner' )

    owner_user_id = fields.Many2one('res.users', string='Owner', track_visibility='onchange' )
    category_id = fields.Many2one('sprogroupasset.equipment.category', string='Category',
                                  track_visibility='onchange', group_expand='_read_group_category_ids')
    partner_id = fields.Many2one('res.partner', string='Vendor', domain="[('supplier', '=', 1)]")
    partner_ref = fields.Char('Vendor Reference')
    location = fields.Char('Location')
    model = fields.Char('Model')
    serial_no = fields.Char('Serial Number', copy=False)
    code = fields.Char('Code', copy=False)
    barcode = fields.Char('Barcode', copy=False)
    assign_date = fields.Date('Assigned Date', track_visibility='onchange' ,default=fields.Date.context_today)
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    cost = fields.Float('Cost')
    note = fields.Text('Note')
    warranty = fields.Date('Warranty')
    color = fields.Integer('Color Index')
    scrap_date = fields.Date('Scrap Date')
    sprogroupasset_ids = fields.One2many('sprogroupasset.request', 'equipment_id')
    sprogroupasset_count = fields.Integer(compute='_compute_sprogroupasset_count', string="Sprogroupasset", store=True)
    sprogroupasset_open_count = fields.Integer(compute='_compute_sprogroupasset_count', string="Current Sprogroupasset", store=True)
    period = fields.Integer('Days between each preventive sprogroupasset')
    next_action_date = fields.Date(compute='_compute_next_sprogroupasset', string='Date of the next preventive sprogroupasset', store=True)
    sprogroupasset_duration = fields.Float(help="Sprogroupasset Duration in minutes and seconds.")
    sprogroupasset_team_id = fields.Many2one('sprogroupasset.team', string='Team')
    asset_parent = fields.Many2one('sprogroupasset.equipment', string='Parent')
    asset_child = fields.One2many('sprogroupasset.equipment', 'asset_parent', string='Child', copy=False)
    guarantee_ids = fields.One2many('sprogroupasset.guarantee', 'equipment_id',string='Guarantee')
    borrow_state = fields.Selection([('available', 'Available'), ('transfering', 'Transfering'), ('unavailable', 'Unavailable')], string='Borrow State',
                                    default="available")
    attachment_ids = fields.Many2many('ir.attachment', 'sprogroupasset_equipment_ir_attachments_rel', 'equipment_id',
                                      'attachment_id',
                                      'Attachments')
    is_set = fields.Selection([('is_set', 'Is Set'), ('not_is_set', 'Not Is Set'), ('both', 'Both')],
                     string='Loai', default="both", compute = '_compute_is_set' , store = True)
    use_in_location = fields.Many2one('hr.department', string='Department', compute='_compute_department', store=True)
    department = fields.Many2one('hr.department', string='Department', compute='_compute_department2',search='_search_department')

    next_guarantee_date = fields.Date(compute='_compute_next_guarantee_date', string='Date of the next guarantee equipment', store=True)
    component_ids = fields.Many2many('sprogroupasset.equipment.component', 'sprogroupasset_equipment_component_rel', 'equipment_id',
                                      'component_id',
                                      'Components')
    vendor_id = fields.Many2one('sprogroupasset.vendor', string='Vendor')
    inventory_rel_ids = fields.One2many('sprogroupasset.inventory.equipment.rel', 'equipment_id', string ='Inventory')

    def _search_department(self, operator, value):
        departments = self.env['hr.department'].search([('name', operator, value)])

        department_array = []

        for department in departments :
            department_array += self.get_department(department.id)

        products = self.env['sprogroupasset.equipment'].search([('use_in_location.id', 'in', department_array)])


        return [('id', 'in', products.ids)]


    def get_department(self, parent_id):
        department_array = [parent_id]
        departments = self.env['hr.department'].search([('parent_id', '=', parent_id)])
        for department in departments:
            department_array += self.get_department(department.id)

        return department_array

    @api.one
    @api.depends('use_in_location')
    def _compute_department2(self):
        self.department = self.use_in_location

    @api.one
    @api.depends('guarantee_ids')
    def _compute_next_guarantee_date(self):
        guarantee = self.env['sprogroupasset.guarantee'].search([('equipment_id', '=', self.id)])
        if(len(guarantee.ids) > 0):
            self.next_guarantee_date = guarantee[-1].end_date
        else:
            self.next_guarantee_date = None

    @api.one
    @api.depends('owner_user_id')
    def _compute_department(self):
        # employee = self.env['hr.employee'].search([('user_id', '=', self.owner_user_id)])
        # if(len(employee) == 0):

        if(self.owner_user_id.id == False) :
            self.use_in_location = None
            return

        employee = self.env['hr.employee'].search([('work_email', '=', self.owner_user_id.email)])
        if (len(employee) > 0):
            self.use_in_location = employee[0].department_id.id
        else:
            self.use_in_location = None

    @api.one
    @api.depends('asset_child','asset_parent')
    def _compute_is_set(self):
        if((len(self.asset_child.ids) > 0)):
            self.is_set = 'is_set'
        elif(len(self.asset_child.ids) == 0 and (self.asset_parent.id == False)) :
            self.is_set = 'both'
        else:
            self.is_set = 'not_is_set'


    @api.depends('period', 'sprogroupasset_ids.request_date', 'sprogroupasset_ids.close_date')
    def _compute_next_sprogroupasset(self):

        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period > 0):
            next_sprogroupasset_todo = self.env['sprogroupasset.request'].search([
                ('equipment_id', '=', equipment.id),
                ('sprogroupasset_type', '=', 'preventive'),
                ('stage_id.done', '!=', True),
                ('close_date', '=', False)], order="request_date asc", limit=1)
            last_sprogroupasset_done = self.env['sprogroupasset.request'].search([
                ('equipment_id', '=', equipment.id),
                ('sprogroupasset_type', '=', 'preventive'),
                ('stage_id.done', '=', True),
                ('close_date', '!=', False)], order="close_date desc", limit=1)
            if next_sprogroupasset_todo and last_sprogroupasset_done:
                next_date = next_sprogroupasset_todo.request_date
                date_gap = fields.Date.from_string(next_sprogroupasset_todo.request_date) - fields.Date.from_string(last_sprogroupasset_done.close_date)
                # If the gap between the last_sprogroupasset_done and the next_sprogroupasset_todo one is bigger than 2 times the period and next request is in the future
                # We use 2 times the period to avoid creation too closed request from a manually one created
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period) * 2 and fields.Date.from_string(next_sprogroupasset_todo.request_date) > fields.Date.from_string(date_now):
                    # If the new date still in the past, we set it for today
                    if fields.Date.from_string(last_sprogroupasset_done.close_date) + timedelta(days=equipment.period) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(fields.Date.from_string(last_sprogroupasset_done.close_date) + timedelta(days=equipment.period))
            elif next_sprogroupasset_todo:
                next_date = next_sprogroupasset_todo.request_date
                date_gap = fields.Date.from_string(next_sprogroupasset_todo.request_date) - fields.Date.from_string(date_now)
                # If next sprogroupasset to do is in the future, and in more than 2 times the period, we insert an new request
                # We use 2 times the period to avoid creation too closed request from a manually one created
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period) * 2:
                    next_date = fields.Date.to_string(fields.Date.from_string(date_now)+timedelta(days=equipment.period))
            elif last_sprogroupasset_done:
                next_date = fields.Date.from_string(last_sprogroupasset_done.close_date)+timedelta(days=equipment.period)
                # If when we add the period to the last sprogroupasset done and we still in past, we plan it for today
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(fields.Date.from_string(date_now) + timedelta(days=equipment.period))

            equipment.next_action_date = next_date
    @api.one
    @api.depends('sprogroupasset_ids.stage_id.done')
    def _compute_sprogroupasset_count(self):
        self.sprogroupasset_count = len(self.sprogroupasset_ids)
        self.sprogroupasset_open_count = len(self.sprogroupasset_ids.filtered(lambda x: not x.stage_id.done))

    @api.onchange('category_id')
    def _onchange_category_id(self):
        self.technician_user_id = self.category_id.technician_user_id

    _sql_constraints = [
        ('serial_no', 'unique(serial_no)', "Another asset already exists with this serial number!"),
    ]


    def send_mail_to_manager(self,support_ids,default_res_model,default_res_id,message):
        if support_ids:
            support_partner_ids = support_ids.mapped('partner_id').ids
            support_partner_array_ids = []
            for support_id in support_partner_ids:
                support_partner_array_ids.append((4, support_id))
            if support_partner_ids:

                ctx = self.env.context.copy()
                ctx.update({
                    'default_res_model': default_res_model,
                    'default_res_id': default_res_id
                })
                mail_invite = self.env['mail.wizard.invite'].with_context(ctx).create({
                    'partner_ids': [support_partner_array_ids],
                    'message': message,
                    'send_mail': True
                })
                mail_invite.add_followers()

    def send_mail(self,reciptients, equipment):

        for reciptient in reciptients:
            sprogroupasset_mail = self.env['sprogroupasset.mail'].create({
                'email_subject': _('New equipment was created'),
                'email_to': reciptient.email,
                'equipment': equipment.id
            })
            sprogroupasset_mail.send_mail()

    @api.model
    def create(self, vals):
        res = super(SprogroupassetEquipment, self).create(vals)

        if(res):
            groups = self.env['res.groups'].search([('name', 'ilike', 'SPROGROUP Equipment Manager')])
            # send to assigned user
            self.send_mail(res.owner_user_id, res)

            for group in groups:
                users = group.users

                current_login_uid = self.env.context['uid']
                current_user = self.env['res.users'].browse(current_login_uid)
                message = _(
                    u'<div><p>Kính trình quý vị,</p><p>Quý vị được mời theo dõi tài sản "%s" bởi %s.<br/>Vui lòng nhấn vào liên kết để xem chi tiết.</p><p>Trân trọng!</p></div>') % (
                              res.name, current_user.name)
                self.send_mail_to_manager(users,res._name, res.id,message)

                # send to manager
                self.send_mail(users,res)

        return res

    def is_sprogroupasset_manager(self, user):
        if(user and user.has_group('sprogroupasset.group_sprogroupasset_manager')):
            return True
        else:
            return False


    def change_own(self, equipment_id , owner_user):
        equipment = self.env['sprogroupasset.equipment'].browse(equipment_id)
        now = fields.Datetime.now()

        if(owner_user == None):
            owner_user_id = None
            assign_date = None
            end_date = None
        else:
            owner_user_id = owner_user.id
            assign_date = now
            end_date = self.end_date
        equipment.write({'owner_user_id': owner_user_id })
        equipment.write({'assign_date' :  assign_date})
        equipment.write({'end_date' :  end_date})

        for child_equipment in equipment.asset_child:
            child_equipment.write({'owner_user_id': owner_user_id })
            child_equipment.write({'assign_date': assign_date})
            child_equipment.write({'end_date': end_date})

    @api.multi
    def write(self, vals):

        current_user = self.env['res.users'].browse(self.env.context['uid'])
        if(len(vals) > 1 and not self.is_sprogroupasset_manager(current_user)):
            raise ValidationError(u'Ban khong co quyen thay doi!')
            return False
        elif(len(vals) == 1  and not self.is_sprogroupasset_manager(current_user)):
            if('borrow_state' in vals  ):
                go = True
            elif ('assign_date' in vals):
                go = True
            elif ('end_date' in vals):
                go = True
            elif ('owner_user_id' in vals):
                go = True
            else:
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False

        res =  super(SprogroupassetEquipment, self).write(vals)

        for child_equipment in self.asset_child:
            child_equipment.write({'owner_user_id': self.owner_user_id.id})
            child_equipment.write({'assign_date': self.assign_date})
            child_equipment.write({'end_date': self.end_date})

        return res
    @api.model
    def _read_group_category_ids(self, categories, domain, order):
        """ Read group customization in order to display all the categories in
            the kanban view, even if they are empty.
        """
        category_ids = categories._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return categories.browse(category_ids)

    def _create_new_request(self, date):
        self.ensure_one()
        self.env['sprogroupasset.request'].create({
            'name': _('Preventive Sprogroupasset - %s') % self.name,
            'request_date': date,
            'schedule_date': date,
            'category_id': self.category_id.id,
            'equipment_id': self.id,
            'sprogroupasset_type': 'preventive',
            'owner_user_id': self.owner_user_id.id,
            'technician_user_id': self.technician_user_id.id,
            'sprogroupasset_team_id': self.sprogroupasset_team_id.id,
            'duration': self.sprogroupasset_duration,
            })

    @api.model
    def _cron_generate_requests(self):
        """
            Generates sprogroupasset request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period', '>', 0)]):
            next_requests = self.env['sprogroupasset.request'].search([('stage_id.done', '=', False),
                                                    ('equipment_id', '=', equipment.id),
                                                    ('sprogroupasset_type', '=', 'preventive'),
                                                    ('request_date', '=', equipment.next_action_date)])
            if not next_requests:
                equipment._create_new_request(equipment.next_action_date)

class SprogroupassetRequest(models.Model):
    _name = 'sprogroupasset.request'
    _inherit = ['mail.thread']
    _description = 'Sprogroupasset Requests'
    _order = "id desc"

    @api.returns('self')
    def _default_stage(self):
        return self.env['sprogroupasset.stage'].search([], limit=1)

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'stage_id' in init_values and self.stage_id.sequence <= 1:
            return 'sprogroupasset.mt_req_created'
        elif 'stage_id' in init_values and self.stage_id.sequence > 1:
            return 'sprogroupasset.mt_req_status'
        return super(SprogroupassetRequest, self)._track_subtype(init_values)

    def _get_default_team_id(self):
        return self.env.ref('sprogroupasset.equipment_team_sprogroupasset', raise_if_not_found=False)

    name = fields.Char('Subjects', required=True)
    description = fields.Html('Description')
    request_date = fields.Date('Request Date', track_visibility='onchange', default=fields.Date.context_today,
                               help="Date requested for the sprogroupasset to happen")
    owner_user_id = fields.Many2one('res.users', string='Created by', default=lambda s: s.env.uid)
    category_id = fields.Many2one('sprogroupasset.equipment.category', related='equipment_id.category_id', string='Category', store=True, readonly=True)
    equipment_id = fields.Many2one('sprogroupasset.equipment', string='Equipment', index=True)
    technician_user_id = fields.Many2one('res.users', string='Owner', track_visibility='onchange', oldname='user_id')
    stage_id = fields.Many2one('sprogroupasset.stage', string='Stage', track_visibility='onchange',
                               group_expand='_read_group_stage_ids', default=_default_stage)
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    color = fields.Integer('Color Index')
    close_date = fields.Date('Close Date', help="Date the sprogroupasset was finished. ")
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Cancelled'), ('done', 'Approved')],
                                    string='Kanban State', required=True, default='normal', track_visibility='onchange')
    # active = fields.Boolean(default=True, help="Set active to false to hide the sprogroupasset request without deleting it.")
    archive = fields.Boolean(default=False, help="Set archive to true to hide the sprogroupasset request without deleting it.")
    sprogroupasset_type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive')], string='Sprogroupasset Type', default="corrective")
    schedule_date = fields.Datetime('Scheduled Date', help="Date the sprogroupasset team plans the sprogroupasset.  It should not differ much from the Request Date. ")
    sprogroupasset_team_id = fields.Many2one('sprogroupasset.team', string='Team', required=True, default=_get_default_team_id)

    duration = fields.Float(help="Duration in minutes and seconds.")
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date', default=fields.Date.context_today)

    @api.multi
    def archive_equipment_request(self):
        self.write({'archive': True})

    @api.multi
    def reset_equipment_request(self):
        """ Reinsert the sprogroupasset request into the sprogroupasset pipe in the first stage"""
        first_stage_obj = self.env['sprogroupasset.stage'].search([], order="sequence asc", limit=1)
        # self.write({'active': True, 'stage_id': first_stage_obj.id})
        self.write({'archive': False, 'stage_id': first_stage_obj.id})


    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.equipment_id:
            if (self.equipment_id.owner_user_id):
                self.equipment_id = None
                return {
                    'warning': {
                        'title': 'Invalid value',
                        'message': 'This Equipment had been owned by other.'
                    }
                }

        if self.equipment_id:
            self.technician_user_id = self.equipment_id.technician_user_id if self.equipment_id.technician_user_id else self.equipment_id.category_id.technician_user_id
            self.category_id = self.equipment_id.category_id
            if self.equipment_id.sprogroupasset_team_id:
                self.sprogroupasset_team_id = self.equipment_id.sprogroupasset_team_id.id

    @api.onchange('category_id')
    def onchange_category_id(self):
        if not self.technician_user_id or not self.equipment_id or (self.technician_user_id and not self.equipment_id.technician_user_id):
            self.technician_user_id = self.category_id.technician_user_id

    @api.model
    def create(self, vals):
        # context: no_log, because subtype already handle this
        self = self.with_context(mail_create_nolog=True)
        request = super(SprogroupassetRequest, self).create(vals)
        if request.owner_user_id:
            request.message_subscribe(partner_ids=[request.owner_user_id.partner_id.id])
        if request.equipment_id and not request.sprogroupasset_team_id:
            request.sprogroupasset_team_id = request.equipment_id.sprogroupasset_team_id
        return request



    @api.multi
    def write(self, vals):
        # if self.stage_id == 2 or self.stage_id == 3:
        #     current_kanban_stage = self.kanban_state
        #     if(current_kanban_stage == 'done'):
        #         raise ValidationError(_('Cannot edit'))

        # Overridden to reset the kanban_state to normal whenever
        # the stage (stage_id) of the Sprogroupasset Request changes.
        if vals and 'kanban_state' not in vals and 'stage_id' in vals:
            vals['kanban_state'] = 'normal'
        if vals.get('owner_user_id'):
            owner_user = self.env['res.users'].sudo().browse(vals['owner_user_id'])
            self.message_subscribe(partner_ids=[owner_user.partner_id.id])
        res = super(SprogroupassetRequest, self).write(vals)
        if self.stage_id.done and 'stage_id' in vals:
            self.write({'close_date': fields.Date.today()})


        if vals and 'kanban_state' in vals :
            if(vals.get('kanban_state') == 'done'):
                if self.stage_id.id == 2:
                    self.change_own(self.equipment_id.id,self.owner_user_id )
                elif self.stage_id.id == 3:
                    self.change_own(self.equipment_id.id,None )
        return res

    def change_own(self, equipment_id , owner_user):
        equipment = self.env['sprogroupasset.equipment'].browse(equipment_id)

        if(owner_user == None):
            owner_user_id = None
        else:
            owner_user_id = owner_user.id
        equipment.write({'owner_user_id': owner_user_id})

        for child_equipment in equipment.asset_child:
            child_equipment.write({'owner_user_id': owner_user_id})


    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)


class SprogroupassetTeam(models.Model):
    _name = 'sprogroupasset.team'
    _description = 'Sprogroupasset Teams'

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', string='Subcontracting Partner')
    color = fields.Integer(default=0)
    request_ids = fields.One2many('sprogroupasset.request', 'sprogroupasset_team_id', copy=False)
    equipment_ids = fields.One2many('sprogroupasset.equipment', 'sprogroupasset_team_id', copy=False)

    # For the dashboard only
    todo_request_ids = fields.One2many('sprogroupasset.request', copy=False, compute='_compute_todo_requests')
    todo_request_count = fields.Integer(compute='_compute_todo_requests')
    todo_request_count_date = fields.Integer(compute='_compute_todo_requests')
    todo_request_count_high_priority = fields.Integer(compute='_compute_todo_requests')
    todo_request_count_block = fields.Integer(compute='_compute_todo_requests')

    @api.one
    @api.depends('request_ids.stage_id.done')
    def _compute_todo_requests(self):
        self.todo_request_ids = self.request_ids.filtered(lambda e: e.stage_id.done==False)
        self.todo_request_count = len(self.todo_request_ids)
        self.todo_request_count_date = len(self.todo_request_ids.filtered(lambda e: e.schedule_date != False))
        self.todo_request_count_high_priority = len(self.todo_request_ids.filtered(lambda e: e.priority == '3'))
        self.todo_request_count_block = len(self.todo_request_ids.filtered(lambda e: e.kanban_state == 'blocked'))

    @api.one
    @api.depends('equipment_ids')
    def _compute_equipment(self):
        self.equipment_count = len(self.equipment_ids)

class SprogroupassetGuarantee(models.Model):
    _name = 'sprogroupasset.guarantee'
    _description = 'Sprogroupasset guarantee'

    name = fields.Char(required=True)
    equipment_id = fields.Many2one('sprogroupasset.equipment', string='Equipment', copy=False)
    vendor_id = fields.Many2one('sprogroupasset.vendor', string='Vendor')
    assign_date = fields.Date(string='Assign Date')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    description = fields.Html(string='Description')


class SprogroupassetTransferStage(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.transfer.stage'
    _description = 'Sprogroupasset Transfer Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Sprogroupasset Pipe')
    done = fields.Boolean('Request Done')

class SprogroupassetRequestStage(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.request.stage'
    _description = 'Sprogroupasset Request Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Sprogroupasset Pipe')
    done = fields.Boolean('Request Done')

class SprogroupassetEquipmentComponent(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.equipment.component'
    _description = 'Sprogroupasset equipment Component'
    _order = 'category, id'

    name = fields.Char(required=True)
    equipment_ids = fields.Many2many('sprogroupasset.equipment', 'sprogroupasset_equipment_component_rel', 'component_id',
                                     'equipment_id',
                                     'Equipments')
    description = fields.Text(string='Description')
    category = fields.Many2one('sprogroupasset.equipment.component.category',string='Category')

class SprogroupassetEquipmentComponentCategory(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.equipment.component.category'
    _description = 'Sprogroupasset equipment Component Category'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence', default=20)
    description = fields.Text(string='Description')