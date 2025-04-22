/** @odoo-module **/
import { KpiCard } from "./kpi_card.js";
import { registry } from "@web/core/registry";
const { Component } = owl

// import { useService } from "@web/core/utils/hooks";
export class OwlSalesDashboard extends Component{}
OwlSalesDashboard.template = "sales_dashboard.OwlSalesDashboard"

OwlSalesDashboard.components = { KpiCard }
registry.category("actions").add("sales_dashboard.Dashboard",OwlSalesDashboard);