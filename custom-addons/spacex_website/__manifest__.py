{
    'name': 'SpaceX Website',
    'version': '17.0',
    'summary': 'Manage SpaceX missions and rockets',
    'description': 'A module to manage SpaceX missions and rockets.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Website',
    'sequence': 1,
    'depends': ['base','web','website',],
    'data': [
        'security/ir.model.access.csv',
         'views/actions.xml',
        # 'views/menus.xml',
        'views/templates.xml',
    ],

    'assets': {
        'web.assets_backend': [
             'spacex_website/static/src/js/awesome_dashboard.js',
            #  'spacex_website/static/src/xml/awesome_dashboard.xml',
             'spacex_website/static/src/css/dashboard.scss',
             
        ],
        
    },
    'installable': True,
    'application': True,
    'sequence':1,
    'license': 'LGPL-3',
}
