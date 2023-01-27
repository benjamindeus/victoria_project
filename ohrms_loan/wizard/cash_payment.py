# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2016 Webkul Software Pvt. Ltd.
# Author : www.webkul.com
#
##############################################################################

from odoo import api, fields, models, tools, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class LoanCashPay(models.TransientModel):
    _name = 'loan.cash.pay'
    _description = "cash Loan Payment"
    _order = 'id desc'


    date_paid = fields.Date(string="Received Date", required=True, default=lambda self: fields.Date.to_string(date.today()))
    loan_amount = fields.Float(string="Loan Amount", readonly=True,required=True, help="Loan amount")

	# date_to = fields.Date(string='Date To', required=True, default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    def cash_paymentxxx(self):
        idz=self.env.context.get('active_id')
        dataz=self.env['hr.loan'].search([('id','=',idz)],limit=1)
        for loan in dataz.loan_lines:
            if not loan.paid:
                loan.write({'paid':True,'paid_by':'cash'})
                dataz._compute_loan_amount()

        dataz.write({'state':'close'})
    # def send_payslips(self):
    #     employee_ids = self.env.context.get('active_ids')
    #     template = self.env.ref('hr_payroll_community.hr_payslip_views', raise_if_not_found=False)
    #     for obj in employee_ids:
    #         if template:
	# 			# ilivyokuwa mwanzo
    #             # template.sudo().with_context(employee_id=obj, date_from=self.date_from, date_to=self.date_to).send_mail(obj, force_send=False)
    #             template.sudo().with_context(employee_id=obj, date_from=self.date_from, date_to=self.date_to).send_mail(obj, force_send=True)
    #     return self.env['wizard.message'].generated_message("Email sent successfully!!")
