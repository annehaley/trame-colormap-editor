// Modified from
https://raw.githubusercontent.com/chrispahm/chartjs-plugin-dragdata/master/docs/index.html

<script lang="ts">
import { Chart, registerables } from "chart.js";
import "chartjs-plugin-dragdata";
Chart.register(...registerables);

export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
    dataRange: {
      type: Array,
      required: true,
    },
  },
  components: {},
  data() {
    return {
      options: {
        type: "line",
        data: {
          labels: this.dataRange,
          datasets: [
            {
              label: "Opacity",
              data: [1, 1],
              fill: true,
              tension: 0.5,
              borderWidth: 1,
              pointHitRadius: 25,
              backgroundColor: this.dark ? "#fff" : "#000",
              pointBackgroundColor: this.dark ? "#fff" : "#000",
              borderColor: this.dark ? "#fff" : "#000",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              min: 0,
              max: 1,
            },
            x: {
              min: 0,
              max: 100,
              display: false,
            },
          },
          layout: {
            padding: {
              right: 30,
            },
          },
          onHover: function (e) {
            const point = e.chart.getElementsAtEventForMode(
              e,
              "nearest",
              { intersect: true },
              false
            );
            if (point.length) e.native.target.style.cursor = "grab";
            else e.native.target.style.cursor = "default";
          },
          plugins: {
            legend: {
              display: false,
            },
            dragData: {
              round: 1,
              dragX: true,
              showTooltip: true,
              onDrag: function (e) {
                e.target.style.cursor = "grabbing";
              },
              onDragEnd: function (e, datasetIndex, index, value) {
                e.target.style.cursor = "default";
                console.log(index, value);
              },
            },
          },
        },
      },
    };
  },
  mounted() {
    this.canvas = document.getElementById(
      "chartJSContainer"
    ) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d");
    this.gradient = this.ctx.createLinearGradient(0, 0, 0, 100);
    this.gradient.addColorStop(1, "transparent");
    this.gradient.addColorStop(0, this.dark ? "white" : "black");
    this.options.data.datasets[0].backgroundColor = this.gradient;
    this.chartInstance = new Chart(this.ctx, this.options);
  },
};
</script>

<template>
  <div class="curve-editor">
    <div class="responsive-size">
      <canvas id="chartJSContainer" height="50"></canvas>
    </div>
  </div>
</template>

<style scoped>
.curve-editor {
  height: 110px;
  width: calc(100% + 20px);
  position: absolute;
  top: 23px;
  left: -10px;
  z-index: 5;
}
.responsive-size {
  position: relative;
  height: 100%;
  width: 100%;
}
</style>
