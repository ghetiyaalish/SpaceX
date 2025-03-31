{
    'name': 'SpaceX Website',
    'version': '17.0',
    'summary': 'Manage SpaceX missions and rockets',
    'description': 'A module to manage SpaceX missions and rockets.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Website',
    'sequence': 1,
    'depends': ['web',"website"],
    'data': [
        
        'views/templates.xml',
        # 'security/ir.model.access.csv',
        

    ],

    'assets': {
        'web.assets_frontend': [
             'spacex_website/static/src/js_templates.xml',
             
             

        ],
        
    },
    'installable': True,
    'application': True,
    'sequence':-1,
    'license': 'LGPL-3',
}
