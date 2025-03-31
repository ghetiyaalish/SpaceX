from odoo import http
from odoo.http import request

class QwebTutorials(http.Controller):
    @http.route('/qweb-tutorials', type='http', auth="public", website=True)
    def qweb_tutorials(self):
        
        def some_fun():
            return "return string from a function in website how can i edit in this project"
        # some_model=http.request.env['sale.order'].search([])
        data={
            'string':'Qweb Tutorial',
            'integer':1000,
            'float':20.0,
            'boolean':True,
            'some_list':[1,2,3,4,5],
            'some_dict':{'any-value':'any-value'},
            'some_fun':some_fun(),
            # 'model':some_model,
        }
        return http.request.render('spacex_website.somePythonTemplate',data)