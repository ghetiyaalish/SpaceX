from odoo import http

class SpaceXController(http.Controller):

    @http.route('/missions', type='http', auth='public', website=True)
    def missions_page(self, **kwargs):
        missions = http.request.env['spacex.mission'].search([])
        return http.request.render('spacex_website.missions_page_template', {
            'missions': missions,
        })
    @http.route('/about', type='http', auth='public', website=True)
    def about_page(self, **kwargs):
        return http.request.render('spacex_website.about_page_template', {})
    
    @http.route('/rockets', type='http', auth='public', website=True)
    def rockets_page(self, **kwargs):
        rockets = http.request.env['spacex.rocket'].search([])  # Fetch all rockets
        return http.request.render('spacex_website.rockets_page_template', {
            'rockets': rockets,
        })
        
    @http.route('/launches', type='http', auth='public', website=True)
    def launches_page(self, **kwargs):
        missions = http.request.env['spacex.mission'].search([])  # Fetch all missions
        return http.request.render('spacex_website.launches_page_template', {
            'missions': missions,
        })
        
    @http.route('/careers', type='http', auth='public', website=True)
    def careers_page(self, **kwargs):
        return http.request.render('spacex_website.careers_page_template', {})
    