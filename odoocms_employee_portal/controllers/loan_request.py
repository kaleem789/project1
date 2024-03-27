from odoo import http
from odoo.http import content_disposition, Controller, request, route


class Test(http.Controller):

    @http.route(['/test/Leave/form'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def test_form(self, **post):
        current_user = http.request.env.user
        employee_id = request.env['hr.loan'].sudo().search([('employee_id', '=', current_user.name),('state', '=', 'approve')])

        data = {
            'employee_id': employee_id,
        }
        return request.render("odoocms_employee_portal.test_leave_request_form", data)



    @http.route(['/test/Leave/form/submit'], type='http', auth="user", website=True, method=['POST'], portal=True)
    def test_submit(self, **post):
        date = post.get('date')
        loan_amount = post.get('loan_amount')
        installment = post.get('installment')
        current_user = http.request.env.user

        b = request.env['hr.loan'].sudo().create({
            'name': post.get('name'),
            'employee_id': current_user.employee_id.id,
            'date': date,
            'loan_amount': loan_amount,
            'installment': installment,
        })
        return request.render("odoocms_employee_portal.test_loan_leave_form_success", )


    @http.route(['/test/back'], type='http', auth="user", website=True, portal=True)
    def test_back(self, **post):
        return request.redirect('/test/Leave/form')


class LoanLeaveRecordss(http.Controller):

    @http.route(['/loan/Leave/recss'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def loan_recs_form(self, **post):
        return request.render("odoocms_employee_portal.loan_leaves_recs", )
