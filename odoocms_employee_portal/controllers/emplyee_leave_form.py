from odoo import http
from odoo.http import request, route, Controller
from datetime import datetime


class PartnerForm(http.Controller):

    @http.route(['/customer/form'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def partner_form(self, **post):
        leaves_id = request.env['hr.leave.type'].sudo().search([])
        data = {
            'leaves_id': leaves_id,
        }
        return request.render("odoocms_employee_portal.tmp_customer_form", data)

    @http.route(['/customer/form/submit'], type='http', auth="user", website=True, method=['POST'], portal=True)
    def customer_form_submit(self, **post):
        employee = request.env['hr.employee'].sudo().search([('name', '=', request.env.user.name)])

        fmt = '%Y-%m-%d'

        date_from = post.get('date_from')
        date_to = post.get('date_to')
        d1 = datetime.strptime(date_from, fmt)
        d2 = datetime.strptime(date_to, fmt)
        date_difference = (d2 - d1).days + 1

        if not post['date_from'] == post.get('date_to'):
            request.env['hr.leave'].sudo().create({
                'employee_id': employee.id,
                'holiday_status_id': int(post.get('leaves_id')),
                'request_date_from': post.get('date_from'),
                'request_date_to': post.get('date_to'),
                'date_from': post.get('date_from'),
                'date_to': post.get('date_to'),
                'number_of_days': date_difference,
                'name': post.get('name'),
            })
        return request.render("odoocms_employee_portal.tmp_customer_form_success", )

    def date_function(self):
        fmt = '%Y-%m-%d'
        date_from = self.date_from
        date_to = self.date_to
        d1 = datetime.strptime(date_from, fmt)
        d2 = datetime.strptime(date_to, fmt)
        date_difference = d2 - d1

    @http.route(['/customer/back'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def back_customer_form(self, **post):
        return request.redirect('/customer/form')


class TestForm(http.Controller):

    @http.route(['/editleave/form'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def editleave_form(self, **post):
        leaves_id = request.env['hr.leave.type'].sudo().search([])
        data = {
            'leaves_id': leaves_id,
        }
        return request.render("odoocms_employee_portal.edit_leave_form", data)

    @http.route(['/editleave/form/successfull'], type='http', auth="user", website=True, method=['POST'], portal=True)
    def editleave_form_submit(self, **post):
        employee = request.env['hr.employee'].search([('name', '=', request.env.user.name)])
        fmt = '%Y-%m-%d'
        date_from = post.get('date_from')
        date_to = post.get('date_to')
        a = request.env['hr.leave'].sudo().create({
            'employee_id': employee.id,
            'holiday_status_id': int(post.get('leaves_id')),
            # post.get['leaves_id'],
            'request_date_from': post.get('date_from'),
            'request_date_to': post.get('date_to'),
            'number_of_days': post.get('name'),
            'name': post.get('name'),
        })
        return request.redirect('/editleave/form')
