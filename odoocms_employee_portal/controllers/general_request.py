from odoo import http
from odoo.http import content_disposition, Controller, request, route


class GeneralRequest(http.Controller):

    @http.route(['/general/Leave/form'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def general_form(self, **post):
        general_id = request.env['emp.general.request'].sudo().search([])
        data = {
            'general_id': general_id,
        }
        return request.render("odoocms_employee_portal.general_leave_form", data)

    @http.route(['/general/Leave/form/submit'], type='http', auth="user", website=True, method=['POST'], portal=True)
    def general_leave_form_submit(self, **post):
        general_id = post.get('general_id')
        description = post.get('description')
        date = post.get('date')

        b = request.env['genericc.req'].sudo().create({
            'generic_name': general_id,
            'description': description,
            'date': date,

        })
        return request.render("odoocms_employee_portal.general_leave_form_success", )


    @http.route(['/general/back'], type='http', auth="user", website=True, portal=True)
    def travel_back(self, **post):
        return request.redirect('/general/Leave/form')


class GenericRecordss(http.Controller):

    @http.route(['/generic/Leave/recss'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def generic_recs_form(self, **post):
        return request.render("odoocms_employee_portal.generic_leave_recs", )
