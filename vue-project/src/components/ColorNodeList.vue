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
  methods: {
    changeNodeValue(index, newValue) {
      const newList = [...this.nodes];
      newList[index][0] = parseInt(newValue);
      this.$emit("change", newList);
    },
    removeNode(index) {
      const newList = [...this.nodes];
      newList.splice(index, 1);
      this.$emit("change", newList);
    },
  },
  computed: {
    nodeList() {
      return this.nodes.map((node, index) => {
        const rgb = node.slice(1).map((value) => value * 255);
        return {
          id: index,
          value: node[0],
          rgb: `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`,
          index,
        };
      });
    },
    headers() {
      return [
        { text: "ID", value: "id", sortable: false, align: "start" },
        { text: "value", value: "value", align: "center" },
        { text: "swatch", value: "rgb", sortable: false, align: "end" },
        { text: "remove", value: "index", sortable: false, width: "50px" },
      ];
    },
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
      <template #item.value="{ item }">
        <v-text-field
          :value="item.value"
          class="value-input"
          hide-details
          single-line
          type="number"
          @change="(newValue) => changeNodeValue(item.id, newValue)"
        ></v-text-field>
      </template>
      <!-- eslint-disable-next-line -->
      <template #item.rgb="{ item }">
        <div
          :class="dark ? `color-square dark` : `color-square`"
          :style="`background-color: ` + item.rgb"
        />
      </template>
      <!-- eslint-disable-next-line -->
      <template #item.index="{ item }">
        <v-icon @click="() => removeNode(item.index)"> mdi-trash-can </v-icon>
      </template>
    </v-data-table>
  </div>
</template>

<style scoped>
.value-input {
  width: 70px;
  padding: 0;
  margin: 0;
  margin-left: calc(50% - 35px);
}
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
