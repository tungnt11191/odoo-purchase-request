
from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class SprogroupassetProvideStage(models.Model):
    """ Model for case stages. This models the main stages of a Sprogroupasset Request management flow. """

    _name = 'sprogroupasset.provide.stage'
    _description = 'Sprogroupasset Provide Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    fold = fields.Boolean('Folded in Sprogroupasset Pipe')
    done = fields.Boolean('Request Done')
    provide_state = fields.Selection([('new', 'New Request'), ('requested', 'Requested'), ('approved', 'Approved'), ('rejected', 'Rejected')], string='Provide State')


class SprogroupassetProvideComponent(models.Model):
    _name = 'sprogroupasset.provide.component'
    _description = 'SPROGROUPasset Provide Component'

    name = fields.Char(required=True)
    provide_request_id = fields.Many2one('sprogroupasset.provide.request', string='ProvideRequest', copy=False)
    price = fields.Monetary('Price', required=True, default=0.0)
    description = fields.Html(string='Description')
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)


class SprogroupassetProvideRequest(models.Model):
    _name = 'sprogroupasset.provide.request'
    _inherit = ['mail.thread']
    _description = 'Sprogroupasset Provide Requests'
    _order = "id desc"

    @api.returns('self')
    def _default_stage(self):
        return self.env['sprogroupasset.provide.stage'].search([], limit=1)

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'stage_id' in init_values and self.stage_id.provide_state == 'new':
            return 'sprogroupasset.mt_provide_req_created'
        elif 'stage_id' in init_values and self.stage_id.sequence > 1:
            return 'sprogroupasset.mt_provide_req_status'
        return super(SprogroupassetProvideRequest, self)._track_subtype(init_values)

    name = fields.Char('Subjects', required=True)
    description = fields.Html('Description')
    request_date = fields.Date('Request Date', track_visibility='onchange',
                               help="Date requested for the sprogroupasset to happen" , readonly = True)

    rejected_date = fields.Date('Rejected Date', track_visibility='onchange',
                                help="Date requested for the sprogroupasset to happen"  , readonly = True)
    rejected_user_id = fields.Many2one('res.users', string='Rejected by', readonly=True)

    approved_date = fields.Date('Approved Date', help="Date the sprogroupasset was finished. ", readonly=True)
    approved_user_id = fields.Many2one('res.users', string='Approved by', readonly=True)

    owner_user_id = fields.Many2one('res.users', string='Created by', default=lambda s: s.env.uid , readonly = True)
    stage_id = fields.Many2one('sprogroupasset.provide.stage', string='Stage', track_visibility='onchange',
                               group_expand='_read_group_stage_ids', default=_default_stage)
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    color = fields.Integer('Color Index')
    archive = fields.Boolean(default=False, help="Set archive to true to hide the sprogroupasset request without deleting it.")
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    current_stage_provide_state = fields.Char(string='Provide State', compute='_compute_current_stage_provide_state' , store=True)
    attachment_ids = fields.Many2many('ir.attachment', 'sprogroupasset_provide_request_ir_attachments_rel', 'provide_request_id',
                                      'attachment_id',
                                      'Attachments')
    provide_component_ids = fields.One2many('sprogroupasset.provide.component', 'provide_request_id', string='Component')

    @api.one
    @api.depends('stage_id')
    def _compute_current_stage_provide_state(self):
        stage = self.env['sprogroupasset.provide.stage'].browse(self.stage_id.id)
        self.current_stage_provide_state = stage.provide_state

    @api.multi
    def archive_equipment_request(self):
        self.write({'archive': True})

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        onchange_stage_id = True

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.multi
    def reset_equipment_request(self):
        """ Reinsert the sprogroupasset request into the sprogroupasset pipe in the first stage"""
        first_stage_obj = self.env['sprogroupasset.provide.stage'].search([], order="sequence asc", limit=1)
        # self.write({'active': True, 'stage_id': first_stage_obj.id})
        self.write({'archive': False, 'stage_id': first_stage_obj.id})

    def is_sprogroupasset_manager(self, user):
        if(user and user.has_group('sprogroupasset.group_sprogroupasset_manager')):
            return True
        else:
            return False

    def is_provide_request_stage(self, stage_id, provide_state):
        stage = self.env['sprogroupasset.provide.stage'].browse(stage_id)
        return stage.provide_state == provide_state


    @api.multi
    def write(self, vals):
        current_user = self.env['res.users'].browse(self.env.context['uid'])

        if ('stage_id' in vals and self.is_provide_request_stage(vals.get('stage_id'), 'new')):
            if (self.is_provide_request_stage(self.stage_id.id, 'new')) : # check previous stage
                go = True
            elif(self.is_provide_request_stage(self.stage_id.id, 'requested')) : # check previous stage
                go = True
            else:
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False



        if ('stage_id' in vals and self.is_provide_request_stage(vals.get('stage_id'), 'requested')):


            if (not self.is_provide_request_stage(self.stage_id.id, 'new')) : # check previous stage
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False

            if (not self.is_sprogroupasset_manager(current_user) and self.owner_user_id != current_user):
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False

        if ('stage_id' in vals and self.is_provide_request_stage(vals.get('stage_id'), 'approved')):
            if (not self.is_provide_request_stage(self.stage_id.id, 'requested')) : # check previous stage
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False
            if (self.archive == True):
                raise ValidationError(u'Yeu cau da duoc huy!')
                return False
            if (not self.is_sprogroupasset_manager(current_user)):
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False


        if ('stage_id' in vals and self.is_provide_request_stage(vals.get('stage_id'), 'rejected')):
            if (not self.is_provide_request_stage(self.stage_id.id, 'requested')) : # check previous stage
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False
            if (not self.is_sprogroupasset_manager(current_user)):
                raise ValidationError(u'Ban khong co quyen thay doi!')
                return False


        res = super(SprogroupassetProvideRequest, self).write(vals)

        if(self.archive == True):
            Archive = True

        # after writing, all values is currrent values
        now = fields.Datetime.now()
        if self.stage_id.provide_state == 'new' and 'stage_id' in vals:
            stage_id = True
        elif self.stage_id.provide_state == 'requested' and 'stage_id' in vals:
            self.write({'request_date': fields.Date.today()})
        elif self.stage_id.provide_state == 'approved' and 'stage_id' in vals:
            self.write({'approved_date': fields.Date.today(), 'approved_user_id' : self.env.context['uid'] })
        elif self.stage_id.provide_state == 'rejected' and 'stage_id' in vals:
            self.write({'rejected_date': fields.Date.today() , 'rejected_user_id' : self.env.context['uid']})

        return res

    @api.multi
    def unlink(self):
        if self.stage_id.provide_state != 'new':
            raise ValidationError(_('You cannot delete'))
        return super(SprogroupassetProvideRequest, self).unlink()

    @api.multi
    def copy(self, default=None):
        raise ValidationError(_('You cannot copy'))

