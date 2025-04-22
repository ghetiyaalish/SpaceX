{
    'name': 'Sales Dashboard',
    'version': '1.0',
    'summary': 'Simple Sales Dashboard',
    'depends': ['base','sale','board','web'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/dashboard.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sales_dashboard/static/src/css/dashboard.scss',
            'sales_dashboard/static/src/js/dashboard.js',
            'sales_dashboard/static/src/js/kpi_card.js',
            'sales_dashboard/static/src/xml/dashboard.xml',
            'sales_dashboard/static/src/xml/kpi_card.xml',


        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}