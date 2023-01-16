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
            'hr_payroll_community.payee_statemenet_repot_xlsx').report_action(self)

class NssfPayslipXlsx(models.AbstractModel):
    _name = 'report.hr_payslip.payee_statemenet_repot_xlsx'
    _inherit = 'report.report_xlsx.abstract'

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
        bold_right = workbook.add_format(
            {'size': 12,
             'align': 'right',
             'bold': True, 'font_name': 'Times New Roman'})
        bold_center = workbook.add_format(
            {'size': 12,
             'align': 'center',
             'bold': True, 'font_name': 'Times New Roman'})
        
        worksheet.merge_range(2, 2, 2, 5, "TANZANIA REVENUE AUTHORITY", bold_left)
        worksheet.merge_range(4, 2, 4, 5, "P.A.Y.E.", bold_center)
        worksheet.merge_range(5, 2, 5, 8, "STATEMENT AND PAYMENT OF TAX WITHHELD", bold_left)
        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 35)
        worksheet.set_column(6, 6, 20)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 20)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 20)
        worksheet.set_column(7, 7, 20)
        worksheet.write(
                'F7', "Year" or '', content)
        worksheet.write(
                'F8', "TIN:" or '', content)
        worksheet.write(
                'B9', "Period: (Please tick the appropriate box)" or '', content)
        worksheet.write(
                'B10', "From 1 January to 30 June" or '', content)
        worksheet.write(
                'B11', "From 1 January to 31 December" or '', content)
        worksheet.write(
                'B13', "Name of Employer: " or '', bold_left)
        worksheet.write(
                'B14', self.env.user.company_id.name or '', content)
        worksheet.merge_range(16, 1, 16, 8, 'Postal Address' or '', bold_left)
        worksheet.write(
                'B18', "P. O. Box " or '', bold_left)
        worksheet.merge_range(17, 2, 17, 3, self.env.user.company_id.zip or '', content)
        worksheet.write(
                'F18', "Postal City" or '', bold_left)
        worksheet.merge_range(17, 6, 17, 7, self.env.user.company_id.city or '', content)
        worksheet.merge_range(19, 1, 19, 8, 'Contact Numbers:' or '', bold_left)
        worksheet.write(
                'B22', "Phone number" or '', bold_left)
        worksheet.merge_range(21, 2, 21, 3, self.env.user.company_id.phone or '', content)
        worksheet.write(
                'F22', "Second Phone" or '', bold_left)
        worksheet.merge_range(21, 6, 21, 7, self.env.user.company_id.phone or '', content)
        worksheet.write(
                'B23', "Third Phone" or '', bold_left)
        worksheet.merge_range(22, 2, 22, 3, self.env.user.company_id.phone or '', content)
        worksheet.write(
                'F23', " Fax number" or '', bold_left)
        worksheet.merge_range(22, 6, 22, 7, self.env.user.company_id.phone or '', content)
        worksheet.write('B25' ,'Email Address:' or '', bold_left)
        worksheet.merge_range(24, 2, 24, 8, self.env.user.company_id.email or '', bold_left)
        worksheet.merge_range(26, 1, 26, 8, 'Physical Address:' or '', bold_left)
        worksheet.write(
                'B28', "Plot Number" or '', bold_left)
        worksheet.merge_range(27, 2, 27, 3, '', content)
        worksheet.write(
                'F28', "Block Number" or '', bold_left)
        worksheet.merge_range(27, 6, 27, 7, '', content)
        worksheet.write('B30' ,'Street/Location:' or '', bold_left)
        worksheet.merge_range(29, 2, 29, 8, self.env.user.company_id.street or '', bold_left)
        worksheet.write('B31' ,'Name of Branch' or '', bold_left)
        worksheet.merge_range(30, 2, 30, 8, '', bold_left)
        worksheet.merge_range(32, 1, 32, 6, "P.A.Y.E. - DETAILS OF PAYMENT OF TAX WITHHELD", bold_center)
        worksheet.write('B34' ,'Name of Employer: ' or '', bold_left)
        worksheet.merge_range(33, 2, 33, 3, self.env.user.company_id.name, content)
        worksheet.write('E34' ,'TIN' or '', bold_left)
