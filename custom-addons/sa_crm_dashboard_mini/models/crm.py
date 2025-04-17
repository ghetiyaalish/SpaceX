from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import ast
import logging
_logger = logging.getLogger(__name__)

class SaCrmFiltersWizard(models.TransientModel):
    _name = 'sa.crm.filters.wizard'
    _description = 'CRM Filters Wizard'

    # Date range fields for the main period
    date_from   = fields.Date(string="Create Date From")
    date_to     = fields.Date(string="Create Date To")
    salesperson = fields.Many2one('res.users', string="Salesperson")
    salesteam   = fields.Many2one('crm.team', string="Sales Team")
    model_id = fields.Selection(selection=[('crm.lead','Lead/Opportunity')], string='Model', default='crm.lead', required=True)
    domain      = fields.Text(default='[]', required=True)
    # Date range fields for the comparison period
    compare_date_from   = fields.Date(string="Create Date From")
    compare_date_to     = fields.Date(string="Create Date To")
    compare_salesperson = fields.Many2one('res.users', string="Salesperson")
    compare_salesteam   = fields.Many2one('crm.team', string="Sales Team")
    compare_domain      = fields.Text(default='[]', required=True)

    def action_filter(self):
        self.env['sa.crm.filters.wizard'].search([('create_uid', '=', self.env.context.get('uid')), 
                                                  ('id', '!=',self.id)], order="id DESC").unlink()
        action = self.env.ref('crm.crm_lead_action_pipeline').sudo().read()[0]
        action['target'] = 'main'
        return action

