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
        confidence: Number // valeur entre 0 et 1
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
.gauge-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
}

.gauge {
    width: 160px;
    height: 80px;
    background: #e6e6e6;
    border-radius: 160px 160px 0 0;
    position: relative;
    overflow: hidden;
}

.gauge-fill {
    width: 160px;
    height: 80px;
    background: #1eae17;
    transform-origin: center bottom;
    transition: transform 0.6s ease, background 0.3s ease;
}

.gauge-cover {
    width: 120px;
    height: 60px;
    background: #F1F5FC;
    border-radius: 120px 120px 0 0;
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 22px;
    font-weight: bold;
    color: #03005B;
}
</style>
