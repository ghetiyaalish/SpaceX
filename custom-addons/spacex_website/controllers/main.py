from odoo import http
from odoo.http import request

class DashboardController(http.Controller):
    
    @http.route('/spacex/dashboard/data', type='json', auth='user')
    def dashboard_data(self):
        Dashboard = request.env['spacex.dashboard']
        records = Dashboard.fetch_visible_data()
        return records.read(['name', 'value', 'description'])