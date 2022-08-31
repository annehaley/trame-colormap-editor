<script lang="ts">
import { defineComponent } from "vue";
import ColormapEditor from "./components/ColormapEditor.vue";

export default defineComponent({
  name: "HomePage",
  components: {
    ColormapEditor,
  },
  setup() {
    const histogramData = {
      counts: [
        7417676, 0, 14464981, 7114126, 5670523, 164754, 16188, 5310, 3273, 8321,
      ],
      range: [-2048.0, 3071.0],
    };
    const value = [
      [-2369, 1, 0, 0],
      [-2048, 0, 1, 0],
      [511.5, 0, 0, 1],
      [3071, 0, 0, 0],
      [3392, 1, 1, 1],
    ];

    return {
      histogramData,
      value,
    };
  },
});
</script>

<template>
  <div class="container">
    <colormap-editor :histogram-data="histogramData" :value="value" dark />
  </div>
</template>

<style scoped>
.container {
  margin: 10px;
  padding: 10px;
  border: 1px dashed black;
  width: 400px;
  background-color: black;
}
</style>
