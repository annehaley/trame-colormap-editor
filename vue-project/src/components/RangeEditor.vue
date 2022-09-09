<script lang="ts">
export default {
  props: {
    selectedNodes: {
      type: Array,
      required: true,
    },
    fullRange: {
      type: Array,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      originalRange: undefined,
      newRange: undefined,
    };
  },
  methods: {
    updateOriginalRange() {
      const values = this.selectedNodes.map((node) => node.value);
      this.originalRange = [Math.min(...values), Math.max(...values)];
      this.newRange = [...this.originalRange];
    },
  },
  mounted() {
    this.updateOriginalRange();
  },
  watch: {
    selectedNodes() {
      this.updateOriginalRange();
    },
  },
};
</script>

<template>
  <v-card :dark="dark" v-if="selectedNodes.length > 1" class="mt-3 pa-3">
    <div class="d-flex" style="justify-content: space-between">
      <span>Adjust range for selected nodes</span>
      <v-btn
        small
        v-if="
          newRange[0] != originalRange[0] || newRange[1] != originalRange[1]
        "
        >Adjust</v-btn
      >
      <span
        >Original range: {{ originalRange[0] }}...{{ originalRange[1] }}</span
      >
    </div>
    <v-range-slider
      v-if="newRange"
      :value="newRange"
      disabled
      :min="newRange[0]"
      :max="newRange[1]"
      hide-details
      class="align-center"
    >
      <template v-slot:prepend>
        <v-text-field
          :value="newRange[0]"
          class="mt-0 pt-0"
          hide-details
          single-line
          type="number"
          style="width: 60px"
          @input="$set(newRange, 0, $event)"
        ></v-text-field>
      </template>
      <template v-slot:append>
        <v-text-field
          :value="newRange[1]"
          class="mt-0 pt-0"
          hide-details
          single-line
          type="number"
          style="width: 60px"
          @input="$set(newRange, 1, $event)"
        ></v-text-field>
      </template>
    </v-range-slider>
  </v-card>
</template>
