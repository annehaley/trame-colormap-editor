<script lang="ts">
import ColorNode from "./ColorNode.vue";
import { drawHistogram, drawGradient } from "../utils/canvasDrawing";
import { HistogramData } from "../utils/types";
import ColorNodeList from "./ColorNodeList.vue";
import clamp from "../utils/clamp";
import InfoTooltip from "./InfoTooltip.vue";
import { listenDragSelection } from "../utils/drag";

export default {
  components: { ColorNode, ColorNodeList, InfoTooltip },
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
      selectedNodes: [],
      visibleColorPicker: undefined,
      filterRange: undefined,
    };
  },
  methods: {
    nodeToTableItem(node, index) {
      const rgb = node.slice(1).map((value) => value * 255);
      return {
        id: index,
        value: node[0],
        rgbString: `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`,
        rgb,
        index,
      };
    },
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
      return Math.round(
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
    createNodeAtClick(event) {
      const newNodeValue = Math.round(this.positionToScalar(event.layerX));
      const newNode = [newNodeValue, 0, 0, 0];
      this.colorNodes = [...this.colorNodes, newNode];
      this.selectedNodes = [
        this.nodeToTableItem(newNode, this.colorNodes.length - 1),
      ];
      this.render();
    },
    updateFilterRange(newRange) {
      this.filterRange = newRange;
    },
    updateSelectedNodes(selected) {
      this.selectedNodes = selected;
    },
    updateVisibleColorPicker(visibleColorPicker) {
      this.visibleColorPicker = visibleColorPicker;
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
    listenDragSelection(
      this.$refs.histogramLabels,
      (startPos: number, endPos: number) => {
        const startValue = this.positionToScalar(startPos);
        const endValue = this.positionToScalar(endPos);
        this.filterRange = [startValue, endValue];
      }
    );
    this.render();
  },
  updated() {
    this.render();
  },
};
</script>

<template>
  <div
    ref="container"
    :class="!dark ? 'widget-container' : 'widget-container dark'"
  >
    <v-tooltip right>
      <template v-slot:activator="{ on, attrs }">
        <v-icon class="help-circle" :dark="dark" v-bind="attrs" v-on="on">
          mdi-help-circle
        </v-icon>
      </template>
      <div class="caption">
        Double click gradient bar to create new control point
        <br />
        Double click existing control point to edit color
        <br />
        Drag along section of gradient to select range and filter table
        <br />
        Drag existing control point to edit its value
      </div>
    </v-tooltip>
    <info-tooltip
      v-if="colorLine"
      :dark="dark"
      :container="$refs.container"
      :positionToScalar="positionToScalar"
      :histogramData="histogramData"
      :nodes="colorNodes"
      :targets="[$refs.histogram, $refs.histogramLabels, $refs.colorLine]"
    />
    <canvas ref="histogram" class="histogram-canvas indented" />
    <div
      ref="histogramLabels"
      class="histogram-labels indented"
      @dblclick="createNodeAtClick"
    />
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
        :visibleColorPicker="visibleColorPicker"
        :scalarToPosition="scalarToPosition"
        :positionToScalar="positionToScalar"
        @change="updateSingleNode"
        @pick="updateVisibleColorPicker"
        @updaterange="updateFilterRange"
      />
    </div>
    <color-node-list
      :nodes="colorNodes"
      :selectedNodes="selectedNodes"
      :visibleColorPicker="visibleColorPicker"
      :nodeToTableItem="nodeToTableItem"
      :filterRange="filterRange"
      :dark="dark"
      @change="updateNodeList"
      @select="updateSelectedNodes"
      @pick="updateVisibleColorPicker"
    />
    <br />
    <v-btn @click="update" class="update-btn">Update</v-btn>
  </div>
</template>

<style>
.dark {
  color: white !important;
}
.help-circle {
  position: absolute;
  left: 0;
  top: 0;
  width: 30px;
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
  position: absolute;
  width: 100%;
  top: 140px;
  z-index: 3;
  justify-content: space-between;
  font-weight: 900;
  -webkit-text-fill-color: white;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: black;
}
.gradient-box {
  height: 45px;
  width: 100%;
  position: absolute;
  top: -30px;
  z-index: -1;
}
.color-line {
  z-index: 2;
  outline: 1px solid black;
  position: relative;
  margin: 20px 0px;
}
.color-line.dark {
  outline: 1px solid white;
}
.update-btn {
  justify-self: flex-end;
}
</style>
