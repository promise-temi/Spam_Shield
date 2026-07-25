<!-- <template>
    <div id="dis-per-cat">
    </div>
</template>
<script>
export default{
    props:{
        graphValues_:Array
    },
    data(){
        return{
            pie_values : this.graphValues_,
            pie_labels : ["HAM Prédiction IA", "SPAM Prédiction IA", "SPAM Patterns Interdits", "SPAM Par Reclassement", "HAM Corrigés", "SPAM Corrigés"],
            labels_colors : ["#1eae17", "#fd3831", "#404040", "#8026fd", "#57affc", "#ff981a"],
        }
    },
    watch: {
        graphValues_(newVal) {
            this.pie_values = newVal;
            this.showPie();
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
</script> -->


<template>
    <div id="dis-per-cat"></div>
</template>

<script>
export default {
    props: {
        graphValues_: Array
    },
    data() {
        return {
            bar_values: [],
            bar_labels: [
                "HAM Prédit\t",
                "SPAM Prédit\t",
                "SPAM Métier\t",
                "SPAM Reclassés\t",
                "HAM Corrigés\t",
                "SPAM Corrigés\t"
            ],
            labels_colors: ["#1eae17", "#fd3831", "#404040", "#8026fd", "#57affc", "#ff981a"]
        };
    },
    watch: {
        graphValues_(newVal) {
            this.bar_values = newVal;
            this.showBar();
        }
    },
    methods: {
        showBar() {
            let data = [{
                x: this.bar_values,
                y: this.bar_labels,
                type: "bar",
                orientation: "h",
                marker: {
                    color: this.labels_colors
                }
            }];

            let layout = {
                margin: { l: 130, r: 40, t: 20, b: 20 },
                paper_bgcolor: "#F1F5FC",
                plot_bgcolor: "transparent",
                font: {
                    size: 13,
                    color: "#03005B"
                },
            };

            let config = {
                displaylogo: false,
                responsive: true
            };

            Plotly.newPlot("dis-per-cat", data, layout, config);
        }
    },
    mounted() {
        if (this.graphValues_.length > 0) {
            this.bar_values = this.graphValues_;
            this.showBar();
        }
    }
};
</script>
