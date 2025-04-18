odoo.define('sales_dashboard.Dashboard',function(require){
    "use strict";

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const session = require('web.session');
    const _t = core._t;

    const SalesDashboard = AbstractAction.extend({
        template : 'sales_dashboard.Dashboard',
        events: {
            'click .o_reload_data' : '_onReloadData',
        },

        init: function(parent, context) {
            this._super.apply(this, arguments);
            this.data = {};
            this.metabase_enabled = false;
            this.metabase_url = '';
        },

        willStart : function(){
            return this._loadData();
        },
        start : function(){
            this._renderCharts();
            return this._super.apply(this,arguments);
        },
        _loadData : function(){
            const self = this;
            return this._rpc({
                model:'sales.dashboard',
                method: 'get_sales_data'
            }).then(function(result){
                self.data = result;
                return self._checkMetabaseConfig();
            });
        },

        _checkMetabaseConfig:function(){
            const self = this;
            return this._rpc({
                model: 'ir.config_parameter',
                method: 'get_param',
                args : ['metabase.url',false],
            }).then(function(url){
                if(url){
                    self.metabase_enabled = true;
                    return self._rpc({
                        model : 'ir.config_parameter',
                        method : 'get_param',
                        args : ['metabase.sales_dashboard_id',false],
                    }).then(function(dashboardId) {
                        if (dashboardId) {
                            self.metabase_url = `${url}/embed/dashboard/${dashboardId}#bordered=false&titled=false`;
                        }
                    })
                }

            });
        },

        _renderCharts: function() {
            // Top Customers Chart
            if (this.data.top_customers && this.data.top_customers.length) {
                this._renderBarChart(
                    'topCustomersChart',
                    this.data.top_customers.map(item => item.partner_id[1]),
                    this.data.top_customers.map(item => item.amount_total),
                    'Top Customers by Sales'
                );
            }

            // Sales by Salesperson Chart
            if (this.data.sales_by_salesperson && this.data.sales_by_salesperson.length) {
                this._renderPieChart(
                    'salesBySalespersonChart',
                    this.data.sales_by_salesperson.map(item => item.user_id[1]),
                    this.data.sales_by_salesperson.map(item => item.amount_total),
                    'Sales by Salesperson'
                );
            }

        },
        _renderBarChart: function(elementId, labels, data, title) {
            const ctx = document.getElementById(elementId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Sales Amount',
                        data: data,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: title
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },

        _renderPieChart: function(elementId, labels, data, title) {
            const ctx = document.getElementById(elementId).getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 206, 86, 0.5)',
                            'rgba(75, 192, 192, 0.5)',
                            'rgba(153, 102, 255, 0.5)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: title
                        }
                    }
                }
            });
        },

        format_currency: function(value) {
            return new Intl.NumberFormat(undefined, {
                style: 'currency',
                currency: this.getSession().get_currency() || 'USD'
            }).format(value);
        },

        _onReloadData: function() {
            this._loadData().then(() => {
                this._renderCharts();
            });
        },


    });

    core.action_registry.add('sales_dashboard_action', SalesDashboard);
    return SalesDashboard;

});