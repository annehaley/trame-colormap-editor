<script lang="ts">
import ColorNode from "./ColorNode.vue";
import { drawHistogram, drawGradient } from "../utils/canvasDrawing";
import { HistogramData } from "../utils/types";

export default {
  components: { ColorNode },
  props: {
    value: {
      type: Array,
      required: true,
    },
    histogramData: {
      type: Object as () => HistogramData,
      required: true,
    },
    dark: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    fullRange() {
      return this.histogramData.range;
    },
  },
  data() {
    return {
      colorLine: undefined,
      colorNodes: this.value,
    };
  },
  methods: {
    render() {
      this.colorLine = this.$refs.colorLine;
      drawHistogram(
        this.histogramData,
        this.$refs.histogram,
        this.$refs.histogramLabels,
        this.dark
      );
      drawGradient(this.colorNodes, this.$refs.gradientBox, this.fullRange);
    },
    update() {
      this.colorNodes = [
        [-3000, 0, 0, 0],
        [0, 1, 0, 1],
        [1000, 1, 0, 0],
        [4000, 0, 1, 0],
      ];
      this.$emit("input", this.colorNodes);
    },
  },
  mounted() {
    this.render();
  },
  updated() {
    this.render();
  },
};
</script>

<template>
  <div :class="!dark ? 'widget-container' : 'widget-container dark'">
    <canvas ref="histogram" class="histogram-canvas indented" />
    <div ref="histogramLabels" class="histogram-labels indented" />
    <div ref="colorLine" :class="!dark ? 'color-line' : 'color-line dark'">
      <canvas ref="gradientBox" class="gradient-box indented" />
      <color-node
        v-for="node in colorNodes"
        :key="node[0]"
        :scalarValue="node[0]"
        :rgbValue="node.slice(1)"
        :histogramData="histogramData"
        :colorLine="colorLine"
        :fullRange="fullRange"
        :dark="dark"
      />
    </div>
    <v-btn @click="update" class="update-btn">Update</v-btn>
  </div>
</template>

<style scoped>
.dark {
  color: white !important;
}
.widget-container {
  display: flex;
  flex-direction: column;
  row-gap: 5px;
  position: relative;
  margin: 10px;
}
.indented {
  margin: 0px 20px;
  max-width: calc(100% - 40px);
}
.histogram-canvas {
  height: 100px;
}
.histogram-labels {
  display: flex;
  justify-content: space-between;
}
.gradient-box {
  height: 25px;
  width: 100%;
  position: absolute;
  top: -20px;
  z-index: -1;
}
.color-line {
  z-index: 2;
  margin-top: 15px;
  outline: 1px solid black;
  margin-bottom: 50px;
  position: relative;
}
.color-line.dark {
  outline: 1px solid white;
}
.update-btn {
  justify-self: flex-end;
}
</style>
