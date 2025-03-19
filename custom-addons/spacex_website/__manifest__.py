{
    'name': 'SpaceX Website',
    'version': '1.0',
    'summary': 'Manage SpaceX missions and rockets',
    'description': 'A module to manage SpaceX missions and rockets.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Website',
    'sequence':1,
    'depends': ['website','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/spacex_views.xml',
        'views/templates.xml',
        # 'views/assets.xml', 
    ],
    'controllers': [
        'controllers/main.py',  # Add the new controller
    ],
    'assets': {
    'web.assets_backend': [
        'custom-addons/spacex_website/static/src/css/style.css',
    ],
},
    
    
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}