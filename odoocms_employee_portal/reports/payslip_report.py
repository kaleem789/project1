from odoo import api, models, fields, _


class ProductCatalogueReport(models.AbstractModel):
    _name = "report.odoocms_employee_portal.report_payslip"
    _description = "Portal Payslip Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        pay = self.env['hr.payslip'].browse(docids)
        return {
            'docs': pay,
            'data': data,
        }

    @api.model
    def _get_default_report_id(self):
        return self.env.ref('odoocms_employee_portal.employee_action_report', False)


class TestingPayslip(models.Model):
    _inherit = "hr.payslip"
