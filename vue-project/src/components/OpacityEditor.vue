<script lang="ts">
import clamp from "../utils/clamp";
import { Chart, registerables } from "chart.js";
import "chartjs-plugin-dragdata";
Chart.register(...registerables);

function registerPlugin(that) {
  Chart.register({
    id: "advanced_line_controls",
    beforeDatasetsDraw: (chart) => {
      const { ctx, width, height } = chart;
      const chartMargins = {
        x: 30,
        y: 10,
      };
      const w = width - chartMargins.x * 2;
      const h = height - chartMargins.y * 2;

      const svgns = "http://www.w3.org/2000/svg";
      const editableNodesContainer = document.getElementById(
        "editableNodesContainer"
      );
      function createEditableNode(x, y, m, s, controlPoints) {
        let primaryFill = "#000";
        let secondaryFill = "#fff";
        if (that.dark) {
          primaryFill = "#fff";
          secondaryFill = "#000";
        }
        // draggable node
        var circle = document.createElementNS(svgns, "circle");
        circle.setAttributeNS(null, "cx", x);
        circle.setAttributeNS(null, "cy", y);
        circle.setAttributeNS(null, "r", "3");
        circle.setAttributeNS(null, "fill", primaryFill);
        editableNodesContainer.appendChild(circle);

        controlPoints.forEach((cp, index) => {
          var control = document.createElementNS(svgns, "circle");
          var shiftedX = index === 0 ? cp.x - 10 : cp.x + 10;
          control.setAttributeNS(null, "cx", shiftedX);
          control.setAttributeNS(null, "cy", cp.y);
          control.setAttributeNS(null, "r", "3");
          control.setAttributeNS(null, "stroke", primaryFill);
          control.setAttributeNS(null, "fill", secondaryFill);
          control.setAttributeNS(
            null,
            "style",
            "position: relative; z-index: 2"
          );
          editableNodesContainer.appendChild(control);
        });
      }

      const contextData = that.currentData.map((point) => {
        return {
          x: (point.x / 100) * w + chartMargins.x,
          y: h - point.y * h + chartMargins.y,
          m: point.m,
          s: point.s,
        };
      });

      ctx.lineWidth = 3;
      ctx.lineCap = "round";
      ctx.fillStyle = that.gradient;
      if (that.dark) ctx.strokeStyle = "#fff";
      that.controlPoints = Array(contextData.length);
      for (var i = 0; i < contextData.length - 1; i++) {
        const pointA = contextData[i];
        const pointB = contextData[i + 1];
        if (i === 0) {
          ctx.beginPath();
          ctx.moveTo(pointA.x, pointA.y);
        }
        const cp1 = {
          x: pointA.x + (pointB.x - pointA.x) * pointA.s,
          y: pointA.y,
        };
        const cp2 = {
          x: pointB.x - (pointB.x - pointA.x) * pointB.s,
          y: pointB.y,
        };
        ctx.bezierCurveTo(cp1.x, cp1.y, cp2.x, cp2.y, pointB.x, pointB.y);
        if (!that.controlPoints[i]) that.controlPoints[i] = [];
        if (!that.controlPoints[i + 1]) that.controlPoints[i + 1] = [];
        that.controlPoints[i].push(cp1);
        that.controlPoints[i + 1].push(cp2);
      }
      ctx.stroke();
      ctx.lineWidth = 0;
      ctx.lineTo(w + chartMargins.x, h + chartMargins.y);
      ctx.lineTo(chartMargins.x, h + chartMargins.y);
      ctx.closePath();
      ctx.fill();

      if (editableNodesContainer) {
        editableNodesContainer.innerHTML = "";
        contextData.forEach((point, index) =>
          createEditableNode(
            point.x,
            point.y,
            point.m,
            point.s,
            index === that.focusedPoint ? that.controlPoints[index] : []
          )
        );
      }

      return false; // cancel datasets draw
    },
  });
}

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
    opacityNodes: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentData: [],
      controlPoints: [],
      focusedPoint: undefined,
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
              data: this.currentData.map((point) => ({
                x: point.x,
                y: point.y,
              })),
              pointHitRadius: 15,
              borderColor: this.dark ? "#fff" : "#000",
            },
          ],
        },
        options: {
          responsive: true,
          animation: false,
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
            advanced_line_controls: true,
            tooltip: {
              callbacks: {
                title: function (context) {
                  return this.toTrueValue(context[0].parsed.x);
                }.bind(this),
              },
            },
            legend: { display: false },
            dragData: {
              round: 1,
              dragX: true,
              showTooltip: true,
              onDrag: (e, dIndex, index) => {
                e.target.style.cursor = "grabbing";
                this.focusedPoint = index;
              },
              onDragEnd: (e) => {
                e.target.style.cursor = "default";
              },
            },
          },
        },
      };
    },
  },
  methods: {
    toTrueValue(x) {
      return Math.round(
        (x / 100) * (this.dataRange[1] - this.dataRange[0]) + this.dataRange[0]
      );
    },
    toProportionalValue(x) {
      return (
        ((x - this.dataRange[0]) / (this.dataRange[1] - this.dataRange[0])) *
        100
      );
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
    addDatum(x, y, m, s) {
      this.chartInstance.data.labels = this.insertSortedByFunction(
        this.chartInstance.data.labels,
        x,
        (a, b) => a < b
      );
      this.currentData = this.insertSortedByFunction(
        this.currentData,
        { x, y, m, s },
        (a, b) => a.x < b.x
      );
      this.chartInstance.data.datasets[0].data = this.currentData;
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
      this.addDatum(x, y, 0.5, 0);
      this.update();
    },
    render() {
      // populate with input data
      this.currentData = [];
      this.opacityNodes.forEach(([x, y, m, s]) => {
        this.addDatum(this.toProportionalValue(x), y, m, s);
      });
    },
    update() {
      this.$emit(
        "update",
        this.currentData.map(({ x, y, m, s }) => [this.toTrueValue(x), y, m, s])
      );
    },
  },
  mounted() {
    registerPlugin(this);

    this.canvas = document.getElementById(
      "chartJSContainer"
    ) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext("2d");

    // create gradient fill
    this.gradient = this.ctx.createLinearGradient(0, 0, 0, 100);
    this.gradient.addColorStop(1, "transparent");
    this.gradient.addColorStop(0, this.dark ? "white" : "black");

    this.chartInstance = new Chart(this.ctx, this.chartOptions);
    this.render();
  },
  watch: {
    opacityNodes() {
      this.render();
    },
  },
};
</script>

<template>
  <div class="curve-editor">
    <div class="responsive-size">
      <canvas id="chartJSContainer" height="50"></canvas>
      <svg
        id="editableNodesContainer"
        class="nodes-container"
        xmlns="http://www.w3.org/2000/svg"
        width="100%"
      />
    </div>
    <div class="x-labels">
      <p>{{ dataRange[0] }}</p>
      <p>{{ dataRange[1] }}</p>
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
.nodes-container {
  position: absolute;
  top: 0;
  pointer-events: none;
}
.x-labels {
  display: flex;
  justify-content: space-between;
  padding: 0px 30px;
  margin-top: -10px;
  width: 100%;
}
</style>
