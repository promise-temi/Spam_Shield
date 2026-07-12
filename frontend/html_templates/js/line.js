// Les 14 jours
const x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];


// Les informations de toutes tes courbes
const series = [
    {
        name: "HAM Prédiction IA",
        color: "#1eae17",
        values: [10, 15, 13, 17, 12, 16, 19, 14, 18, 20, 17, 21, 19, 23]
    },

    {
        name: "SPAM Prédiction IA",
        color: "#fd3831",
        values: [16, 5, 11, 9, 13, 10, 15, 12, 8, 14, 11, 16, 13, 18]
    },

    {
        name: "SPAM Patterns Interdits",
        color: "#404040",
        values: [4, 7, 5, 8, 6, 9, 7, 10, 8, 11, 9, 12, 10, 13]
    },

    {
        name: "SPAM Low Confidence",
        color: "#8026fd",
        values: [2, 4, 3, 5, 4, 6, 5, 7, 4, 8, 6, 7, 5, 9]
    },

    {
        name: "HAM Corrigés",
        color: "#57affc",
        values: [1, 2, 1, 3, 2, 4, 3, 2, 5, 4, 3, 5, 4, 6]
    },

    {
        name: "SPAM Corrigés",
        color: "#ff981a",
        values: [3, 1, 2, 4, 2, 3, 5, 3, 4, 6, 4, 5, 7, 6]
    }
];


// Création automatique de toutes les traces
const data = series.map(serie => ({
    x: x,
    y: serie.values,

    name: serie.name,

    mode: 'lines',

    line: {
        color: serie.color,
        width: 1.5
    },

    
}));


const layout = {
    // showlegend: false,
    margin: {
        l: 50,
        r: 20,
        t: 20,
        b: 50
    },
    paper_bgcolor: "#F1F5FC",   // ← background global
    plot_bgcolor: "transparent", // ← fond derrière
    xaxis: {
        title: {
            text: "Temps",
            font: {
                size: 10,
                color: "#03005B"
            },
            standoff: 10
        },

        automargin: true,
        zeroline: false
    },

    yaxis: {
        title: {
            text: "Nombre de messages",
            font: {
                size: 10,
                color: "#03005B"
            },
            standoff: 5
        },

        automargin: true,
        zeroline: false
    },

    legend: {
    orientation: "h",

    x: 0.5,
    xanchor: "center",

    y: -0.2,
    yanchor: "top"
    },
    font: {
        size: 10,   // ← taille du texte de la légende
        color: "#03005B",
    }
};


const config = {
    responsive: true,
    displaylogo: false
};


Plotly.newPlot(
    "evo-per-cat",
    data,
    layout,
    config
);