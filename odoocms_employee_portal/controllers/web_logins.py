# -*- coding: utf-8 -*-
from odoo import http, tools, _, SUPERUSER_ID
from odoo.http import content_disposition, Controller, request, route, dispatch_rpc

from odoo.addons.portal.controllers.web import Home


class MyWebsite(Home):
	@http.route(website=True, auth="public", sitemap=False)
	def web_login(self, redirect=None, *args, **kw):
		response = super(MyWebsite, self).web_login(redirect=redirect, *args, **kw)
		if not redirect and request.params['login_success']:
			user = request.env['res.users'].browse(request.uid)
			return request.redirect('/employee/dashboard')
			
			redirect = b'/web?' + request.httprequest.query_string
			return http.redirect_with_hash(redirect)
		return response
