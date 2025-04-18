{
    'name': 'Sales Dashboard',
    'version': '1.0',
    'summary': 'Advanced Sales Dashboard with Metabase Integration',
    'description': 'Comprehensive sales dashboard with key metrics and Metabase integration',
    'author': 'Irish Tweed',
    'depends': ['sale', 'account'],
    'data': [
        'views/sales_dashboard_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sales_dashboard/static/src/js/dashboard.js',
            'sales_dashboard/static/src/xml/dashboard.xml',

        ],
    },
    'installable': True,
    'application': True,
}