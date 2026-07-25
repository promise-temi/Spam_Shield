<template>
    <div class="gauge-wrapper">
        <div class="gauge">
            <div class="gauge-fill" :style="fillStyle"></div>
            <div class="gauge-cover">{{ percent }}%</div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        confidence: Number
    },
    computed: {
        percent() {
            return Math.round(this.confidence * 100);
        },
        fillStyle() {
            return {
                transform: `rotate(${this.percent * 1.8}deg)`,
                background: this.getColor()
            };
        }
    },
    methods: {
        getColor() {
            if (this.percent < 50) return "#ff3838";   // rouge
            if (this.percent < 75) return "#ffb038";   // orange
            return "#1eae17";                          // vert
        }
    }
};
</script>

<style scoped>
/* Conteneur */
.gauge-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 10px 0;
}

/* Jauge (plus grande et plus arrondie) */
.gauge {
    width: 200px;
    height: 100px;
    background: #e6e6e6;
    border-radius: 200px 200px 0 0;
    position: relative;
    overflow: hidden;
}

/* Remplissage */
.gauge-fill {
    width: 200px;
    height: 100px;
    transform-origin: center bottom;
    transition: transform 0.6s ease, background 0.3s ease;
}

/* Couverture (fond propre, arrondi parfait) */
.gauge-cover {
    width: 150px;
    height: 75px;
    background: #ffffff;
    border-radius: 150px 150px 0 0;
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 26px;
    font-weight: bold;
    color: #03005B;
}
</style>
