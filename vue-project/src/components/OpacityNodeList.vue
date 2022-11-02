<script lang="ts">
export default {
  props: {
    opacityNodes: {
      type: Array,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {};
  },
  methods: {},
  computed: {},
  watch: {},
};
</script>

<template>
  <v-data-table :dark="dark" class="mt-3">
    <template #top>
      <div class="px-3 d-flex caption">Opacity function nodes</div>
      <div :dark="dark" class="px-3 d-flex" style="align-items: center">
        <div class="text-caption">{{ opacityNodes.length }} Control Points</div>
      </div>
    </template>
  </v-data-table>
</template>

<style></style>
