#-*- coding:utf-8 -*-

from odoo import api, models

class PayslipDetailsMonthlyReport(models.AbstractModel):
    _name = 'report.hr_payroll_community.report_payslip_approval'
    _description = 'Payslip Monthly Approval'
    
    
    def _get_applicable_month(self, payslip_ids):
        applicable_month= ''
        for payslip_rec in payslip_ids:
            applicable_month = payslip_rec.date_from.strftime("%B") + ' '+str(payslip_rec.date_from.year)
        return applicable_month

    def _get_prepared_by(self, payslip_ids):
        prepared_by = ''
        if payslip_ids:
            for rec in payslip_ids:
                if rec.payslip_run_id and rec.payslip_run_id.p_user_id:
                    prepared_by = rec.payslip_run_id.p_user_id.name
        return prepared_by
    
    def _get_ceruser_by(self, payslip_ids):
        ceruser_by = ''
        if payslip_ids:
            for rec in payslip_ids:
                if rec.payslip_run_id and rec.payslip_run_id.c_user_id:
                    ceruser_by = rec.payslip_run_id.c_user_id.name
        return ceruser_by

    def _get_approved_by(self, payslip_ids):
        approved_by = ''
        if payslip_ids:
            for rec in payslip_ids:
                if rec.payslip_run_id and rec.payslip_run_id.a_user_id:
                    approved_by = rec.payslip_run_id.a_user_id.name
        return approved_by
    
    def _get_payslip_lines(self, payslip_ids):
        result = {}
        lst = []
        cnt = 0
        emp_total_basic= 0.0
        
        payslip_ids = self.env['hr.payslip'].browse(payslip_ids)
        for payslip_rec in payslip_ids:
            cnt += 1
            total = 0
            result[payslip_rec.employee_id.id]= {'cnt':cnt,
                                                          'emp_name':payslip_rec.employee_id.name}
            for line in payslip_rec.line_ids:
                if line.code == 'LO':
                    print ("line.totalline.total", line.total)
                    result[payslip_rec.employee_id.id].update({'sa':line.total})
                    total += line.total
                if line.code == 'BASIC':
                    result[payslip_rec.employee_id.id].update({'basic':line.total,
                                                          })
                    total += line.total
                    emp_total_basic += total
                elif line.code == 'GROSS':
                    result[payslip_rec.employee_id.id].update({'gross':line.total})
                    total += line.total
                elif line.code == 'ALW':
                    result[payslip_rec.employee_id.id].update({'ha':line.total})
                    total += line.total
                elif line.code == 'MDC_PR':
                    result[payslip_rec.employee_id.id].update({'ma':line.total})
                    total += line.total
                elif line.code == 'MDC_AD':
                    old_ma = 0.0
                    if result[payslip_rec.employee_id.id].get('ma'):
                        old_ma = result[payslip_rec.employee_id.id].get('ma')
                    result[payslip_rec.employee_id.id].update({'ma': old_ma + line.total})
                    total += line.total
                elif line.code == 'PAYEE':
                    result[payslip_rec.employee_id.id].update({'paye':line.total})
                    total += line.total
                elif line.code == 'PAYEE-MOSE':
                    old_payee_1 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_1 = result[payslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_1 + line.total})
                    total += line.total
                elif line.code == 'PAYEE-SIAH':
                    old_payee_2 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_2 = result[payslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_2 +  line.total})
                    total += line.total
                elif line.code == 'PAYE -andrew':
                    old_payee_3 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_3 = result[payslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_3 + line.total})
                    total += line.total
                elif line.code == 'PAYE -Andrew':
                    old_payee_4 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_4 = result[payslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_4+line.total})
                    total += line.total
                elif line.code == 'ADSDL':
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'sdl':line.total})
                elif line.code == 'PRSDL':
                    old_sdl = 0.0
                    if result[payslip_rec.employee_id.id].get('sdl'):
                        old_sdl = result[payslip_rec.employee_id.id].get('sdl')
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'sdl': old_sdl + line.total})
                elif line.code == 'TXB':
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'tax':line.total})
                elif line.code == 'TXD':
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'deduction':line.total})
                elif line.name == 'NSSF':
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'ppf':line.total})
                elif line.code == 'WCF_ADM':
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'wcf':line.total})
                elif line.code == 'WCF_PRG':
                    wcf_old = 0.0
                    if result[payslip_rec.employee_id.id].get('wcf'):
                        wcf_old = result[payslip_rec.employee_id.id].get('wcf')
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'wcf': wcf_old + line.total})
                elif line.code == 'NET':
                    result[payslip_rec.employee_id.id].update({'net':line.total})
    
            result[payslip_rec.employee_id.id].update({'total':round(total, 2)})
#         result[payslip_rec.employee_id.id].update({'total_basic':emp_total_basic})
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        payslips = self.env['hr.payslip'].browse(data.get('ids'))
        print ("payslipspayslips", payslips)
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'get_applicable_month': self._get_applicable_month,
            'data': data,
            'get_lines':self._get_payslip_lines,
            'get_prepared_by': self._get_prepared_by,
            'get_ceruser_by': self._get_ceruser_by,
            'get_approved_by':self._get_approved_by
        }
