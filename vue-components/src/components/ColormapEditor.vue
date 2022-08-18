<script lang="ts">
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
  props: {
    value: {
      type: Array,
      required: true,
    },
    histogramData: {
      type: Array,
      required: true,
    }
  },
  setup(props) {

    console.log(props);
    console.log('custom color map editor mounted');

    function update() {
      this.$emit('input', [
        [-3000, 0, 0, 0],
        [0, 1, 0, 1],
        [1000, 1, 0, 0],
        [4000, 0, 1, 0]
      ]);
    }

    return {
      update,
    }
  },
})
</script>



<template>
<div>
  <v-btn @click="update">Update</v-btn>
</div>
</template>
