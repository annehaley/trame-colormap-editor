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
              tension: 0.4,
              borderWidth: 1,
              pointHitRadius: 25,
            },
          ],
        },
        options: {
          scales: {
            y: {
              min: 0,
              max: 1,
            },
            x: {
              min: 0,
              max: 100,
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
            dragData: {
              round: 1,
              dragX: true,
              showTooltip: true,
              onDrag: function (e) {
                e.target.style.cursor = "grabbing";
              },
              onDragEnd: function (e, datasetIndex, index, value) {
                e.target.style.cursor = "default";
                console.log(datasetIndex, index, value);
              },
            },
          },
        },
      },
    };
  },
  mounted() {
    this.ctx = (
      document.getElementById("chartJSContainer") as HTMLCanvasElement
    ).getContext("2d");
    this.chartInstance = new Chart(this.ctx, this.options);
  },
};
</script>

<template>
  <div class="curve-editor">
    <canvas id="chartJSContainer" height="50"></canvas>
  </div>
</template>

<style scoped>
.curve-editor {
  height: 150px;
  width: 100%;
  position: absolute;
  top: 30px;
  z-index: 5;
}
</style>
