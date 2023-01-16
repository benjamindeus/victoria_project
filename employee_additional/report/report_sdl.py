#-*- coding:utf-8 -*-

from odoo import api, models
from datetime import datetime


class PayslipDetailsMonthlyReport(models.AbstractModel):
    _name = 'report.hr_payroll_community.report_payroll_sdl'
    _description = 'Payslip report sdl'
    
    
    def _get_applicable_month(self, date_from):
        dt_from = datetime.strptime(date_from, '%Y-%m-%d')
        return str(dt_from)
#     

    def _get_total(self, payslip_ids, date_from, date_to):
        dict = {}
        result = self._get_payslip_lines(payslip_ids, date_from, date_to)
        c_gross = 0.0
        p_gross = 0.0
        total_emt_tzs = 0.0
        tzs_per = 0.0
        for key, value in result.items():
            if value.get('c_gross'):
                c_gross += value.get('c_gross')
            if value.get('p_gross'):
                p_gross += value.get('p_gross')
            if value.get('total_emt_tzs'):
                total_emt_tzs += value.get('total_emt_tzs')
            if total_emt_tzs:
                t = value.get('total_emt_tzs') *4.5/100
                tzs_per += t
        dict.update({'c_gross': c_gross,
                     'p_gross': p_gross,
                     'total_emt_tzs': total_emt_tzs,
                     'tzs_per':tzs_per})
        return dict
    
    def _get_payslip_lines(self, payslip_ids, date_from, date_to):
        result = {}
        lst = []
        cnt = 0
        emp_total_basic= 0.0
        d = datetime.strptime(date_to, "%Y-%m-%d")
        month_dict_6 = {}
        month_dict_12 = {}
        payslip_ids = self.env['hr.payslip'].browse(payslip_ids)
        date_from = [x.date_from for x in payslip_ids]
        for payslip_rec in payslip_ids:
            cnt += 1
            total = 0
            date_month = datetime.strftime(payslip_rec.date_to, "%Y-%m-%d")
            date_month_1 = datetime.strptime(date_month, "%Y-%m-%d")
            if d.month == 6:
                if payslip_rec.employee_id.empployee_type == 'casual':
                    if str(date_month_1.month) not in month_dict_6:
                        month_dict_6[date_month_1.month]= {'c_gross':0.0,
                                                   'p_gross': 0.0,'total_emt_tzs':0.0,}
                    for line in payslip_rec.line_ids:
                        if line.code == 'GROSS':
                            if str(date_month_1.month) in month_dict_6:
                                if 'c_gross' in month_dict_6[str(date_month_1.month)]:
                                    month_dict_6[str(date_month_1.month)]['c_gross'] += line.total
                                    month_dict_6[str(date_month_1.month)]['total_emt_tzs'] += line.total
                                else:
                                    month_dict_6[str(date_month_1.month)] = {'c_gross': line.total, 
                                                                'total_emt_tzs': line.total}
                            else:
                                month_dict_6[str(date_month_1.month)] = {'c_gross': line.total, 
                                                                'total_emt_tzs': line.total}
                else:
                    for line in payslip_rec.line_ids:
                        date_month = datetime.strftime(payslip_rec.date_to, "%Y-%m-%d")
                        date_month_1 = datetime.strptime(date_month, "%Y-%m-%d")                    
                        if line.code == 'GROSS':
                            if str(date_month_1.month) in month_dict_6:
                                if 'p_gross' in month_dict_6[str(date_month_1.month)]:
                                    month_dict_6[str(date_month_1.month)]['p_gross'] += line.total
                                    month_dict_6[str(date_month_1.month)]['total_emt_tzs'] += line.total
                                else:
                                    month_dict_6[str(date_month_1.month)] = {'c_gross': 0.0, 'p_gross': line.total,
                                                                         'total_emt_tzs': line.total}
                            else:
                                month_dict_6[str(date_month_1.month)] = {'p_gross': line.total, 
                                                                'total_emt_tzs': line.total}
            else:
                if payslip_rec.employee_id.empployee_type == 'casual':
                    if str(date_month_1.month) not in month_dict_12:
                        month_dict_12[date_month_1.month]= {'c_gross':0.0,
                                                   'p_gross': 0.0,'total_emt_tzs':0.0,}
                    for line in payslip_rec.line_ids:
                        date_month = datetime.strftime(payslip_rec.date_to, "%Y-%m-%d")
                        date_month_1 = datetime.strptime(date_month, "%Y-%m-%d")
                        if line.code == 'GROSS':
                            if str(date_month_1.month) in month_dict_12:
                                if 'c_gross' in month_dict_12[str(date_month_1.month)]:
                                    month_dict_12[str(date_month_1.month)]['c_gross'] += line.total
                                    month_dict_12[str(date_month_1.month)]['total_emt_tzs'] += line.total
                                else:
                                    month_dict_12[str(date_month_1.month)] = {'c_gross': line.total, 
                                                                'total_emt_tzs': line.total}
                            else:
                                month_dict_12[str(date_month_1.month)] = {'c_gross': line.total, 
                                                                'total_emt_tzs': line.total}
                else:
                    for line in payslip_rec.line_ids:
                        date_month = datetime.strftime(payslip_rec.date_to, "%Y-%m-%d")
                        date_month_1 = datetime.strptime(date_month, "%Y-%m-%d")                    
                        if line.code == 'GROSS':
                            if str(date_month_1.month) in month_dict_12:
                                if 'c_gross' in month_dict_12[str(date_month_1.month)]:
                                    month_dict_12[str(date_month_1.month)]['c_gross'] += line.total
                                    month_dict_12[str(date_month_1.month)]['total_emt_tzs'] += line.total
                                else:
                                    month_dict_12[str(date_month_1.month)] = {'c_gross': 0.0, 'p_gross': line.total,
                                                                         'total_emt_tzs': line.total}
                            else:
                                month_dict_12[str(date_month_1.month)] = {'p_gross': line.total, 
                                                                'total_emt_tzs': line.total}
        if d.month == 6:
            return month_dict_6
        else:
            return month_dict_12

    @api.model
    def _get_report_values(self, docids, data=None):
        payslips = self.env['hr.payslip'].browse(data.get('ids'))
        for payslip in payslips:
            if payslip.employee_id.gender=='male':
                data.update({'male':True})
            elif payslip.employee_id.gender=='female':
                data.update({'female':True})
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'get_applicable_month': self._get_applicable_month,
            'data': data,
            'get_lines':self._get_payslip_lines,
            'get_lines_total': self._get_total,
        }