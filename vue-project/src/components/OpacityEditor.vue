// Modified from
https://raw.githubusercontent.com/chrispahm/chartjs-plugin-dragdata/master/docs/index.html

<script lang="ts">
import clamp from "../utils/clamp";
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
      currentData: [],
    };
  },
  computed: {
    chartOptions() {
      return {
        type: "line",
        data: {
          datasets: [
            {
              label: "Opacity",
              data: this.currentData,
              fill: true,
              tension: 0.5,
              borderWidth: 1,
              pointHitRadius: 25,
              backgroundColor: this.gradient,
              pointBackgroundColor: this.dark ? "#fff" : "#000",
              borderColor: this.dark ? "#fff" : "#000",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { min: 0, max: 1 },
            x: { min: 0, max: 100, display: false, type: "linear" },
          },
          layout: { padding: { right: 30 } },
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
          onClick: this.clickChart,
          plugins: {
            legend: { display: false },
            dragData: {
              round: 1,
              showTooltip: true,
              onDrag: (e) => {
                e.target.style.cursor = "grabbing";
              },
              onDragEnd: this.completeDrag,
            },
          },
        },
      };
    },
  },
  methods: {
    completeDrag(e, dIndex, index, value) {
      e.target.style.cursor = "default";
      console.log(index, value);
    },
    insertSortedByFunction(array, value, func) {
      // from https://stackoverflow.com/a/21822316
      var low = 0;
      var high = array.length;

      while (low < high) {
        var mid = (low + high) >>> 1;
        if (func(array[mid], value)) low = mid + 1;
        else high = mid;
      }
      array.splice(low, 0, value);
      return array;
    },
    addDatum(x, y) {
      this.chartInstance.data.labels = this.insertSortedByFunction(
        this.chartInstance.data.labels,
        x,
        (a, b) => a < b
      );
      // this.chartInstance.data.labels.push(x);
      console.log(this.chartInstance.data.labels);
      // this.currentData.push({ x, y });
      this.currentData = this.insertSortedByFunction(
        this.currentData,
        { x, y },
        (a, b) => a.x < b.x
      );
      this.chartInstance.update();
    },
    clickChart(e) {
      const { height, width } = e.chart.chartArea;
      const x = clamp(Math.round(((e.x - 40) / width) * 100), 0, 100);
      const y = clamp(
        parseFloat(((height - (e.y - 10)) / height).toFixed(1)),
        0,
        1
      );
      this.addDatum(x, y);
    },
  },
  mounted() {
    this.canvas = document.getElementById(
      "chartJSContainer"
    ) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d");

    // create gradient fill
    this.gradient = this.ctx.createLinearGradient(0, 0, 0, 100);
    this.gradient.addColorStop(1, "transparent");
    this.gradient.addColorStop(0, this.dark ? "white" : "black");

    this.chartInstance = new Chart(this.ctx, this.chartOptions);

    // populate with two endpoints
    this.addDatum(0, 1);
    this.addDatum(100, 1);
    this.addDatum(49, 0.5);
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
