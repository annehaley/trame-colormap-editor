<script lang="ts">
import { HistogramData } from "../utils/types";
import clamp from "../utils/clamp";
import makeDraggable from "../utils/drag";

export default {
  props: {
    index: {
      type: Number,
      required: true,
    },
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
    gradientLength() {
      // -40 accounts for the 20px padding on either side
      return this.colorLine.clientWidth - 40;
    },
    rangeDifference() {
      return this.fullRange[1] - this.fullRange[0];
    },
  },
  methods: {
    scalarToPosition(scalar) {
      const clampedScalar = clamp(scalar, this.fullRange[0], this.fullRange[1]);
      const calculatedPosition =
        this.gradientLength *
        ((clampedScalar - this.fullRange[0]) / this.rangeDifference);
      return clamp(calculatedPosition, -10, this.gradientLength) + 20;
    },
    positionToScalar(position) {
      position -= 10; // -10 accounts for half the square width
      return (
        (position / this.gradientLength) * this.rangeDifference +
        this.fullRange[0]
      );
    },
    onDragSquare() {
      const scalar = this.positionToScalar(this.$el.offsetLeft);
      const newValue = [scalar, ...this.rgbValue];
      this.$emit("change", this.index, newValue);
    },
    updateXPosition() {
      if (!this.colorLine) return;
      this.xPosition = this.scalarToPosition(this.scalarValue);
      makeDraggable(
        this.$el,
        this.onDragSquare,
        [-10, this.colorLine.clientWidth - 10],
        [],
        this.fullRange.map((value) => this.scalarToPosition(value) - 10),
        []
      );
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
    ref="colorSquare"
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
  height: 20px;
  width: 20px;
  border: 3px solid black;
}
.color-square.dark {
  border: 3px solid white;
}
.color-square::after {
  content: "\25B2";
  font-size: 16px;
  position: relative;
  top: -20px;
}
</style>
