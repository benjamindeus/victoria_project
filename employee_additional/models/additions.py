from odoo import models, fields, _, api
import datetime
import calendar
from odoo.exceptions import UserError, ValidationError

class AdditionEmployeeInfo(models.Model):
    """ for additionaL infos such as tin, pspf and nssf """
    
    _inherit = "hr.employee"
    
    empl_id = fields.Char('Employee ID')
    nssf_number = fields.Char('NSSF NUMBER')
    nhif_number = fields.Char('NHIF NUMBER')
    tin_number = fields.Char('TIN NUMBER')
    has_nhif = fields.Boolean('NHIF')
    tasiwu = fields.Boolean('TASIWU')
    cowtu = fields.Boolean('COWTU')
    pspf_number = fields.Char('PSPF NUMBER')
    form_4_number = fields.Char('Form Four Index Number')
    helsb_line_ids = fields.One2many(
        'salary.helsb',
        'employee_id',
        string='HELSB',
    )
    bank_name=fields.Char(string="Bank Name")
    bank_account_number=fields.Char(string="Account Number")
    
    
    
class SalaryHelsb(models.Model):

    _name = 'salary.helsb'
    _description = 'Salary HELSB'

    name = fields.Char(
        string='Name',
    )

    date = fields.Date(
        string='Date',
        default=datetime.date.today()
    )
    
    amount = fields.Float(
        string='Amount',
    )

    balance_amt = fields.Float(
        string='Balance Amount',
    )
        
    employee_id = fields.Many2one('hr.employee', 'Employee')
    
    @api.onchange("amount")
    def onchange_amount(self):
        res = {}
        if self.amount:
            self.balance_amt = self.amount
            
            
# class HrContract(models.Model):
#     _inherit = 'hr.contract'
#     gross_amount = fields.Float(
#         string='Gross Salary',
#     )

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    def action_payslip_done(self):
        if self.loan_line_ids_ben:
            for rec1 in self.loan_line_ids_ben:
                rec1.paid = True
                # rec.paid = True
                rec1.loan_id._compute_loan_amount()
        if self.penalt_line_ids_ben:
            for rec2 in self.penalt_line_ids_ben:
                rec2.paid = True
                # rec.paid = True
                rec2.loan_id._compute_loan_amount()
            return super(HrPayslip, self).action_payslip_done()

    @api.depends('line_ids')
    def _salary_total(self):
        for rec in self:
            basic = 0.0
            gross = 0.0
            taxable = 0.0
            house_alw = 0.0
            medical = 0.0
            payee = 0.0
            sdl = 0.0
            nssf = 0.0
            nssf_emp = 0.0
            WCF_PRG = 0.0
            loan = 0.0
            tot_ded = 0.0
            net = 0.0
            ALW = 0.0
            MDC_PR = 0.0
            MDC_AD = 0.0
            ADSDL = 0.0
            PRSDL = 0.0
            AD_NSSF_EMPLOYER = 0.0
            WCF_ADM = 0.0
            HLB = 0.0
            TXD = 0.0
            LO = 0.0
            for line in rec.line_ids:
                basic += (line.code=='BASIC' and line.total) 
                gross += (line.code=='GROSS' and line.total) 
                taxable += (line.code=='TXB' and line.total) 
                house_alw += (line.code=='ALW' and line.total) 
#                 medical += (line.code=='MDC_AD' and line.total) 
                payee += (line.code=='PAYEE' and line.total) 
                sdl += (line.code=='PRSDL' and line.total) 
                nssf_emp += (line.code=='NSSF_EMPLOYEE' and line.total) 
                WCF_PRG += (line.code=='WCF_PRG' and line.total) 
                loan += (line.code=='LO' and line.total) 
                tot_ded += (line.code=='TXD' and line.total)
                net += (line.code=='NET' and line.total)
                ALW += (line.code=='ALW' and line.total)
                MDC_PR += (line.code=='MDC_PR' and line.total)
                MDC_AD += (line.code=='MDC_AD' and line.total)
                ADSDL += (line.code=='ADSDL' and line.total)
                PRSDL += (line.code=='PRSDL' and line.total)
                AD_NSSF_EMPLOYER += (line.code=='AD_NSSF_EMPLOYER' and line.total)
                WCF_ADM += (line.code=='WCF_ADM' and line.total)
                HLB += (line.code=='HLB' and line.total)
                LO += (line.code=='LO' and line.total)
            rec.basic = basic
            rec.gross = gross
            rec.taxable = taxable
            rec.house_alw = house_alw
