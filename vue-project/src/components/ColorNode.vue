<script lang="ts">
import { HistogramData } from "../utils/types";
import { clamp } from "../utils/canvasDrawing";
import makeDraggable from "../utils/drag";

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
    onDragSquare() {
      console.log(this.$el.offsetLeft);
    },
    updateXPosition() {
      if (!this.colorLine) return;
      const clampedScalar = clamp(
        this.scalarValue,
        this.fullRange[0],
        this.fullRange[1]
      );
      const lineLength = this.colorLine.clientWidth;
      const calculatedPosition =
        lineLength *
        ((clampedScalar - this.fullRange[0]) /
          (this.fullRange[1] - this.fullRange[0]));
      this.xPosition = clamp(calculatedPosition, -10, lineLength) - 10;
      makeDraggable(this.$el, this.onDragSquare, [-10, lineLength], []);
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
