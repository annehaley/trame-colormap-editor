<script lang="ts">
import { HistogramData } from "../utils/types";
import { clamp } from "../utils/canvasDrawing";

export default {
  props: {
    scalarValue: {
      type: Number,
      required: true,
    },
    rgbValue: {
      type: Array,
      required: true,
    },
    histogramData: {
      type: Object as () => HistogramData,
      required: true,
    },
    colorLine: {
      required: true,
    },
    fullRange: {
      type: Array,
      required: true,
    },
    dark: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      xPosition: 0,
    };
  },
  computed: {
    rgbString() {
      const rgb = this.rgbValue.map((value) => value * 255);
      return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
    },
  },
  methods: {
    updateXPosition() {
      if (!this.colorLine) return;
      const clampedScalar = clamp(
        this.scalarValue,
        this.fullRange[0],
        this.fullRange[1]
      );
      const lineLength = this.colorLine.clientWidth;
      const maxPosition = lineLength - 10;
      const calculatedPosition =
        lineLength *
          ((clampedScalar - this.fullRange[0]) /
            (this.fullRange[1] - this.fullRange[0])) -
        7; // this is half the width of the box;
      this.xPosition =
        calculatedPosition < maxPosition ? calculatedPosition : maxPosition;
    },
  },
  mounted() {
    this.updateXPosition();
  },
  updated() {
    this.updateXPosition();
  },
};
</script>

<template>
  <div
    v-if="colorLine"
    :class="!dark ? 'color-square' : 'color-square dark'"
    :style="`left: ${xPosition}px; background-color: ${rgbString}`"
  />
</template>

<style scoped>
.color-square {
  position: absolute;
  top: 0px;
  margin-top: 10px;
  height: 15px;
  width: 15px;
  border: 3px solid black;
}
.color-square.dark {
  border: 3px solid white;
}
.color-square::after {
  content: "\25B2";
  font-size: 18px;
  position: relative;
  top: -22px;
  left: -5%;
}
</style>