#             rec.medical = medical
            rec.payee = payee
#             rec.sdl = sdl
            rec.nssf = nssf
            rec.nssf_emp = nssf_emp
#             rec.wcf = wcf
            rec.loan = loan
            rec.tot_ded = tot_ded
            rec.net = net
#             rec.ALW = ALW
            rec.MDC_PR = MDC_PR
            rec.MDC_AD = MDC_AD
            rec.ADSDL = ADSDL
            rec.PRSDL = PRSDL
            rec.AD_NSSF_EMPLOYER = AD_NSSF_EMPLOYER
            rec.WCF_ADM = WCF_ADM
            rec.HLB = HLB
            rec.WCF_PRG = WCF_PRG
            rec.LO = LO


    batch_state = fields.Selection(related='payslip_run_id.state', string='Batch State',)   
    basic = fields.Float(string='Basic', default=0.0,compute='_salary_total', )
    gross = fields.Float(string='Gross', default=0.0,compute='_salary_total', )
    taxable = fields.Float(string='Taxable', default=0.0,compute='_salary_total', )
    house_alw = fields.Float(string='ALW', default=0.0,compute='_salary_total',)
#     medical = fields.Float(string='Medical', default=0.0,compute='_salary_total', )
    payee = fields.Float(string='Payee', default=0.0,compute='_salary_total', )
#     sdl = fields.Float(string='SDL', default=0.0,compute='_salary_total', )
    nssf = fields.Float(string='NSSF', default=0.0,compute='_salary_total', )
    nssf_emp = fields.Float(string='NSSF_EMPLOYEE', default=0.0,compute='_salary_total', )
    WCF_PRG = fields.Float(string='WCF_PRG', default=0.0,compute='_salary_total', )
    loan = fields.Float(string='Loan', default=0.0,compute='_salary_total', )
    tot_ded = fields.Float(string='Total Deduction', default=0.0,compute='_salary_total', )
    net = fields.Float(string='Net', default=0.0,compute='_salary_total', )
