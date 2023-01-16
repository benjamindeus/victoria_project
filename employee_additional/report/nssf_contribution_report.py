# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, Warning
import base64
import io

class HrPaslip(models.Model):
     
    _inherit = 'hr.payslip'
     
    def nssf_report(self):
        print ("==========innnnnnnn")
        return self.env.ref(
            'hr_payroll_community.nssf_contribution_xlsx').report_action(self)

class NssfPayslipXlsx(models.AbstractModel):
    _name = 'report.hr_payslip.nssf_contribution_report'
#     _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, payslip_ids):
        
        print ("======payslip_ids",self, workbook, data, payslip_ids)
        worksheet = workbook.add_worksheet('Sheet 1')
        header1 = workbook.add_format(
            {'bold': True, 'font_name': 'Times New Roman',
             'size': 14, 'align': 'center',
             'font': 'height 180',
             }
        )
        header1.set_fg_color('#808080')
        content = workbook.add_format(
            {'size': 12,
             'align': 'center', 'font_name': 'Times New Roman'})
        bold_left = workbook.add_format(
            {'size': 12,
             'align': 'left',
             'bold': True, 'font_name': 'Times New Roman'})
        
        worksheet.merge_range(3, 2, 3, 10, "INSURED PERSON'S CONTRIBUTION RECORD", bold_left)
        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 35)
        worksheet.set_column(6, 6, 20)
        worksheet.write(
                'A5', "Eployer's Name:" or '', content)
        worksheet.write(
                'B5',  self.env.user.company_id.name or '', content)
        worksheet.write(
                'A6', "Address:" or '', content)
        worksheet.write(
                'B6', self.env.user.company_id.street or '', content)
        worksheet.write(
                'B7', self.env.user.company_id.street2 or '' + self.env.user.company_id.city or '' + self.env.user.company_id.zip or ' ', content)
        worksheet.write(
                'F5', "Page No:" or '', content)
        worksheet.write(
                'F6', "Chq/Mo/po No:" or '', content)
        worksheet.write(
                'F7', "Date of chq/mo/po:" or '', content)
        worksheet.write(
                'F8', "Amount:" or '', content)
        worksheet.write(
                'F9', "Bank/post Office Branch:" or '', content)
        worksheet.write(
                'F10', "Cash tsh:" or '', content)
        worksheet.write(
                'F11', "Bank/post Office Branch:" or '', content)
        worksheet.write(
                'F12', "Receipt No:" or '', content)
        worksheet.write(
                'F13', "Date of Receipt:" or '', content)
        worksheet.write(
                'A9', "Employer Registration number:" or '', content)
        worksheet.write(
                'A10', "Month of contribution:" or '', content)
        worksheet.write(
                'A11', "Regional/District Code No:" or '', content)
        bold_center = workbook.add_format(
            {'size': 12,
             'align': 'center',
             'bold': True, 'font_name': 'Times New Roman'})
        worksheet.write(
                'J1', "Form:NSSF CON.05" or '', bold_center)
        worksheet.write(
                'A13', "SR/NO." or '', bold_center)
        worksheet.write(
                'B13', "INSURED PERSON'S NAME " or '', bold_center)
        worksheet.write(
                'C13', "WAGE" or '', bold_center)
        worksheet.merge_range(12,3,12,4,"MEMBERSHIP NUMBER" or '', bold_center)
        worksheet.merge_range(
                12,5,12,6, "CONTRIBUTIONS" or '', bold_center)
        worksheet.write(
                'H13', "TSH(20%)" or '', bold_center)
        worksheet.write(
                'I13', "REMARKS" or '', bold_center)
        sr_no = 0
        row = 14
        for rec in payslip_ids:
            contribution_total = 0.0
            for line_rec in rec.line_ids:
                if line_rec.category_id.code == 'COMP':
                    contribution_total += line_rec.total
                
            sr_no += 1
            worksheet.write(
                row, 0,  sr_no or '', content)
            worksheet.write(
                row, 1, rec.employee_id.name or '', content)
            worksheet.write(
                row, 2, rec.contract_id.wage or '', content)
            worksheet.merge_range(row, 3, row, 4, rec.employee_id.identification_id or '', content)
            worksheet.merge_range(row, 5, row, 6, contribution_total or 0.0 , content)
            worksheet.write(
                row, 7, rec.contract_id.wage*0.2 or '', content)
            row += 1
            
            
        workbook.close()