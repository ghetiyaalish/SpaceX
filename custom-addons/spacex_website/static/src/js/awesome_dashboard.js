/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "spacex_website.AwesomeDashboard";
    static components = { Layout };
    
    setup() {
        this.state = useState({
            controlPanel: {
                display: {
                    top: true,
                    bottom: false,
                },
            },
            dashboardData: [],
            loading: true,
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            this.state.loading = true;
            this.state.dashboardData = await rpc("/spacex/dashboard/data", {});
        } catch (error) {
            console.error("Failed to load dashboard data:", error);
        } finally {
            this.state.loading = false;
        }
    }
}

registry.category("actions").add("awesome_dashboard", AwesomeDashboard);