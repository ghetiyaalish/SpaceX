/** @odoo-module **/
import { registry } from "@web/core/registry";
const { Component,onWillStart ,useRef,onMounted } = owl
import { loadJS } from "@web/core/assets"


// import { useService } from "@web/core/utils/hooks";
export class ChartRenderer extends Component{
    setup(){
        this.chartRef = useRef("chart")
        onWillStart(async()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })
        onMounted(()=>{
            this.renderChart()
        })
    }
    renderChart(){
        new Chart(this.chartRef.el,
            {
              type: this.props.type,
              data: {
                labels: [
                    'Red',
                    'Blue',
                    'Yellow'
                  ],
                  datasets: [
                    {
                    label: 'My First Dataset',
                    data: [50, 60, 70],
                    hoverOffset: 4
                  },
                  {
                    label: 'My Second Dataset',
                    data: [80,60,40],
                    hoverOffset: 4
                  }
                ]
              },
              options:{
                responsive:true,
                plugins:{
                    legend:{
                        position:'bottom'
                    },
                    title:{
                        display:true,
                        text:this.props.title,
                        position:'bottom',
                    }
                }
              }
            }
          );

    }

}
ChartRenderer.template = "sales_dashboard.ChartRenderer"
