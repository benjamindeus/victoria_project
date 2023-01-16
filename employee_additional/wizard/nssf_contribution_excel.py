# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil import relativedelta
import base64
import io
import xlsxwriter
import os
import tempfile

from odoo import api, fields, models
from email.policy import default


class NssfXlsReport(models.TransientModel):
    _name = 'nssf.contribution.xls'
    _description = 'Nssf Contribution report'

    date_from = fields.Date(string='Date From', required=True,
        default=datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    report_status = fields.Selection([('draft','Draft'),('done','Done'),('both','Both')], default='both')
    struct_ids = fields.Many2many('hr.payroll.structure', 
                                string='Salary Structure')
    
    
    def print_report(self):
        domain = [('date_from','>=', str(self.date_from)),
                ('date_to','<=', str(self.date_to)),
                ('credit_note', '=', False),
                 #('is_refund', '=', False)
                 ]
        if self.struct_ids:
                struct_id = self.struct_ids.ids
                domain.append(('struct_id', 'in', struct_id))
        if self.report_status == 'draft':
            domain.append(('state','=','draft'))
        elif self.report_status == 'done':
            domain.append(('state','=','done'))
        else:
            domain.append(('state','in',('draft','done')))
        print ("domaindomain", domain)
        payslip_ids = self.env['hr.payslip'].search(domain)
        print ("payslip_idspayslip_ids", payslip_ids)
        attch_obj = self.env['ir.attachment']
        file_path = tempfile.NamedTemporaryFile().name
        workbook = xlsxwriter.Workbook(file_path + '.xlsx')
        worksheet = workbook.add_worksheet('Sheet 1')
        header1 = workbook.add_format(
            {'bold': True, 'font_name': 'Times New Roman',
             'size': 14, 'align': 'center',
             'font': 'height 180',
             }
        )
        header1.set_fg_color('#808080')
        num_fmt = workbook.add_format({'num_format': '#,##0.00'})
        
        content = workbook.add_format(
            {'size': 12,
             'align': 'left', 'font_name': 'Times New Roman'})
        bold_left = workbook.add_format(
            {'size': 12,
             'align': 'left',
             'bold': True, 'font_name': 'Times New Roman'})
        
        worksheet.merge_range(3, 2, 3, 10, "INSURED PERSON'S CONTRIBUTION RECORD", bold_left)
        worksheet.set_column(0, 0, 15)
        worksheet.set_column(2, 2, 15)
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
                row, 2, rec.contract_id.wage or '', num_fmt)
            worksheet.merge_range(row, 3, row, 4, rec.employee_id.identification_id or '', content)
            worksheet.merge_range(row, 5, row, 6, contribution_total or 0.0 , num_fmt)
            worksheet.write(
                row, 7, rec.contract_id.wage*0.2 or '', num_fmt)
            row += 1
            
            
        workbook.close()
        buf = base64.encodebytes(open(file_path + '.xlsx', 'rb').read())
        try:
            if buf:
                os.remove(file_path + '.xlsx')
        except OSError:
            pass

        attach_ids = attch_obj.search([('res_model', '=',
                                        'nssf.contribution.xls')])
        if attach_ids:
            try:
                attach_ids.unlink()
            except:
                pass
        doc_id = attch_obj.create({'name': '%s.xlsx' % ('NSSF Statement xls'),
                                   'datas': buf,
                                   'res_model': 'nssf.contribution.xls'
                                                'wizard',
                                   'store_fname': '%s.xlsx' % (
                                   'nssf contribution xls report'),
                                   })
        return {'type': 'ir.actions.act_url',
                'url': 'web/content/%s?download=true' % (doc_id.id),
                'target': 'current',
                }