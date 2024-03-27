from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class TravelRequests(models.Model):
    _name = "emp.travel.request"
    _description = "Employee Travelling Requests"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string="Employees", required=True)
    name = fields.Char(string="Name", )
    location = fields.Char(string="location", required=True, )
    date_to = fields.Date(string="End Date")
    date_from = fields.Date(string="From Date")
    state = fields.Selection(
        [('to_approve', 'To Approve'), ('approve', 'Approve'), ('refuse', 'Refuse')
         ], string='Status',
        default='to_approve')

    @api.onchange('date_to')
    def check_previous_date(self):
        current_date = datetime.today().date()
        for rec in self:
            if rec.date_to:
                if rec.date_to < current_date:
                    raise ValidationError("Selected today's Date >>>>>>>>>>>>>>")

    def button_to_approve(self):
        self.write({'state': "approve"})

    def button_refuse(self):
        self.write({'state': "refuse"})