#         worksheet.write(33, self.env.company_id.name or '', content)
        worksheet.merge_range(33, 6, 33, 7, self.env.user.company_id.tin, content)
# #         worksheet.write(
# #                 'A10', "Month of contribution:" or '', content)
#         worksheet.write(
#                 'A11', "Regional/District Code No:" or '', content)
        bold_center = workbook.add_format(
            {'size': 12,
             'align': 'center',
             'bold': True, 'font_name': 'Times New Roman'})
        worksheet.write(
                'A36', "SR/NO." or '', bold_center)
        worksheet.write(
                'B36', "NAME OF EMPLOYEE " or '', bold_center)
        worksheet.write(
                'C36', "PAY ROLL NO." or '', bold_center)
        worksheet.write(
                'D36', "POSTAL ADDRESS" or '', bold_center)
        worksheet.write(
                'E36', "POSTAL CITY" or '', bold_center)
        worksheet.write(
                'F36', "BASIC PAY" or '', bold_center)
        worksheet.write(
                'G36', "HOUSING" or '', bold_center)
        worksheet.write(
                'H36', "ALLOWANCE AND BENEFIT" or '', bold_center)
        worksheet.write(
                'I36', "GROSS PAY" or '', bold_center)
        worksheet.write(
                'J36', "DEDUCTIONS" or '', bold_center)
        worksheet.write(
                'K36', "TAXABLE AMOUNT" or '', bold_center)
        worksheet.write(
                'L36', "TAX DUE" or '', bold_center)
        sr_no = 0
        row = 36
        basic_total = 0.0
        gross_total = 0.0
        ha_total = 0.0
        alw_total_total = 0.0
        ded_total_total = 0.0
        tax_total_total = 0.0
        for rec in payslip_ids:
#             contribution_total = 0.0
            basic = 0.0
            gross = 0.0
            ha = 0.0
            alw_total = 0.0
            ded_total = 0.0
            tax_total = 0.0
            payeee
            for line_rec in rec.line_ids:
                if line_rec.code == 'BASIC':
                    basic = line.total
                    basic_total += basic
                elif line_rec.code == 'GROSS':
                    gross += line_rec.total
                    gross_total += gross
                elif line_rec.code == 'HOUSE ALLOWANCE':
                    ha = line_rec.total
                    ha_total += ha
                elif line_rec.category_id.code == 'ALW':
                    alw_total += line_rec.total
                    alw_total -= ha
                    alw_total_total += alw_total
                elif line_rec.code == 'DED':
                    ded_total += line_rec.total
                    ded_total_total += ded_total
                elif line.code == 'TXB':
                    tax_total += line_rec.total
                    tax_total_total += tax_total
                elif line.code in ['PAYEE', 'PAYEE-MOSE','PAYEE-andrew','PAYEE-Andrew']:
                    print
#        
            sr_no += 1
            worksheet.write(
                row, 0,  sr_no or '', content)
            worksheet.write(
                row, 1, rec.employee_id.name or '', content)
            worksheet.write(
                row, 2, '', content)
            worksheet.write(
                row, 3, rec.employee_id.address_home_id.street, content)
            worksheet.write(
                row, 4, rec.employee_id.address_home_id.city, content)
            worksheet.write(
                row, 5, basic, content)
            worksheet.write(
                row, 6, ha, content)
            worksheet.write(
                row, 7, alw_total, content)
            worksheet.write(
                row, 8, gross, content)
            worksheet.write(
                row, 9, ded_total, content)
            
#             worksheet.merge_range(row, 5, row, 6, contribution_total or 0.0 , content)
#             worksheet.write(
#                 row, 7, rec.contract_id.wage*0.2 or '', content)
            row += 1
        worksheet.write(
                row, 0,  'TOTAL', content)
        worksheet.write(
            row, 1, '', content)
        worksheet.write(
            row, 2, '', content)
        worksheet.write(
            row, 3, '', content)
        worksheet.write(
            row, 4, ' ',  content)
        worksheet.write(
            row, 5, basic_total, content)
        worksheet.write(
            row, 6, ha_total, content)
        worksheet.write(
            row, 7, alw_total_total, content)
        worksheet.write(
            row, 8, gross_total, content)
        worksheet.write(
            row, 9, ded_total_total, content)
        
        workbook.close()