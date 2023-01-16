# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil import relativedelta
import base64
import io
import xlsxwriter
import os
import tempfile

from odoo import api, fields, models


class MontlyStatmentXlsReport(models.TransientModel):
    _name = 'monthly.statement.xls'
    _description = 'Monthly statement xls report'

    date_from = fields.Date(string='Date From', required=True,
        default=datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    report_status = fields.Selection([('draft','Draft'),('done','Done'),('both','Both')], default='both')
    struct_ids = fields.Many2many('hr.payroll.structure', 
                                string='Salary Structure')
    
    def print_report(self):
        aproximate_place=0
        domain = [('date_from','>=', str(self.date_from)),
                ('date_to','<=', str(self.date_to)),
                ('credit_note', '=', False),
                #  ('is_refund', '=', False)
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
        payslip_ids = self.env['hr.payslip'].search(domain)
        
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
        worksheet.set_column('B:B', 24)
        worksheet.set_column('C:AD7', 20)
        header1.set_fg_color('#808080')
        num_fmt = workbook.add_format({'num_format': '#,##0.00'})
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
        bold_center_head = workbook.add_format(
            {'size': 13,
             'align': 'center',
             'bold': True, 'font_name': 'Times New Roman'})

        bold_center_num_frmt = workbook.add_format(
            {'size': 12,
             'align': 'center','num_format': '#,##0.00',
             'bold': True, 'font_name': 'Times New Roman'})
        
        worksheet.merge_range(2, 1, 2, 2, "VIGU TRADING", bold_center_head)
        worksheet.merge_range(3, 1, 3, 2, "PAYROLL REPORT FOR THE MONTH OF  ", bold_center_head)
        worksheet.merge_range(4, 1, 4, 2, "TANZANIA MAINLY LAND", bold_center_head)
        worksheet.write(
                'A7', "SR/NO." or '', bold_center)
        worksheet.write(
                'B7', "EMPLOYEE NAME " or '', bold_center)
        # worksheet.write(
        #         'C7', "PAY ROLL NO." or '', bold_center)
        worksheet.write(
                'C7', "BRANCH NAME " or '', bold_center)
        worksheet.write(
                'D7', "DESIGNATION" or '', bold_center)
        worksheet.write(
                'E7', "EMPLOYEE ID" or '', bold_center)
        worksheet.write(
                'F7', "BASIC PAY" or '', bold_center)
        worksheet.write(
                'G7', "LIVING ALLOWANCE" or '', bold_center)
        worksheet.write(
                'H7', "CONVEYANCE " or '', bold_center)
        worksheet.write(
                'I7', "MEDICAL" or '', bold_center)
        worksheet.write(
                'J7', "FOOD ALLOWANCE" or '', bold_center)
        worksheet.write(
                'K7', "NHIF ALLOWANCE" or '', bold_center)
        worksheet.write(
                'L7', "BENEFET IN KIND" or '', bold_center)
        worksheet.write(
                'M7', "OVERTIME" or '', bold_center)

        worksheet.write(
                'N7', "LEAVE ALLOWANCE." or '', bold_center)
        worksheet.write(
                'O7', "GROSS PAY " or '', bold_center)
        worksheet.write(
                'P7', "NSSF EMPLOYER" or '', bold_center)
        worksheet.write(
                'Q7', "TAXABLE AMOUNT" or '', bold_center)
        worksheet.write(
                'R7', "P.A.Y.E" or '', bold_center)
        worksheet.write(
                'S7', "NSSF EMPLOYEE" or '', bold_center)
        worksheet.write(
                'T7', "NHIF EMPLOYEE" or '', bold_center)
        worksheet.write(
                'U7', "HELSB" or '', bold_center)
        worksheet.write(
                'V7', "WCF" or '', bold_center)
        worksheet.write(
                'W7', "SDL" or '', bold_center)
        worksheet.write(
                'X7', "TOTAL DEDUCTION" or '', bold_center)
        worksheet.write(
                'Y7', "TOTAL NSSF" or '', bold_center)

        worksheet.write(
                'Z7', "TOTAL NHIF." or '', bold_center)

        worksheet.write(
                'AA7', "STAFF LOAN " or '', bold_center)

        worksheet.write(
                'AB7', "SALARY ADVANCE " or '', bold_center)

        worksheet.write(
                'AC7', "NET SALARY " or '', bold_center)
        worksheet.write(
                'AD7', "ZSSF TOTAL" or '', bold_center)

        sr_no = 0
        row = 7
        basic_total = 0.0
        living_exp_total = 0.0
        gross_total = 0.0
        ha_total = 0.0
        alw_total_total = 0.0
        ded_total_total = 0.0
        payee_total_total = 0.0
        cna_allow_total = 0.0
        foo_allow_total = 0.0
        leav_allow_total = 0.0
        mda_allow_total = 0.0
        final_alw_total =0.0
        tax_total_total = 0.0
        NSSFEMPLOYEER_total = 0.0
        NSSFEMPLOYEE_total = 0.0
        ZSSFEMPLOYEER_total = 0.0
        ZSSFEMPLOYEE_total = 0.0
        nhif_allow_total = 0.0
        ben_allow_total = 0.0
        over_allow_total = 0.0
        NHIFEMPLOYEE_total = 0.0
        txb_total = 0.0
        payee_total = 0.0
        helsb_total = 0.0
        ded_total = 0.0
        tnssf_total = 0.0
        tzssf_total = 0.0
        tnhif_total = 0.0
        net_total = 0.0


        wcf_total = 0.0
        sdl_total = 0.0
        # ben added this
        loan_total=0.0
        adv_salary_total=0.0

        for rec in payslip_ids:
#             contribution_total = 0.0
            basic = 0.0
            livng_ = 0.0
            cna_ = 0.0
            mda_ = 0.0
            NSSFEMPLOYEER_ = 0.0
            NSSFEMPLOYEE_ = 0.0
            ZSSFEMPLOYEER_ = 0.0
            ZSSFEMPLOYEE_ = 0.0
            NHIFEMPLOYEE_ = 0.0
            helsb_ = 0.0
            wcf_ = 0.0
            sdl_ = 0.0
            ded_ = 0.0
            tnssf_ = 0.0
            tzssf_ = 0.0
            tnhif_ = 0.0
            nhif_all = 0.0
            ben_ = 0.0
            over_ = 0.0
            net_ = 0.0
            foo_ = 0.0
            leav_ = 0.0
            txb_ = 0.0
            gross = 0.0
            ha = 0.0
            alw_total = 0.0
            payee_ = 0.0
            final_alw = 0.0
            tax_total =0.0
# benjamin deus added this to compute payroll total
            loan_=0.0
            _adv_salary=0.0



            for line_rec in rec.line_ids:
                print ("line_rec.codeline_rec.code",line_rec.code)
                if line_rec.category_id.code == 'BASIC':
                    basic += line_rec.total
                    basic_total += basic

                if line_rec.code == 'GROSS':
                    gross += line_rec.total
                    gross_total += gross
                    
                if line_rec.code == 'NSSFF_EMPLER':
                    NSSFEMPLOYEER_ += line_rec.total
                    NSSFEMPLOYEER_total += NSSFEMPLOYEER_
                if line_rec.code == 'ZSSFF_EMPLER':
                    ZSSFEMPLOYEER_ += line_rec.total
                    ZSSFEMPLOYEER_total += ZSSFEMPLOYEER_

                if line_rec.category_id.code == 'DED' and not line_rec.code != 'PAYEE':
                    ded_total += line_rec.total
                    ded_total_total += ded_total

                if line_rec.code == 'TXB':
                    tax_total += line_rec.total
                    tax_total_total += tax_total

                if line_rec.code == 'PAYEE':
                    payee_ += line_rec.total
                    payee_total += payee_

                if line_rec.code == 'NSSF_EMPLOYEE':
                    NSSFEMPLOYEE_ += line_rec.total
                    NSSFEMPLOYEE_total += NSSFEMPLOYEE_
                if line_rec.code == 'ZSSF_EMPLOYEE':
                    ZSSFEMPLOYEE_ += line_rec.total
                    ZSSFEMPLOYEE_total += ZSSFEMPLOYEE_


                if line_rec.code == 'LIVIN':
                    livng_ += line_rec.total
                    living_exp_total += livng_


                if line_rec.code == 'CNA':
                    cna_ += line_rec.total
                    cna_allow_total += cna_


                if line_rec.code == 'MDA':
                    mda_ += line_rec.total
                    mda_allow_total += mda_

                if line_rec.code == 'FOOD':
                    foo_ += line_rec.total
                    foo_allow_total += foo_

                if line_rec.code == 'LEA':
                    leav_ += line_rec.total
                    leav_allow_total += leav_

                


                if line_rec.code == 'NHIF_EMPLYEE':
                    NHIFEMPLOYEE_ += line_rec.total
                    NHIFEMPLOYEE_total += NHIFEMPLOYEE_

                if line_rec.code == 'HELSB':
                    helsb_ += line_rec.total
                    helsb_total += helsb_

                if line_rec.code == 'WCF_ADM':
                    wcf_ += line_rec.total
                    wcf_total += wcf_

                if line_rec.code == 'ADSDL':
                    sdl_ += line_rec.total
                    sdl_total += sdl_

                if line_rec.code == 'TXD':
                    ded_ += line_rec.total
                    ded_total += ded_

                if line_rec.code == 'TNSSF':
                    tnssf_ += line_rec.total
                    tnssf_total += tnssf_
                if line_rec.code == 'ZNSSF':
                    tzssf_ += line_rec.total
                    tzssf_total += tzssf_
                if line_rec.code == 'TNHIF':
                    tnhif_ += line_rec.total
                    tnhif_total += tnhif_

                if line_rec.code == 'NET':
                    net_ += line_rec.total
                    net_total += net_

# benjamin added this
	# SAR
            # adv_salary=0.0


                if line_rec.code == 'LO':
                    loan_ += line_rec.total
                    loan_total += loan_

                if line_rec.code == 'SAR':
                    _adv_salary += line_rec.total
                    adv_salary_total += _adv_salary
# benjamin added this

     
                if line_rec.code == 'TXB':
                    txb_ += line_rec.total
                    txb_total += txb_


              
                 

#                 
            sr_no += 1
            worksheet.write(
                row, 0,  sr_no or '', content)
            worksheet.write(
                row, 1, rec.employee_id.name or '', bold_left)
            # worksheet.write(
            #     row, 2, rec.number, bold_left)
            worksheet.write(
                row, 2,"ben", bold_left)
            worksheet.write(
                row, 3, rec.contract_id.job_id.name, bold_left)
            worksheet.write(
                row, 4, rec.employee_id.empl_id, bold_left)
            worksheet.write(
                row, 5, round(basic,aproximate_place), num_fmt)

            worksheet.write(
                row, 6, round(livng_,aproximate_place), num_fmt)

            worksheet.write(
                row, 7, round(cna_,aproximate_place), num_fmt)
            worksheet.write(
                row, 8, round(mda_,aproximate_place), num_fmt)
            worksheet.write(
                row, 9, round(foo_,aproximate_place), num_fmt)
            worksheet.write(
                row, 10, round(nhif_all,aproximate_place), num_fmt)
            worksheet.write(
                row, 11, round(ben_,aproximate_place), num_fmt)
            worksheet.write(
                row, 12, over_, num_fmt)
            worksheet.write(
                row, 13, round(leav_,aproximate_place), num_fmt)
            worksheet.write(
                row, 14, round(gross,aproximate_place), num_fmt)
            worksheet.write(
                row, 15, round(NSSFEMPLOYEER_,aproximate_place), num_fmt)
            worksheet.write(
                row, 16, round(txb_,aproximate_place), num_fmt)
            worksheet.write(
                row, 17, round(payee_,aproximate_place), num_fmt)
            worksheet.write(
                row, 18, round(NSSFEMPLOYEE_,aproximate_place), num_fmt)
            worksheet.write(
                row, 19, round(NHIFEMPLOYEE_,aproximate_place), num_fmt)
            worksheet.write(
                row, 20, round(helsb_,aproximate_place), num_fmt)

            worksheet.write(
                row, 21, round(wcf_,aproximate_place), num_fmt)
            worksheet.write(
                row, 22, round(sdl_,aproximate_place), num_fmt)
            worksheet.write(
                row, 23, round(ded_,aproximate_place), num_fmt)
            worksheet.write(
                row, 24, round(tnssf_,aproximate_place), num_fmt)
            worksheet.write(
                row, 25, round(tnhif_,aproximate_place), num_fmt)

        # benjamin added this
            worksheet.write(
                row, 26, round(loan_,aproximate_place), num_fmt)

            worksheet.write(
                row, 27, round(_adv_salary,aproximate_place), num_fmt)

            worksheet.write(
                row, 28, round(net_,aproximate_place), num_fmt)


            worksheet.write(
                row, 29, round(tzssf_, aproximate_place), num_fmt)

            row += 1
        worksheet.write(
                row, 0,  'TOTAL', bold_center)
        worksheet.write(
            row, 1, '', content)
        worksheet.write(
            row, 2, '', content)
        worksheet.write(
            row, 3, '', content)
        worksheet.write(
            row, 4, ' ',  content)
        worksheet.write(
            row, 5, basic_total, bold_center_num_frmt)

        worksheet.write(
            row, 6, living_exp_total, bold_center_num_frmt)

        worksheet.write(
            row, 7, cna_allow_total, bold_center_num_frmt)
        worksheet.write(
            row, 8, mda_allow_total, bold_center_num_frmt)
        worksheet.write(
            row, 9, foo_allow_total, bold_center_num_frmt)
        worksheet.write(
            row, 10, nhif_allow_total, bold_center_num_frmt)
        worksheet.write(
            row, 11, ben_allow_total, bold_center_num_frmt)
        worksheet.write(
            row, 12, over_allow_total, bold_center_num_frmt)
        worksheet.write(
            row, 13, leav_allow_total, bold_center_num_frmt)

        worksheet.write(
            row, 14, gross_total, bold_center_num_frmt)
   
        worksheet.write(
            row, 15, NSSFEMPLOYEER_total, bold_center_num_frmt)
        worksheet.write(
            row, 16, txb_total, bold_center_num_frmt)
        worksheet.write(
            row, 17, payee_total, bold_center_num_frmt)
        worksheet.write(
            row, 18, NSSFEMPLOYEE_total, bold_center_num_frmt)
        worksheet.write(
            row, 19, NHIFEMPLOYEE_total, bold_center_num_frmt)
        worksheet.write(
            row, 20, helsb_total, bold_center_num_frmt)
        worksheet.write(
            row, 21, wcf_total, bold_center_num_frmt)

        worksheet.write(
            row, 22, sdl_total, bold_center_num_frmt)


        worksheet.write(
            row, 23, ded_total, bold_center_num_frmt)
        worksheet.write(
            row, 24, tnssf_total, bold_center_num_frmt)
        worksheet.write(
            row, 25, tnhif_total, bold_center_num_frmt)
        worksheet.write(
            row, 26, loan_total, bold_center_num_frmt)
        worksheet.write(
            row, 27, adv_salary_total, bold_center_num_frmt)
        worksheet.write(
            row, 28, net_total, bold_center_num_frmt)
        worksheet.write(
            row, 29, tzssf_total, bold_center_num_frmt)
        


        workbook.close()
        buf = base64.encodebytes(open(file_path + '.xlsx', 'rb').read())
        try:
            if buf:
                os.remove(file_path + '.xlsx')
        except OSError:
            pass

        attach_ids = attch_obj.search([('res_model', '=',
                                        'monthly.statement.xls')])
        if attach_ids:
            try:
                attach_ids.unlink()
            except:
                pass
        doc_id = attch_obj.create({'name': '%s.xlsx' % ('Payroll Monthly Report xls'),
                                   'datas': buf,
                                   'res_model': 'monthly.statement.xls'
                                                'wizard',
                                   'store_fname': '%s.xlsx' % (
                                   'Payroll Monthly Report xls'),
                                   })
        return {'type': 'ir.actions.act_url',
                'url': 'web/content/%s?download=true' % (doc_id.id),
                'target': 'current',
                }

