/** @odoo-module **/

import { session } from '@web/session';
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart ,onMounted} from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";

export class SaCrmDashboard extends Component {
    setup() {
        this.action = useService('action');
        this.orm = useService('orm');
        this.notification = useService('notification');
        this.state = useState({
            dashboardValues: null,
            isCollapsed: false,
            isHidden: true,
            // mapLoaded: false,
            // chartLibLoaded: false,
            // isCreatingInvoice: false,
            activeTab: 'timeline', // 'timeline' or 'suggestions'
            selectedOpportunity: null,
        });
        onWillStart(this.onWillStart);

    }
    setActiveTab(tab) {
        this.state.activeTab = tab;
    }
    
    selectOpportunity(opportunityId) {
        this.state.selectedOpportunity = opportunityId;
    }
    async onWillStart() {
        await this._checkUserGroup();
        if (!this.state.isHidden) {
            await Promise.all([
                loadJS("/web/static/lib/Chart/Chart.js"),
                loadJS("https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=visualization"),
                this._fetchData()
            ]);
            this.state.chartLibLoaded = true;
            this.state.mapLoaded = true;
        }
    }
    async _fetchData() {
        this.state.dashboardValues = await this.orm.call(
            'crm.lead',
            'get_sa_dashboard_values',
            [],
            { context: session.user_context },
        );
    }

    async createSuggestedActivity(activityType, summary) {
        if (!this.state.selectedOpportunity) {
            this.notification.add(
                _t("Please select an opportunity first"),
                {type: "warning"}
            );
            return;
        }
        
        try {
            await this.orm.call(
                'mail.activity',
                'create',
                [{
                    'res_id': this.state.selectedOpportunity,
                    'res_model': 'crm.lead',
                    'activity_type_id': activityType,
                    'summary': summary,
                    'date_deadline': new Date().toISOString().split('T')[0], // Today
                }]
            );
            this.notification.add(
                _t("Activity created successfully"),
                {type: "success"}
            );
            await this._fetchData(); // Refresh data
        } catch (error) {
            this.notification.add(
                _t("Error creating activity: ") + error.message,
                {type: "danger"}
            );
        }
    }

    //  async createInvoice(opportunityId){
    //     this.state.isCreatingInvoice = true ;
    //     try{
    //         const result = await this.orm.call(
    //             'crm.lead',
    //             'create_invoice_from_opportunity',
    //             [opportunityId],
    //             { context: session.user_context },
    //         );
    //         this.notification.add(
    //             _t(`Invoice ${result.invoice_name} created successfully`),
    //             {type:"success"}
    //         );
    //         // Open the created invoice
    //         this.action.doAction({
    //             type:"ir.actions.act_window",
    //             name:"Invoice",
    //             res_model: "account.move",
    //             res_id: result.invoice_id,
    //             views: [[false,"form"]],
    //             view_mode: "form",

    //         });
    //     }
    //         catch(error){
    //             let errorMessage = error.message;
    //             if (error.data && error.data.arguments) {
    //                 errorMessage = error.data.arguments[0];
    //             }
    //             this.notification.add(
    //                 _t(`Error creating invoice : ${error.message}`),
    //                 {type:'danger'}
    //             );
    //         }
    //         finally{
    //             this.state.isCreatingInvoice =  false;

            
    //     }
    //  }
     



    toggleFiltersWizard() {
        const action = {
            type: "ir.actions.act_window",
            name: "Filters",
            res_model: "sa.crm.filters.wizard",
            views: [[false, "form"]],
            view_mode: "form",
            target: "new",
        };
    
        this.action.doAction(action);
    }

    ChangeSearchVals(ev) {
        const filters = ev.currentTarget.getAttribute("filter_name");
        const filters_list = filters.split(",");
        const searchItems = this.env.searchModel.getSearchItems((item) =>
            filters_list.includes(item.name)
        );
        this.env.searchModel.query = [];
        for (const item of searchItems) {
            this.env.searchModel.toggleSearchItem(item.id);
        }
    }

    toggleCollapse() {
        this.state.isCollapsed = !this.state.isCollapsed;
    }

    async _checkUserGroup() {
        const groupId = 'sa_crm_dashboard_mini.group_sa_crm_min_dashboard';
        try {
            const hasGroup = await this.orm.call('res.users', 'has_group', [groupId]);
            this.state.isHidden = !hasGroup;
        } catch (error) {
            console.error("Error checking user group:", error);
            this.state.isHidden = true;
        }
    }
}

SaCrmDashboard.template = 'sa_crm_dashboard_mini.SaCrmDashboard';