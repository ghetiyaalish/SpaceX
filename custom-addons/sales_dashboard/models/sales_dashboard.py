from odoo import models,fields,api
class SalesDashboard(models.Model):
    _name = "sales.dashboard"
    _description = "Sales Dashboard"
    
    @api.model
    def get_sales_data(self):
        # Get total sales orders
        total_orders = self.env['sale.order'].search_count([])
        
        # Get total sales amount
        total_sales = sum(self.env['sale.order'].search([]).mapped('amount_total'))
        
        # Get average order value
        avg_order_value = total_sales / total_orders if total_orders else 0
        
        # Get top customers
        top_customers = self.env['sale.order'].read_group([],['partner_id','amount_total:sum'],['used_id'],orderby = 'amount_total desc')
        
        # Get sales by salesperson
        sales_by_salesperson = self.env['sale.order'].read_group([],['used_id' , 'amount_total:sum'],['user_id'],orderby='amount_total desc')
        
        # Get recent orders
        recent_orders = self.env['sale.order'].search_read([],['name','date_order','partner_id','amount_total','state'],limit=10,order = 'date_order desc')
        
        return{
            'total_orders': total_orders,
            'total_sales': total_sales,
            'avg_order_value': avg_order_value,
            'top_customers': top_customers,
            'sales_by_salesperson': sales_by_salesperson,
            'recent_orders': recent_orders,
            
        }