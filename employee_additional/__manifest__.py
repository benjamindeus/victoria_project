# -*- coding: utf-8 -*-
{
    'name': "employee_additional",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'hr_payroll_community',
        'hr_contract',
        'hr_holidays',
        'hr_contract_types',
        ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/hr_payroll_security.xml',
        'data/hr_payroll_data.xml',
        'data/data.xml',
        'data/mail_template_data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/custom_attendance.xml',
        'wizard/payslip_send_view.xml',
        'wizard/monthly_statement_xls_view.xml',
        'wizard/payee_statement_xls_view.xml',
        'wizard/nssf_contribution_excel_view.xml',
        'views/worker_compensation_report.xml',
        'views/sdl_report_template.xml',
        'views/payee_statement_report.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
