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

class PayslipSend(models.TransientModel):
    _name = 'payslip.send'
    _description = "Payslip Send Wizard"

    date_from = fields.Date(string='Date From', required=True, default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_to = fields.Date(string='Date To', required=True, default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))

    def send_payslips(self):
        employee_ids = self.env.context.get('active_ids')
        template = self.env.ref('hr_payroll_community.hr_payslip_views', raise_if_not_found=False)
        for obj in employee_ids:
            if template:
				# ilivyokuwa mwanzo
                # template.sudo().with_context(employee_id=obj, date_from=self.date_from, date_to=self.date_to).send_mail(obj, force_send=False)
                template.sudo().with_context(employee_id=obj, date_from=self.date_from, date_to=self.date_to).send_mail(obj, force_send=True)
        return self.env['wizard.message'].generated_message("Email sent successfully!!")

class WizardMessage(models.TransientModel):
	_name = "wizard.message"
	_description = "Message Wizard"

	text = fields.Text(string='Message')

	def generated_message(self,message,name='Message/Summary'):
		partial_id = self.create({'text':message}).id
		return {
			'name':name,
			'view_mode': 'form',
			'view_id': False,
			'view_type': 'form',
			'res_model': 'wizard.message',
			'res_id': partial_id,
			'type': 'ir.actions.act_window',
			'nodestroy': True,
			'target': 'new',
			'domain': '[]',
		}
