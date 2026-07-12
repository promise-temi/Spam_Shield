let data2 = [
    {
        values:[12, 5, 6, 2, 2, 1],
        labels:["HAM Prédiction IA", "SPAM Prédiction IA", "SPAM Patterns Interdits", "SPAM low Confidence", "HAM Corrigés", "SPAM Corrigés"],
        type: "pie",
        hole: .4,
        
        marker:{
            colors:["#1eae17", "#fd3831", "#404040", "#8026fd", "#57affc", "#ff981a"]
        }
    }
];

let layout2 = {
    margin: { l: 10, r: 10, t: 20, b: 20 },
    paper_bgcolor: "#F1F5FC",   // ← background global
    plot_bgcolor: "transparent", // ← fond derrière le donut
  showlegend: true,
  legend: {
    x: 1,
    y: 0.5
  },
  font: {
        size: 10,   // ← taille du texte de la légende
        color: "#03005B",
    }

};

let config2 = {
    displaylogo: false,
    responsive: true
};

Plotly.newPlot('dis-per-cat', data2, layout2, config2);
