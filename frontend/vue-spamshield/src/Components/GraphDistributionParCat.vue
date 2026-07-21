<template>
    <div id="dis-per-cat">
    </div>
</template>
<script>
export default{
    data(){
        return{
            pie_values : [12, 5, 6, 2, 2, 1],
            pie_labels : ["HAM Prédiction IA", "SPAM Prédiction IA", "SPAM Patterns Interdits", "SPAM low Confidence", "HAM Corrigés", "SPAM Corrigés"],
            labels_colors : ["#1eae17", "#fd3831", "#404040", "#8026fd", "#57affc", "#ff981a"],
        }
    },
    methods:{
        showPie(){
            // DATA
            let data = [
                {
                    values:this.pie_values,
                    labels: this.pie_labels,
                    type: "pie",
                    hole: .4,
                    marker:{
                        colors: this.labels_colors
                    }
                }
            ];

            // LAYOUT
            let layout = {
                margin: { l: 10, r: 10, t: 20, b: 20 },
                paper_bgcolor: "#F1F5FC",   // ← background global
                plot_bgcolor: "transparent", // ← fond derrière le donut
                showlegend: true,
                legend: {
                    x: 1,
                    y: 0.5
                },
                font: {
                        size: 13,   // ← taille du texte de la légende
                        color: "#03005B",
                    }

            };

            // CONFIG
            let config = {
                displaylogo: false,
                responsive: true
            };

            Plotly.newPlot('dis-per-cat', data, layout, config);
        }
    },
    mounted(){
        this.showPie();
    }
}
</script>