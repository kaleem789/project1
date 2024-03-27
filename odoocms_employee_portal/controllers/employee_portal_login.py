from odoo import http
from odoo.http import content_disposition, Controller, request, route


class Description(http.Controller):
    @http.route(['/employee/description'], type='http', auth="user", website=True, method=['GET'])
    def employee_description(self, **kw):
        return request.render("odoocms_employee_portal.employee_description", {
        })

class CataloguePrint(http.Controller):

    @http.route(['/report/pdf/catalogue_download'], type='http', auth='user', method=['GET', 'POST'])
    def download_catalogue(self, employee_id):
        pdf, _ = request.env.ref('odoocms_employee_portal.employee_action_report').sudo(). \
            render_qweb_pdf([int(employee_id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition', 'catalogue' + '.pdf;')]
        return request.make_response(pdf, headers=pdfhttpheaders)


class EmployeeLoginDashboard(http.Controller):
    @http.route(['/employee/dashboard'], type='http', auth="user", website=True, method=['GET'])
    def employee_home_new(self, **kw):
        payslip_id = request.env['hr.employee'].sudo().search([])
        current_user = http.request.env.user
        return request.render("odoocms_employee_portal.employee_reportsss", {
            'payslip_id': payslip_id,
            'current_user': current_user,

        })

        @http.route(['/employee/dashboard2'], type='http', auth="user", website=True, method=['GET', 'POST'])
        def employee_page(self, so, **kw):
            return request.render("odoocms_employee_portal.employee_portal_dashboard_page", {
                'emp': so
            })


class EmployeeReport(http.Controller):

    @http.route(['/employee/report'], type='http', auth="user", website=True, method=['POST'])
    def employee_report(self, **kw):
        current_user = http.request.env.user
        payslip_id = request.env['hr.employee'].sudo().search([])
        pays_id = request.env['hr.employee'].sudo().search([('current_user', '=', 'employee_id')])
        payslipppss_id = request.env['hr.payslip'].sudo().search([('current_user', '=', 'employee_id')])

        rule_id = request.env['hr.salary.rule'].sudo().search([])
        # docs = request.env['hr.employee'].browse(request.env.context.get('active_id'))
        # docs = pays_id
        datas = {
            'rule_id': rule_id,
            'pays_id': pays_id,
            'payslipppss_id': payslipppss_id,
            # 'docs': docs
        }
        return request.render("odoocms_employee_portal.employee_report_template", datas)


class EmployeeDetails(http.Controller):

    @http.route(['/employee/details'], type='http', auth="user", website=True, method=['GET', 'POST'])
    def employee_report(self, **kw):
        current_user = http.request.env.user
        payslip_id = request.env['hr.payslip'].sudo().search([('employee_id', '=', current_user.name),('state', '=', 'done')])

        return request.render("odoocms_employee_portal.employee_payslips_template",
                              {'payslip_id': payslip_id})


class LeavesEmployee(http.Controller):

    @http.route(['/leaves/details'], type='http', auth="user", website=True, method=['GET'])
    def leaves_details(self, **kw):
        current_user = http.request.env.user
        leaves_id = request.env['hr.leave'].sudo().search([('employee_id', '=', current_user.name),('state', '=', 'validate')])
        return request.render("odoocms_employee_portal.employee_leaves_template",
                              {'leaves_id': leaves_id,

                               }
                              )


class LeavesformSubmit(http.Controller):
    @http.route(['/leaves/form/submit/successfull'], type='http', auth="user", website=True, method=['GET'])
    def partner_form(self, **post):
        leaves_id = request.env['hr.leave.type'].sudo().search([])
        data = {
            'leaves_id': leaves_id,
        }
        print("emloyee form data 11", leaves_id)
        return request.render("odoocms_employee_portal.employee_leaves_form_submit", data)

    @http.route(['/leaves/form/submit'], type='http', auth="user", website=True, method=['POST'])
    def customer_form_submit(self, **post):
        holiday_status_id = post.get('leaves')
        date_from = post.get('date_from')
        date_to = post.get('date_to')
        name = post.get('name')
        duration_display = post.get('duration_display')
        leave_request = request.env['hr.leave'].sudo().create({
            'holiday_status_id': holiday_status_id,
            'date_from': date_from,
            'date_to': date_to,
            'name': name,
            'duration_display': duration_display,
        })
        return request.render("odoocms_employee_portal.tmp_customer_form_success", leave_request)


class LeavesTypes(http.Controller):

    @http.route(['/leaves/types'], type='http', auth="user", website=True, method=['GET'])
    def leaves_details(self, **kw):
        leaves_id = request.env['hr.leave.type'].sudo().search([])
        data = {
            'leaves_id': leaves_id,
        }
        return request.render("odoocms_employee_portal.tmp_customer_form", data)

    @http.route(['/customer/form/submit/new'], type='http', auth="user", website=True, method=['POST'])
    def customer_form_submit(self, **post):
        employee = request.env['hr.employee'].search([('name', '=', request.env.user.name)])
        fmt = '%Y-%m-%d'

        date_from = post.get('date_from')
        date_to = post.get('date_to')
        d1 = datetime.strptime(date_from, fmt)
        print(d1)
        d2 = datetime.strptime(date_to, fmt)
        print(d2)
        date_difference = (d2 - d1).days
        # date_difference = now.strftime("%d")

        a = request.env['hr.leave'].sudo().create({
            'employee_id': employee.id,
            'holiday_status_id': int(post.get('leaves_id')),
            # post.get['leaves_id'],
            'request_date_from': post.get('date_from'),
            'request_date_to': post.get('date_to'),
            'number_of_days': date_difference,
            'name': post.get('name'),
        })
        return request.redirect('/leaves/types')

class LeavesSummaryDetails(http.Controller):

    @http.route(['/leaves/summary/details'], type='http', auth="user", website=True, method=['GET', 'POST'])
    def leaves_form(self,  **post):
        current_user = http.request.env.user
        leaves_summary_id = request.env['hr.leave.allocation'].sudo().search([('employee_id', '=', current_user.name)])
        return request.render("odoocms_employee_portal.leaves_summary_details_template",
                              {'leaves_summary_id': leaves_summary_id,})


class AnnualSummaryDetails(http.Controller):

    @http.route(['/annual/leaves/summary'], type='http', auth="user", website=True, method=['GET', 'POST'])
    def get_sales(self, ):
        current_user = http.request.env.user
        annual_leaves_id = http.request.env['hr.employee'].sudo().search([])
        return request.render("odoocms_employee_portal.annual_leaves_summary_details_template",
                              {'annual_leaves_id': annual_leaves_id, })


class Employeedetails(http.Controller):

    @http.route(['/employee/main/details'], type='http', auth="user", website=True, method=['GET', 'POST'])
    def leaves_details(self, **kw):
        leaves_id = request.env['hr.employee'].sudo().search([])
        return "hello employees"


class LoanRequest(http.Controller):

    @http.route(['/loan/Leave/form'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def loan_form(self, **post):
        loan_id = request.env['hr.loan'].sudo().search([])

        data = {
            'name': loan_id,
        }
        return request.render("odoocms_employee_portal.loan_leave_request_form", data)
