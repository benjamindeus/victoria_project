# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils



class HrPayslip(models.Model):
    _name = 'custom.attendance'
    _description = 'Custom Attendence'
    _order = 'id desc'

    emp_name = fields.Char(string='Employee Name')
    emp_id = fields.Char(string='Employee ID',required=True)
    date = fields.Date('Date',required=True)
    no_of_days_worked = fields.Float('No. Of Days worked',required=True)



