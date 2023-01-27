
import babel
import calendar
from collections import defaultdict
from datetime import date, datetime, time
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
from pytz import utc

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, Warning



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'    
    
    prepare_by = fields.Many2many(related='company_id.prepare_by', readonly=False, relation='res.users', string='Prepared By',)   
    certified_by = fields.Many2many(related='company_id.certified_by', readonly=False, relation='res.users', string='Certified By',) 
    approved_by = fields.Many2many(related='company_id.approved_by', readonly=False, relation='res.users', string='Approved By',)
    usd_rate =  fields.Float(string='USD RATE',default=0.0)





class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('prepare', 'Prepared'),
    #     ('certified', 'Certified'),
    #     ('approved', 'Approved'),
    #     ('close', 'Close'),
    # ], string='Status', index=True, readonly=True, copy=False, default='draft')
#to prevente add batches of the same startin date / ending date after beeing approved ben added this
    
    @api.model
    def create(self,values):
        res=super(HrPayslipRun,self).create(values)
        google=self.env['hr.payslip.run'].search([('date_start','=',self.date_start),('date_end','=',self.date_end),('state','in',('draft','prepare'))])
        if google:
            raise UserError("You can not create another batch for the same start date/end date")
        return res
#to prevente deleteing of the bantch ben added this
    def unlink(self):
        for rec in self:
            if rec.state not in ['draft','prepare']:
                raise UserError("you can not delete this batch!!!")

            else:
                # to update the related payslips ben added this
                payslips=self.env['hr.payslip'].search([('payslip_run_id','=',self.id)])
                for payslip in payslips:
                    helsb_data = self.env['salary.helsb'].search([
                        ('employee_id', '=', payslip.employee_id and payslip.employee_id.id),
                        ('date', '=', rec.date_start)],
                        order='id desc', limit=1)
                    if helsb_data:
                        payslip.unlink()
                        helsb_data.unlink()
                    else:
                        payslip.unlink()
                return super(HrPayslipRun,self).unlink()
                # to update the related payslips ben added this





    p_user_id = fields.Many2one('res.users',string='Prepare By')
    c_user_id = fields.Many2one('res.users',string='Certified By')
    a_user_id = fields.Many2one('res.users',string='Approved By')
    usd_rate =  fields.Float(string='USD RATE',default=0.0)


    def draft_payslip_run(self):
        payslips = self.env['hr.payslip'].search([('payslip_run_id', '=', self.id)])
        for payslip in payslips:
            self.env['hr.payslip'].search([('id', '=', payslip.id)]).action_payslip_draft()

        return self.write({'state': 'draft','p_user_id':False,'c_user_id':False,'a_user_id':False})

    @api.model
    def create(self, vals):
        res = super(HrPayslipRun, self).create(vals)
        if 'slip_ids' in vals:
            template = self.env.ref('payroll_changes.payslip_batch_prepare_notification', raise_if_not_found=False)
            #company_id = self.env['res.company'].search([],limit=1)
            for p_user in self.env.user.company_id.prepare_by:
                if template and p_user.email:
                    template.with_context(self.env.context).send_mail(res.id, email_values={'email_to': p_user.email})
        return res

    def write(self, vals):
        res = super(HrPayslipRun, self).write(vals)
        if ('slip_ids' in vals or self.slip_ids) and self.state == 'draft':
            template = self.env.ref('payroll_changes.payslip_batch_prepare_notification', raise_if_not_found=False)
            #company_id = self.env['res.company'].search([],limit=1)
            for p_user in self.env.user.company_id.prepare_by:
                if template and p_user.email:
                    template.with_context(self.env.context).send_mail(self.id, email_values={'email_to': p_user.email})
        return res

    def prepare_payslip_batch(self):
        if self.env.user.id in self.env.user.company_id.prepare_by.ids:
            template = self.env.ref('payroll_changes.payslip_batch_certify_notification', raise_if_not_found=False)
            #company_id = self.env['res.company'].search([],limit=1)
            for c_user in self.env.user.company_id.certified_by:            
                if template and c_user.email:
                    template.with_context(self.env.context).send_mail(self.id, email_values={'email_to': c_user.email})
            return self.write({'state':'prepare','p_user_id':self.env.user.id})
        else:
            raise UserError('You are not allowed to Prepare Payslip Batch!')
         

    def certified_payslip_batch(self):
        if self.env.user.id in self.env.user.company_id.certified_by.ids:
            template = self.env.ref('payroll_changes.payslip_batch_approval_notification', raise_if_not_found=False)
            #company_id = self.env['res.company'].search([],limit=1)
            # to update the related payslips ben added this
            payslips=self.env['hr.payslip'].search([('payslip_run_id','=',self.id)])
            for payslip in payslips:
                payslip.write({'state':'verify'})
            # to update the related payslips ben added this
            for a_user in self.env.user.company_id.approved_by:   
                if template and a_user.email:
                    template.with_context(self.env.context).send_mail(self.id, email_values={'email_to': a_user.email})
            return self.write({'state':'certified','c_user_id':self.env.user.id})
        else:
            raise UserError('You are not allowed to Certify Payslip Batch!')

    def approve_payslip_batch(self):
        if self.env.user.id in self.env.user.company_id.approved_by.ids:
            # to update the related payslips ben added this
            payslips=self.env['hr.payslip'].search([('payslip_run_id','=',self.id)])
            for payslip in payslips:
                # transactions=super(HrPayslipRun, self).approve_payslip_batch()

                # payslip.write({'state':'done'})
                # i declared the above and now i commented it
                # self.ensure_one()
                self.env['hr.payslip'].search([('id', '=', payslip.id)]).action_payslip_done()
                payslip.write({'state':'done'})

                # transactionz=self.env['arrea.accounts'].search([('employee_id', '=', payslip.employee_id and payslip.employee_id.id),('arrea_end_date','>=', payslip.date_to),
                # ('arrea_end_date','<=', payslip.date_from)])
                # if transactionz:
                #     for transaction in transactionz:
                #         # self.env['arrea.accounts'].search([('id','=',transaction.id,)]).set_paid()
                #         self.env['arrea.accounts'].search([('id','=',transaction.id,)]).set_paid()
                #         self.env['arrea.accounts'].search([('id','=',transaction.id,)]).write({'state':'payed','status':'paid'})
                #
                #         transaction.write({'state':'payed','status':'paid'})


                #         transaction.set_paid()

    # def action_payslip_draft(self):




            # to update the related payslips ben added this
            return self.write({'state':'approved','a_user_id':self.env.user.id})
        else:
            raise UserError('You are not allowed to Approve Payslip Batch!')