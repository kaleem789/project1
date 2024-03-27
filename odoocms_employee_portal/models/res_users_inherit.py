from odoo import fields, models,api


class FacultyUser(models.Model):
    _inherit = 'res.users'

    is_faculty = fields.Boolean(string='Is Faculty' , compute='_compute_faculty')

    def _compute_faculty(self):
        for rec in self:
            chk = False
            print("ppppppppp")
            faculty_member = self.env['odoocms.faculty.staff'].search([('user_id' ,'=' ,rec.id)])
            if faculty_member:
                chk = True
            rec.is_faculty = chk
