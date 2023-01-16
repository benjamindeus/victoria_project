# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeAdditional(http.Controller):
#     @http.route('/employee_additional/employee_additional', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_additional/employee_additional/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_additional.listing', {
#             'root': '/employee_additional/employee_additional',
#             'objects': http.request.env['employee_additional.employee_additional'].search([]),
#         })

#     @http.route('/employee_additional/employee_additional/objects/<model("employee_additional.employee_additional"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_additional.object', {
#             'object': obj
#         })
