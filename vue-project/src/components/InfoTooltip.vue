<script lang="ts">
import { HistogramData } from "../utils/types";
export default {
  props: {
    targets: {
      type: Array,
      required: true,
    },
    container: {
      type: HTMLElement,
      required: true,
    },
    histogramData: {
      type: Object as () => HistogramData,
      required: true,
    },
    positionToScalar: {
      type: Function,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      show: false,
      targetValue: undefined,
      binInfo: undefined,
    };
  },
  computed: {
    numBins() {
      return this.histogramData.counts.length;
    },
    binSize() {
      return (
        (this.histogramData.range[1] - this.histogramData.range[0]) /
        this.numBins
      );
    },
    bins() {
      const bins = [];
      for (var i = 0; i < this.numBins; i++) {
        const lower = Math.round(
          this.histogramData.range[0] + this.binSize * i
        );
        const upper = Math.round(
          this.histogramData.range[0] + this.binSize * (i + 1)
        );
        bins.push([lower, upper]);
      }
      return bins;
    },
  },
  methods: {
    moveTooltip(e) {
      if (this.targets.includes(e.target)) {
        this.show = true;
        this.$nextTick(() => {
          if (this.$refs.tooltip) {
            const left = e.pageX - this.container.offsetLeft;
            const top = e.pageY - this.container.offsetTop;
            this.$refs.tooltip.$el.style.left = left + "px";
            this.$refs.tooltip.$el.style.top = top + "px";
            this.targetValue = Math.round(this.positionToScalar(left - 20));
          }
          if (e.target.className.includes("histogram-canvas")) {
            const proportion =
              (this.targetValue - this.histogramData.range[0]) /
              (this.histogramData.range[1] - this.histogramData.range[0]);
            const binNumber = Math.floor(this.numBins * proportion);
            this.binInfo = {
              number: binNumber,
              count: this.histogramData.counts[binNumber],
              range: this.bins[binNumber],
            };
          } else {
            this.binInfo = undefined;
          }
        });
      } else {
        this.show = false;
        this.targetValue = undefined;
        this.binInfo = undefined;
      }
    },
  },
  mounted() {
    document.addEventListener("mousemove", this.moveTooltip, false);
  },
};
</script>

<template>
  <v-card v-show="show" ref="tooltip" :dark="dark" class="mouse-tooltip pa-2">
    <div v-if="targetValue">Value = {{ targetValue }}</div>
    <div v-if="binInfo && binInfo.range" class="caption">
      Bin range: {{ binInfo.range[0] }}...{{ binInfo.range[1] }}
    </div>
    <div v-if="binInfo" class="caption">Bin count: {{ binInfo.count }}</div>
    <div v-else class="caption">Click to add control point</div>
  </v-card>
</template>

<style scoped>
.mouse-tooltip {
  width: fit-content;
  position: absolute;
  z-index: 4;
}
</style>
