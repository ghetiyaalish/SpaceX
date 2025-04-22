/** @odoo-module **/
import { KpiCard } from "./kpi_card.js";
import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets"
const { Component,onWillStart ,useRef,onMounted } = owl
import { ChartRenderer } from "./chart_renderer.js";
// import { useService } from "@web/core/utils/hooks";
export class OwlSalesDashboard extends Component{
    setup(){
        
    }
}
OwlSalesDashboard.template = "sales_dashboard.OwlSalesDashboard"

OwlSalesDashboard.components = { KpiCard,ChartRenderer }
registry.category("actions").add("sales_dashboard.Dashboard",OwlSalesDashboard);