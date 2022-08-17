<script lang="ts">
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
  setup(props) {

    console.log('custom color map editor mounted')

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
  hello
  {{ props }}
  <v-btn @click="triggerClick">Custom click</v-btn>
  <v-btn @click="triggerChange">Custom change</v-btn>
</div>
</template>
