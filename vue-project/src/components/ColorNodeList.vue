<script lang="ts">
export default {
  props: {
    nodes: {
      type: Array,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  methods: {},
  computed: {
    nodeList() {
      return this.nodes.map((node, index) => {
        const rgb = node.slice(1).map((value) => value * 255);
        return {
          id: index,
          value: node[0],
          rgb: `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`,
        };
      });
    },
    headers() {
      return [
        { text: "ID", value: "id", sortable: false, align: "start" },
        { text: "value", value: "value", align: "center" },
        { text: "swatch", value: "rgb", sortable: false, align: "end" },
      ];
    },
  },
  mounted() {
    console.log(this.nodeList);
  },
};
</script>

<template>
  <div>
    <v-data-table
      :items="nodeList"
      :headers="headers"
      :dark="dark"
      sort-by="value"
      must-sort
      fixed-headers
      hide-default-footer
      show-select
    >
      <!-- eslint-disable-next-line -->
      <template #item.rgb="{ item }">
        <div
          :class="dark ? `color-square dark` : `color-square`"
          :style="`background-color: ` + item.rgb"
        />
      </template>
    </v-data-table>
  </div>
</template>

<style scoped>
.color-square {
  margin-top: 10px;
  height: 25px;
  width: 25px;
  border: 3px solid black;
  float: right;
}
.color-square.dark {
  border: 3px solid white;
}
</style>
