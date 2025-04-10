from odoo import models, fields, api

class DashboardData(models.Model):
    _name = 'spacex.dashboard'
    _description = 'SpaceX Dashboard Data'
    
    name = fields.Char(string='Title', required=True)
    value = fields.Float(string='Numeric Value')
    description = fields.Text(string='Description')
    is_visible = fields.Boolean(string='Visible to Customers', default=True)
    
    def fetch_visible_data(self):
        return self.search([('is_visible', '=', True)])