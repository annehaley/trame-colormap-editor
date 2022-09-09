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
  data() {
    return {
      selectedNodes: [],
      visibleColorPicker: undefined,
      colorPickerWidth: 300,
      colorPickerValue: {
        r: 255,
        g: 0,
        b: 0,
      },
    };
  },
  methods: {
    nodeToTableItem(node, index) {
      const rgb = node.slice(1).map((value) => value * 255);
      return {
        id: index,
        value: node[0],
        rgb: `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`,
        index,
      };
    },
    nodeIndexToColorPickerValue(node) {
      const rgb = node.slice(1).map((value) => value * 255);
      // TODO: change based on interpolation mode
      return {
        r: rgb[0],
        g: rgb[1],
        b: rgb[2],
      };
    },
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
    addNode() {
      const newNode = [0, 0, 0, 0];
      const newList = [...this.nodes];
      newList.push(newNode);
      this.selectedNodes = [this.nodeToTableItem(newNode, newList.length - 1)];
      this.$emit("change", newList);
    },
    updateColorOfSelectedNode(newValue) {
      this.colorPickerValue = newValue;
      const newList = [...this.nodes];
      const newRGB = Object.values(newValue).map(
        (ratio: number) => ratio / 255
      );
      newList[this.selectedNodes[0].index] = [
        this.selectedNodes[0].value,
        ...newRGB,
      ];
      this.$emit("change", newList);
    },
  },
  computed: {
    nodeList() {
      return this.nodes.map(this.nodeToTableItem);
    },
    headers() {
      return [
        {
          text: "swatch",
          value: "rgb",
          sortable: false,
          align: "end",
          width: "50px",
        },
        { text: "value", value: "value" },
      ];
    },
  },
  watch: {
    selectedNodes() {
      if (this.selectedNodes.length == 1) {
        this.visibleColorPicker = this.selectedNodes[0].id;
        this.colorPickerValue = this.nodeIndexToColorPickerValue(
          this.nodes[this.visibleColorPicker]
        );
        this.$nextTick(() => {
          if (this.$refs.colorPicker) {
            this.colorPickerWidth = this.$refs.colorPicker.$el.clientWidth;
          }
        });
      } else if (this.selectedNodes.length == 0) {
        this.visibleColorPicker = undefined;
      }
    },
  },
};
</script>

<template>
  <div>
    <div id="range-editor" v-if="selectedNodes.length > 1">
      <v-card class="pa-3 mb-3"> Edit range for multiple nodes </v-card>
    </div>

    <v-data-table
      v-model="selectedNodes"
      ref="table"
      :items="nodeList"
      :headers="headers"
      :dark="dark"
      sort-by="value"
      must-sort
      fixed-header
      hide-default-footer
      height="200px"
      dense
    >
      <!-- eslint-disable-next-line -->
      <template #item.rgb="{ item }">
        <div>
          <div
            :id="'color-square-' + item.id"
            :class="dark ? `color-square dark` : `color-square`"
            :style="`background-color: ` + item.rgb"
            @click="
              () => {
                if (selectedNodes.map((node) => node.id).includes(item.id)) {
                  selectedNodes = [];
                } else {
                  selectedNodes = [item];
                }
              }
            "
          ></div>
          <v-card
            ref="colorPicker"
            class="color-editor-pane"
            v-if="selectedNodes.length == 1 && visibleColorPicker == item.id"
            v-click-outside="() => (selectedNodes = [])"
          >
            <v-lazy>
              <v-color-picker
                :value="colorPickerValue"
                canvas-height="65px"
                :hide-canvas="colorPickerValue === undefined"
                :width="`${colorPickerWidth}`"
                @input="updateColorOfSelectedNode"
              />
            </v-lazy>
          </v-card>
        </div>
      </template>
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
      <template #footer>
        <v-btn small style="width: 100%" @click="addNode">
          + Add control point
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<style>
.value-input {
  width: 70px;
  padding: 0;
  margin: 0;
}
.color-square {
  height: 25px;
  width: 25px;
  border: 3px solid black;
  float: right;
}
.color-square.dark {
  border: 3px solid white;
}
.color-editor-pane {
  position: absolute;
  top: 35px;
  left: 70px;
  width: calc(100% - 75px);
  height: calc(100% - 40px);
  background-color: inherit;
  z-index: 2;
  padding: 5px;
  text-align: center;
}
.v-data-table__wrapper {
  position: relative;
}
.v-color-picker__preview {
  width: 100%;
  margin-right: 20px;
}
.v-color-picker__hue,
.v-color-picker__edit {
  margin: 3px !important;
}
.v-color-picker__controls {
  padding: 5px 10px;
}
.v-btn.v-btn--icon.v-btn--round.v-size--small,
.v-color-picker__dot {
  display: none;
}
</style>