#     ALW =  fields.Float(string='ALW', default=0.0,compute='_salary_total', )
    MDC_PR = fields.Float(string='Medical PR', default=0.0,compute='_salary_total', )
    MDC_AD = fields.Float(string='Medical AD', default=0.0,compute='_salary_total', )
    ADSDL = fields.Float(string='ADSDL', default=0.0,compute='_salary_total', )
    PRSDL = fields.Float(string='PRSDL', default=0.0,compute='_salary_total', )
    AD_NSSF_EMPLOYER = fields.Float(string='AD_NSSF_EMPLOYER', default=0.0,compute='_salary_total', )
    WCF_ADM = fields.Float(string='WCF_ADM', default=0.0,compute='_salary_total', )
    HLB = fields.Float(string='HELSB', default=0.0,compute='_salary_total', )
    LO = fields.Float(string='LO', default=0.0,compute='_salary_total', )
 
 
 
    def _penalt_payslip_total(self):
        penalt_amount = 0.0
        penalt_id = []
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            pass
        for rec in self:
            lon_obj = self.env['hr.penalt.ded'].search([('employee_id', '=', rec.employee_id.id), ('state', '=', 'approve')])
            for penalt in lon_obj:
                for loan_line in penalt.loan_lines:
                    # if rec.date_from <= loan_line.date <= rec.date_to and not loan_line.paid:
                    # ili ionekane kwenye slip
                    if rec.date_from <= loan_line.date <= rec.date_to:
                        penalt_amount += loan_line.amount
                        penalt_id.append(loan_line.id)
                        print(penalt_id)
                        print(f"ben")
            if penalt_id and penalt_amount > 0.0:
                rec.penalt_total = penalt_amount
                rec.penalt_line_ids_ben = penalt_id
            else:
                rec.penalt_total = 0.0
                rec.penalt_line_ids_ben = []

    # ,store=True i added this
    penalt_total = fields.Float(string='Misappropriation Total',compute='_penalt_payslip_total', default=0.0)
    penalt_line_ids_ben = fields.Many2many('hr.deduction.line', string="Many Arrea", help="Many Misappropriation",compute='_penalt_payslip_total'
                                          )
    # compute='_penalt_payslip_total'
    
    
    def _helsb_payslip_total(self):
        helsb_amount = 0.0
        for rec in self:
            helsb_data = self.env['salary.helsb'].search([
                    ('employee_id', '=', rec.employee_id and rec.employee_id.id),('date','!=',rec.date_from)],
                    order='id desc', limit=1)
            if helsb_data:
                for helsb in helsb_data:
                    if helsb and abs(helsb.balance_amt) > 0:
                        helsb_amount = abs(helsb.balance_amt)
                rec.helsb_payslip = helsb_amount
            else:
                rec.helsb_payslip=0.0


    helsb_payslip = fields.Float(string='HELSB', default=0.0,
                           compute='_helsb_payslip_total', )

    def _attedance_total(self):
        attedance_amount = 0.0
        for rec in self:
    
            att_data = self.env['custom.attendance'].search([
                    ('emp_id', '=', rec.employee_id.empl_id),
                    ('date', '>=', rec.date_from),
                    ('date', '<=', rec.date_to)],
                    order='id desc', limit=1)
            if att_data:
                for att in att_data:
                    if abs(att.no_of_days_worked) > 0:
                        attedance_amount = att.no_of_days_worked * 3500
            else:
                attedance_amount = 0.0

            rec.food_allowance = attedance_amount

        
    food_allowance = fields.Float(string='FOOD Allowance', default=0.0,
                           compute='_attedance_total', )

    # conveyance = fields.Float(related='employee_id.grade_id.conveyance', default=0.0,
    #                        string='Conveyance Allownce', )
    # medical = fields.Float(related='employee_id.grade_id.medical', default=0.0,
    #                        compute='Medical Allownce', )
        
    def compute_basic(self):
        basic_amount=0.0
        for rec in self:
            if rec.employee_id:
                att_data = self.env['custom.attendance'].search([
                    ('emp_id', '=', rec.employee_id.empl_id),
                    ('date', '>=', rec.date_from),
                    ('date', '<=', rec.date_to)],
                    order='id desc', limit=1)
                if att_data:
                    for att in att_data:
                        if abs(att.no_of_days_worked) > 0:
                            basic_amount = att.no_of_days_worked * rec.employee_id.contract_id.wage/int(calendar.monthrange(int(rec.date_from.year),rec.date_from.month)[1])
                        else:
                            basic_amount = 0.0
                else:
                    basic_amount = rec.employee_id.contract_id.wage
                    
            rec.basic_amount=basic_amount
    basic_amount = fields.Float(string="Basic", default=0.0,
                           compute='compute_basic', )
                
            
        
    def compute_sheet(self):
        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                           self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
            lines = [(0, 0, line) for line in self._get_payslip_lines(contract_ids, payslip.id)]
            payslip.write({'line_ids': lines, 'number': number})
            if payslip.employee_id:
                if payslip.employee_id and payslip.employee_id.helsb_line_ids:
                    helsb_data = self.env['salary.helsb'].search([
                    ('employee_id', '=', payslip.employee_id and payslip.employee_id.id)],
                    order='id desc', limit=1)
                    amt = 0
                    balance_amt = helsb_data.balance_amt
                    inst_amt = 0
                    if helsb_data:
                        # inst_amt = (payslip.contract_id.gross_amount*15)/100
                        # also ASA PAYROLL NEEDED AN UPDATES
                        inst_amt = (payslip.contract_id.wage*15)/100
                        amt_r = helsb_data.balance_amt - inst_amt
                        if amt_r >=0:
                            amt = amt_r
                        else:
                            amt = 0

                    if inst_amt > helsb_data.balance_amt:
                        inst_amt = balance_amt

                    helsb_data_old = self.env['salary.helsb'].search([('employee_id', '=', payslip.employee_id and payslip.employee_id.id),('date', '=', payslip.date_from)],order='id desc', limit=1)
                    if not helsb_data_old:
                        vals = {'name': payslip.name,
                                'date': payslip.date_from,
                                'amount': inst_amt,
                                'balance_amt': amt,
                                'employee_id': payslip.employee_id and payslip.employee_id.id,
                            }
                        self.env['salary.helsb'].create(vals)
        return True

    def action_payslip_cancel(self):
        if self.filtered(lambda slip: slip.state == 'done'):
            raise UserError(_("Cannot cancel a payslip that is done."))
        helsb_data = self.env['salary.helsb'].search([
                    ('employee_id', '=', self.employee_id and self.employee_id.id),
                    ('date', '=', self.date_from)],
                    order='id desc', limit=1)
        if helsb_data:
            helsb_data.unlink()
        return self.write({'state': 'cancel'})




class CompanyChanges(models.Model):
    _inherit=['res.company']
    
    tin=fields.Char(string="TIN NUMBER")