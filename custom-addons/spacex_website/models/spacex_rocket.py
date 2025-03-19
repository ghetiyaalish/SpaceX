from odoo import models, fields

class SpaceXRocket(models.Model):
    _name = 'spacex.rocket'
    _description = 'SpaceX Rocket'

    name = fields.Char(string='Rocket Name', required=True)
    model = fields.Char(string='Rocket Model')
    missions_ids = fields.One2many('spacex.mission', 'rocket_id', string='Missions')
    