from odoo import http,_
from odoo.http import content_disposition, Controller, request, route
from datetime import datetime


class TravelLeave(http.Controller):

    @http.route(['/travel/Leave/form'], csrf=False, type='http', auth="user", website=True, method=['GET'], portal=True)
    def travel_form(self, **post):
        employee_id = request.env['emp.travel.request'].sudo().search([])
        return request.render("odoocms_employee_portal.travel_leave_form" )

    @http.route(['/travel/Leave/form/submit'], csrf=False, type='http', auth="user", website=True, method=['POST'],
                portal=True)
    def travel_leave_form_submit(self, **post):
        date_from = post.get('date_from')
        date_to = post.get('date_to')
        current_user = http.request.env.user
        employee_id = request.env['emp.travel.request'].sudo().search([('employee_id', '=', current_user.name),('state', '=', 'approve')])
        values = request.params.copy()

        if date_to < date_from:
            return request.render("odoocms_employee_portal.travel_leave_form_error", values)

        b = request.env['emp.travel.request'].sudo().create({
            'employee_id': current_user.employee_id.id,
            'date_from': date_from,
            'date_to': date_to,
            'location': post.get("location"),
        })
        return request.render("odoocms_employee_portal.travel_leave_form_success", values)

    @http.route(['/travel/back'], type='http', auth="user", website=True, portal=True)
    def travel_back(self, **post):
        return request.redirect('/travel/Leave/form')

def date_function(self):
    fmt = '%Y-%m-%d'
    date_from = self.date_from
    date_to = self.date_to
    d1 = datetime.strptime(date_from, fmt)
    d2 = datetime.strptime(date_to, fmt)
    date_difference = d2 - d1


class TravelLeaveRecordss(http.Controller):

    @http.route(['/travel/Leave/recss'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def travel_recs_form(self, **post):
        return request.render("odoocms_employee_portal.travel_leave_recs", )