class CrmLead(models.Model):
    _inherit = "crm.lead"
    
    # @api.model
    # def create_invoice_from_opportunity(self,opportunity_id):
    #     opportunity = self.browse(opportunity_id)
    #     if not opportunity or opportunity.type != 'opportunity' or opportunity.probability != 100:
    #         raise UserError(_("You can only create invoices from won opportunities."))
    #     if not self.env.user.has_group('account.group_account_invoice'):
    #         raise AccessError(_("You don't have permissions to create invoices."))
    
    #     #prepare invoice values
    #     invoice_vals = {
    #         'move_type': 'out_invoice',
    #         'partner_id': opportunity.partner_id.id,
    #         'invoice_line_ids':[(0,0,{
    #             'name': opportunity.name,
    #             'quantity': 1,
    #             'price_unit': opportunity.expected_revenue,
    #             'account_id': opportunity.company_id.account_default_income_account_id.id,
    #         })],
    #         'team_id': opportunity.team_id.id,
    #         'campaign_id': opportunity.campaign_id.id,
    #         'source_id': opportunity.source_id.id,
    #     }
        
    #     # Create the invoice
    #     invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_vals)
    #     return {
    #     'invoice_id': invoice.id,
    #     'invoice_name': invoice.name,
    # }
         
    def _get_activity_suggestions(self, domain):
        """Get suggested activities based on stage and history"""
        suggestions = []
        stages = self.env['crm.stage'].search([])
        for stage in stages:
            # First find opportunities in this stage
            stage_opportunities = self.env['crm.lead'].search([
                ('stage_id', '=', stage.id)
            ])
            
            if stage_opportunities:
                # Then find activities linked to these opportunities
                stage_activities = self.env['mail.activity'].search([
                    ('res_id', 'in', stage_opportunities.ids),
                    ('res_model', '=', 'crm.lead')
                ], limit=5)
                
                if stage_activities:
                    # Group by activity type
                    activity_types = {}
                    for act in stage_activities:
                        if act.activity_type_id.id not in activity_types:
                            activity_types[act.activity_type_id.id] = {
                                'name': act.activity_type_id.name,
                                'count': 0,
                                'example_summary': act.summary or ''
                            }
                        activity_types[act.activity_type_id.id]['count'] += 1
                    
                    # Add suggestions for this stage
                    suggestions.append({
                        'stage_id': stage.id,
                        'stage_name': stage.name,
                        'activities': list(activity_types.values())
                    })
    
        return suggestions   
    @api.model
    def get_sa_dashboard_values(self):
        """
        Computes CRM metrics for opportunities using filters,
        calculates percentage change, and formats results.
        """
        # Helper functions
        def safe_divide(numerator, denominator):
            return numerator / denominator if denominator else 0
        def format_currency(value):
            return f"{currency} {value:,.2f}"
        def format_percentage(value):
            return f"{value:.2f}%"
        def calculate_percentage_change(new, old):
            if old == 0:
                return 100.0 if new > 0 else 0.0
            return round(((new - old) / old) * 100, 2)
        # Get currency symbol
        currency = self.env.company.currency_id.symbol
        # Retrieve the latest filter record for the current user
        filters = self.env['sa.crm.filters.wizard'].search(
            [('create_uid', '=', self.env.context.get('uid'))], 
            order="id DESC", 
            limit=1
        )
        # Default to current month and last month if no filters are found
        if not filters:
            today = datetime.today()
            start_of_this_month = today.replace(day=1)
            start_of_last_month = (start_of_this_month - relativedelta(months=1)).replace(day=1)
            end_of_last_month = start_of_this_month - timedelta(days=1)
            
            context_1 = {
                'domain': '[]',
                'date_from': datetime.combine(start_of_this_month, datetime.min.time()),  # Start of today, midnight
                'date_to': datetime.combine(today, datetime.max.time()),  # End of today, 11:59:59 PM
                'salesperson': self.env.uid,
                'salesteam': False,
            }
            
            context_2 = {
                'domain': '[]',
                'date_from': datetime.combine(start_of_last_month, datetime.min.time()),  # Start of last month, midnight
                'date_to': datetime.combine(end_of_last_month, datetime.max.time()),  # End of last month, 11:59:59 PM
                'salesperson': self.env.uid,
                'salesteam': False,
            }

        else:
            context = filters.read([
                'date_from', 'date_to', 'salesperson', 'salesteam', 'domain',
                'compare_date_from', 'compare_date_to', 'compare_domain',
                'compare_salesperson', 'compare_salesteam'
            ])[0]
            context_1 = {
                'domain': context['domain'],
                'date_from': context['date_from'],
                'date_to': context['date_to'],
                'salesperson': context['salesperson'][0] if context['salesperson'] else False,
                'salesteam': context['salesteam'][0] if context['salesteam'] else False,
            }
            context_2 = None
            has_comparison = any(context.get(key) for key in ['compare_date_from', 'compare_date_to', 'compare_salesperson', 'compare_salesteam'])
            if has_comparison or context.get('compare_domain') != '[]':
                context_2 = {
                    'domain': context.get('compare_domain', '[]'),
                    'date_from': context.get('compare_date_from') if has_comparison else False,
                    'date_to': context.get('compare_date_to') if has_comparison else False,
                    'salesperson': context.get('compare_salesperson', [False])[0] if context.get('compare_salesperson') else False,
                    'salesteam': context.get('compare_salesteam', [False])[0] if context.get('compare_salesteam') else False,
                }
                
        # Method to compute metrics
        def compute_metrics(filter_context, Label):
            label               = Label
            custom_domain       = ast.literal_eval(filter_context['domain'])
            domain              = [('type', '=', 'opportunity')] + custom_domain
            if filter_context['salesteam']:
                salesteam       = self.env['crm.team'].browse(filter_context['salesteam'])
                label           = salesteam.name
                domain.append(('team_id', '=', filter_context['salesteam']))
            if filter_context['salesperson']:
                salesperson     = self.env['res.users'].browse(filter_context['salesperson'])
                label           = salesperson.name
                domain.append(('user_id', '=', filter_context['salesperson']))
            if filter_context['date_from'] or filter_context['date_to']:
                date_from       = filter_context.get('date_from')
                date_to         = filter_context.get('date_to')
                if date_from:
                    date_from = datetime.combine(date_from, datetime.min.time())
                    formatted_date_from = date_from.strftime("%d %b %Y")  # Format as "17 May 2024"
                    label = f"After {formatted_date_from}" if not date_to else f"{formatted_date_from} to {date_to.strftime('%d %b %Y')}"
                    
                if date_to:
                    date_to = datetime.combine(date_to, datetime.max.time())
                    formatted_date_to = date_to.strftime("%d %b %Y")  # Format as "17 May 2024"
                    label = f"Before {formatted_date_to}" if not date_from else f"{date_from.strftime('%d %b %Y')} to {formatted_date_to}"
                if date_from:
                    domain.append(('create_date', '>=', date_from))
                if date_to:
                    domain.append(('create_date', '<=', date_to))
            won_domain          = domain + [('probability', '=', 100)]
            open_domain         = domain + [('probability', '<', 100)]
            lost_domain         = domain + [('active','in', (True, False)),('probability', '=', 0)]
            won_data            = self.env['crm.lead'].read_group(won_domain, ['expected_revenue:sum', 'day_close:sum'], [])
            open_data           = self.env['crm.lead'].read_group(open_domain, ['expected_revenue:sum'], [])
            lost_data           = self.env['crm.lead'].read_group(lost_domain, [], [])
            won_count           = won_data[0]['__count'] if won_data else 0
            closed_amount       = won_data[0]['expected_revenue'] if won_data else 0
            sum_days_to_win     = won_data[0]['day_close'] if won_data else 0
            open_count          = open_data[0]['__count'] if open_data else 0
            lost_count          = lost_data[0]['__count'] if lost_data else 0
            avg                 = self.env['crm.lead'].read_group(domain, ['expected_revenue:avg'], [])
            avg_deal_size       = avg[0]['expected_revenue'] if avg else 0
            avg_days_to_win     = safe_divide(sum_days_to_win, won_count)
            closing_rate        = safe_divide(won_count, won_count + lost_count) * 100 if (won_count + lost_count) else 0
            opportunities = self.env['crm.lead'].search(domain, limit=10)
            activities = self.env['mail.activity'].search([
            ('res_id', 'in', opportunities.ids),
            ('res_model', '=', 'crm.lead')
            ], order='date_deadline desc', limit=20)
            
            activity_data = []
            for activity in activities:
                activity_data.append({
                    'id': activity.id,
                    'res_id': activity.res_id,
                    'activity_type': activity.activity_type_id.name,
                    'summary': activity.summary or '',
                    'date_deadline': activity.date_deadline.strftime('%Y-%m-%d') if activity.date_deadline else '',
                    'user_id': activity.user_id.name,
                    'note': activity.note or '',
                    'opportunity_name':  activity.res_id if activity.res_id else '',
                })
            
            
        

            
            
            # won_opportunities   = self.env['crm.lead'].search_read(won_domain,['id', 'name', 'expected_revenue', 'partner_id'] , limit=10)
            return {
                'label'             : label,
                'won_count'         : won_count,
                'open_count'        : open_count,
                'closed_amount'     : closed_amount,
                'avg_deal_size'     : avg_deal_size,
                'avg_days_to_win'   : avg_days_to_win,
                'close_rate'        : closing_rate,
                # 'won_opportunities': won_opportunities,
                'activities': activity_data,  # Add activity data
                'activity_suggestions': self._get_activity_suggestions(domain),
            }
        
        metrics_1 = compute_metrics(context_1, "A")
        _logger.error(context_1)

        _logger.error(context_2)
        result = {
            'valsA': {
                'label'             : metrics_1['label'],
                'won_count'         : metrics_1['won_count'],
                'open_count'        : metrics_1['open_count'],
                'closed_amount'     : format_currency(metrics_1['closed_amount']),
                'avg_deal_size'     : format_currency(metrics_1['avg_deal_size']),
                'avg_days_to_win'   : f"{metrics_1['avg_days_to_win']:.2f}",
                'close_rate'        : format_percentage(metrics_1['close_rate']),
                # 'map_data': metrics_1['map_data'],
                # 'funnel_data': metrics_1['funnel_data'],
                # 'won_opportunities' : metrics_1.get('won_opportunities', []),
                'activities': metrics_1['activities'],
                'activity_suggestions': metrics_1['activity_suggestions'],
                
            },
            'valsB'     : False,
            'change'    : False,
            'filters'   : False if not filters else True
        }
        if context_2:
            metrics_2 = compute_metrics(context_2, "B")
            percentage_changes = {
                "open_change": calculate_percentage_change(metrics_1['open_count'], metrics_2['open_count']),
                "avg_deal_size_change": calculate_percentage_change(metrics_1['avg_deal_size'], metrics_2['avg_deal_size']),
                "days_to_win_change": calculate_percentage_change(metrics_1['avg_days_to_win'], metrics_2['avg_days_to_win']),
                "won_change": calculate_percentage_change(metrics_1['won_count'], metrics_2['won_count']),
                "closed_change": calculate_percentage_change(metrics_1['closed_amount'], metrics_2['closed_amount']),
                "close_rate_change": calculate_percentage_change(metrics_1['close_rate'], metrics_2['close_rate']),
            }
            result['valsB'] = {
                'label': metrics_2['label'],
                'won_count': metrics_2['won_count'],
                'open_count': metrics_2['open_count'],
                'closed_amount': format_currency(metrics_2['closed_amount']),
                'avg_deal_size': format_currency(metrics_2['avg_deal_size']),
                'avg_days_to_win': f"{metrics_2['avg_days_to_win']:.2f}",
                'close_rate': format_percentage(metrics_2['close_rate']),
                # 'map_data': metrics_2['map_data'],
                # 'funnel_data': metrics_2['funnel_data'],
                # 'won_opportunities': metrics_2.get('won_opportunities', [])
                'activities': metrics_2['activities'],
                'activity_suggestions': metrics_2['activity_suggestions'],

            }
            result['change'] = percentage_changes
        if filters:
            filters.unlink()
        return result
