#-*- coding:utf-8 -*-

from odoo import api, models
from datetime import datetime

class PayslipDetailsMonthlyReport(models.AbstractModel):
    _name = 'report.hr_payroll_community.report_payee_statement'
    _description = 'Payee Statement'
    
    
    def _get_applicable_month(self, date_from):
        dt_from = datetime.strptime(date_from, '%Y-%m-%d')
        return str(dt_from)

    
    def _get_payslip_lines(self, payslip_ids):
        result = {}
        lst = []
        cnt = 0
        emp_total_basic= 0.0
        for payslip_rec in payslip_ids:
            total = 0
            cnt += 1
#             result[payslip_rec.employee_id.id] = {'cnt':cnt,
#                                                   'emp_name':payslip_rec.employee_id.name,
#                                                   'postal_address': payslip_rec.employee_id.address_id.street,
#                                                   'postal_code': payslip_rec.employee_id.address_id.zip,
#                                                   'payroll_no': payslip_rec.number}
            if payslip_rec.employee_id.id in result:
                result[payslip_rec.employee_id.id].update({'cnt':cnt,
                                                  'emp_name':payslip_rec.employee_id.name,
                                                  'postal_address': payslip_rec.employee_id.address_id.street,
                                                  'postal_code': payslip_rec.employee_id.address_id.street2,
                                                  'payroll_no': payslip_rec.number})
            else:
                result[payslip_rec.employee_id.id] = {'cnt':cnt,
                                                  'emp_name':payslip_rec.employee_id.name,
                                                  'postal_address': payslip_rec.employee_id.address_id.street,
                                                  'postal_code': payslip_rec.employee_id.address_id.street2,
                                                  'payroll_no': payslip_rec.number}
            for line in payslip_rec.line_ids:
                if line.code == 'BASIC':
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'basic':line.total + result[line.slip_id.employee_id.id].get('basic',0.0)})
                    else:
                        result[line.slip_id.employee_id.id] = {'basic':line.total}
                    total += line.total
                    emp_total_basic += total
                elif line.code == 'GROSS':
                    if line.slip_id.employee_id.id in result:
#                     result[payslip_rec.employee_id.id].update({'gross':line.total})
                        result[line.slip_id.employee_id.id].update({'gross':line.total + result[line.slip_id.employee_id.id].get('gross',0.0)})
                    else:
                        result[line.slip_id.employee_id.id].update({'gross':line.total})
                    total += line.total
                elif line.code == 'ALW':
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'ha':line.total + result[line.slip_id.employee_id.id].get('ha',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'ha':line.total})
                    total += line.total
                elif line.code == 'MDC_PR':
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'ma':line.total + result[line.slip_id.employee_id.id].get('ma',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'ma':line.total})
                    total += line.total
                elif line.code == 'MDC_AD':
                    old_ma = 0.0
                    if result[payslip_rec.employee_id.id].get('ma'):
                        old_ma = result[payslip_rec.employee_id.id].get('ma')
                    result[payslip_rec.employee_id.id].update({'ma': old_ma + line.total})
                    total += line.total
                elif line.category_id.code == 'DED':
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'ded':line.total + result[line.slip_id.employee_id.id].get('ded',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'ded':line.total})
                    total += line.total
                elif line.code == 'LO':
                    result[payslip_rec.employee_id.id].update({'sa':line.total})
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
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'tax':line.total + result[line.slip_id.employee_id.id].get('tax',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'tax':line.total})
                elif line.code == 'PPF':
                    total += line.total
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'ppf':line.total + result[line.slip_id.employee_id.id].get('ppf',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'ppf':line.total})
                elif line.code == 'WCF_ADM':
                    total += line.total
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'wcf':line.total + result[line.slip_id.employee_id.id].get('wcf',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'wcf':line.total})
                elif line.code == 'WCF_PRG':
                    wcf_old = 0.0
                    if result[payslip_rec.employee_id.id].get('wcf'):
                        wcf_old = result[payslip_rec.employee_id.id].get('wcf')
                    total += line.total
                    result[payslip_rec.employee_id.id].update({'wcf': wcf_old + line.total})
                elif line.code == 'NET':
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'net':line.total + result[line.slip_id.employee_id.id].get('net',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'net':line.total})
                if line.category_id.code == 'ALW':
                    if line.name != 'House Allowance' or line.name != 'House Allowance.':
                        final_alw = 0.0
                        if result[payslip_rec.employee_id.id].get('alw'):
                            final_alw = result[payslip_rec.employee_id.id].get('alw') + line.total
                        else:
                            final_alw = line.total
                        result[payslip_rec.employee_id.id].update({'alw': final_alw})
                        total += line.total
                        
                if line.code == 'PAYEE':
                    if line.slip_id.employee_id.id in result:
                        result[line.slip_id.employee_id.id].update({'paye':line.total + result[line.slip_id.employee_id.id].get('paye',0.0)})
                    else:
                        result[payslip_rec.employee_id.id].update({'paye':line.total})
                    total += line.total
                if line.code == 'PAYEE-MOSE':
                    old_payee_1 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_1 = result[spayslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_1 + line.total})
                    total += line.total
                if line.code == 'PAYEE-SIAH':
                    old_payee_2 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_2 = result[payslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_2 +  line.total})
                    total += line.total
                if line.code == 'PAYEE-andrew':
                    old_payee_3 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_3 = result[payslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_3 + line.total})
                    total += line.total
                if line.code == 'PAYE -Andrew':
                    old_payee_4 = 0.0
                    if result[payslip_rec.employee_id.id].get('paye'):
                        old_payee_4 = result[payslip_rec.employee_id.id].get('paye')
                    result[payslip_rec.employee_id.id].update({'paye': old_payee_4+line.total})
                    total += line.total
            result[payslip_rec.employee_id.id].update({'total':round(total,2)})
#         result[payslip_rec.employee_id.id].update({'total_basic':emp_total_basic})
        return result



    @api.model
    def _get_report_values(self, docids, data=None):
        payslips = self.env['hr.payslip'].browse(data.get('ids'))
        
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'data': data,
            'get_lines':self._get_payslip_lines,
            'get_applicable_month': self._get_applicable_month,
        }