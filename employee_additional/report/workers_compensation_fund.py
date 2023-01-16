#-*- coding:utf-8 -*-

from odoo import api, models

class PayslipDetailsReportWorkComp(models.AbstractModel):
    _name = 'report.hr_payroll_community.worker_compensation_report'
    _description = 'Worker compensation new'


    def _get_payslip_lines(self, payslip_ids):
        result = {}
        lst = []
        cnt = 0
        emp_total_basic= 0.0
        print ("payslip_ids", payslip_ids)
        for payslip_rec in payslip_ids:
            cnt += 1
            total_basic = 0
            total_gross = 0
            result[payslip_rec.employee_id.id] = { 'cnt':cnt,
                                                          'emp_id': payslip_rec.employee_id.identification_id,
                                                          'emp_name':payslip_rec.employee_id.name}
            for line in payslip_rec.line_ids:
                if line.code == 'BASIC':
                    result[payslip_rec.employee_id.id].update({'basic':line.total,
                                                          })
                elif line.code == 'GROSS':
                    result[payslip_rec.employee_id.id].update({'gross':line.total})
        return result

    def _get_total_basic(self, payslip_ids):
        total_basic= 0.0
        for payslip_rec in payslip_ids:
            for line in payslip_rec.line_ids:
                if line.code == 'BASIC':
                    total_basic += line.total
        return total_basic

    def _get_total_gross(self, payslip_ids):
        total_gross= 0.0
        for payslip_rec in payslip_ids:
            for line in payslip_rec.line_ids:
                if line.code == 'GROSS':
                    total_gross += line.total
        return total_gross
    
    def _get_total_gross_one_per(self, payslip_ids):
        total_gross= 0.0
        for payslip_rec in payslip_ids:
            for line in payslip_rec.line_ids:
                if line.code == 'GROSS':
                    total_gross += line.total
        total_gross = total_gross *1 /100
        return total_gross
    
    def _get_applicable_month(self, payslip_ids):
        applicable_month= ''
        for payslip_rec in payslip_ids:
            applicable_month = payslip_rec.date_from.strftime("%B") + ' '+str(payslip_rec.date_from.year)
        return applicable_month
    
    def _get_applicable_during(self, payslip_ids):
        applicable_during= ''
        for payslip_rec in payslip_ids:
            applicable_during =str(payslip_rec.date_from.year -1) +'/'+str(payslip_rec.date_from.year)
        return applicable_during
    
    @api.model
    def _get_report_values(self, docids, data=None):
        payslips = self.env['hr.payslip'].browse(data.get('ids'))
        print ("data", data)
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'data': data,
            'get_applicable_month': self._get_applicable_month,
            'get_applicable_during': self._get_applicable_during,
            'get_total_gross': self._get_total_gross,
            'get_total_basic': self._get_total_basic,
            'get_total_gross_one_per': self._get_total_gross_one_per,
            'get_lines': self._get_payslip_lines,
        }
