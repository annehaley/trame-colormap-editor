<script lang="ts">
import ColorNode from "./ColorNode.vue";
import { drawHistogram, drawGradient } from "../utils/canvasDrawing";
import { HistogramData } from "../utils/types";
import ColorNodeList from "./ColorNodeList.vue";
import clamp from "../utils/clamp";

export default {
  components: { ColorNode, ColorNodeList },
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
    dataRange() {
      return this.histogramData.range;
    },
    gradientLength() {
      // -40 accounts for the 20px padding on either side
      return this.$refs.colorLine.clientWidth - 40;
    },
    rangeDifference() {
      return this.dataRange[1] - this.dataRange[0];
    },
  },
  data() {
    return {
      colorLine: undefined,
      colorNodes: this.value,
    };
  },
  methods: {
    scalarToPosition(scalar) {
      let calculatedPosition =
        this.gradientLength *
        ((scalar - this.dataRange[0]) / this.rangeDifference);
      calculatedPosition = clamp(
        calculatedPosition,
        -20,
        this.gradientLength + 20
      );
      calculatedPosition += 10; // +10 accounts for half the square width
      return calculatedPosition;
    },
    positionToScalar(position) {
      position -= 10; // -10 accounts for half the square width
      return (
        (position / this.gradientLength) * this.rangeDifference +
        this.dataRange[0]
      );
    },
    getFullRange() {
      return [
        this.positionToScalar(this.scalarToPosition(this.dataRange[0]) - 20),
        this.positionToScalar(this.scalarToPosition(this.dataRange[1]) + 20),
      ].map((val) => Math.floor(val));
    },
    render() {
      this.colorLine = this.$refs.colorLine;
      drawHistogram(
        this.histogramData,
        this.$refs.histogram,
        this.$refs.histogramLabels,
        this.dark
      );
      drawGradient(
        this.colorNodes,
        this.$refs.gradientBox,
        this.getFullRange(),
        this.dataRange[0]
      );
    },
    updateSingleNode(nodeIndex, newValue) {
      this.colorNodes[nodeIndex] = newValue;
      this.colorNodes = [...this.colorNodes];
      this.render();
    },
    updateNodeList(newList) {
      this.colorNodes = newList;
      this.render();
    },
    update() {
      this.$emit("input", [...this.colorNodes]);
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
      <canvas ref="gradientBox" class="gradient-box" />
      <color-node
        v-for="(node, index) in colorNodes"
        :key="'node_' + index"
        :index="index"
        :scalarValue="node[0]"
        :rgbValue="node.slice(1)"
        :histogramData="histogramData"
        :colorLine="colorLine"
        :dataRange="dataRange"
        :dark="dark"
        :scalarToPosition="scalarToPosition"
        :positionToScalar="positionToScalar"
        @change="updateSingleNode"
      />
    </div>
    <color-node-list
      :nodes="colorNodes"
      :dark="dark"
      @change="updateNodeList"
    />
    <br />
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
  row-gap: 10px;
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
