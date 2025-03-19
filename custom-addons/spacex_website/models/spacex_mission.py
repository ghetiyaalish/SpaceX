from odoo import models, fields,api

class SpaceXMission(models.Model):
    _name = 'spacex.mission'
    _description = 'SpaceX Mission'

    name = fields.Char(string='Mission Name', required=True)
    launch_date = fields.Date(string='Launch Date')
    success = fields.Boolean(string='Mission Success')
    rocket_id = fields.Many2one('spacex.rocket', string='Rocket Used')
    Mission_leader = fields.Char(string='Leader Name', required=True)
    
