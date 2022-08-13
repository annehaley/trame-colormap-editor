<script lang="ts">
import { defineComponent, onMounted } from '@vue/composition-api'

export default defineComponent({
  setup(props) {
    console.log('props:', props)

    function  triggerClick() {
      this.$emit('click');
    }
    function triggerChange() {
      this.$emit('change');
    }

    return {
      triggerClick,
      triggerChange,
    }
  },
})
</script>



<template>
<div>
  <v-btn @click="triggerClick">Custom click</v-btn>
  <v-btn @click="triggerChange">Custom change</v-btn>
</div>
</template>
