<script lang="ts">
export default {
  props: {
    nodes: {
      type: Array,
      required: true,
    },
    getFullRange: {
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
      selectedNodes: [],
      visibleColorPicker: undefined,
      colorPickerWidth: 300,
      colorPickerValue: {
        r: 255,
        g: 0,
        b: 0,
      },
      fullRange: undefined,
      tableRange: undefined,
      filteredNodeList: undefined,
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
    toggleSelectNode(item, single = false) {
      this.visibleColorPicker = undefined;
      if (this.selectedNodes.map((node) => node.id).includes(item.id)) {
        this.selectedNodes = this.selectedNodes.filter(
          (node) => node.id != item.id
        );
      } else {
        if (single) this.selectedNodes = [item];
        else this.selectedNodes.push(item);
      }
      console.log(this.selectedNodes);
    },
    toggleSelectAll() {
      if (this.selectedNodes.length == this.filteredNodeList.length) {
        this.selectedNodes = [];
      } else {
        this.selectedNodes = this.filteredNodeList;
      }
    },
    toggleColorPicker(item) {
      if (this.visibleColorPicker !== item.id) {
        this.visibleColorPicker = item.id;
        this.colorPickerValue = this.nodeIndexToColorPickerValue(
          this.nodes[this.visibleColorPicker]
        );
        this.$nextTick(() => {
          if (this.$refs.colorPicker) {
            this.colorPickerWidth = this.$refs.colorPicker.$el.clientWidth;
          }
        });
      } else {
        this.visibleColorPicker = undefined;
        this.colorPickerValue = { r: 255, g: 0, b: 0 };
      }
    },
    changeNodeValue(index, newValue) {
      const newList = [...this.nodes];
      newList[index][0] = parseInt(newValue);
      this.$emit("change", newList);
    },
    removeSelectedNodes() {
      const newList = [...this.nodes];
      this.selectedNodes.forEach((node) => {
        newList.splice(node.id, 1);
      });
      this.$emit("change", newList);
      this.selectedNodes = [];
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
          width: "50px",
        },
        { text: "value", value: "value", align: "start" },
      ];
    },
  },
  watch: {
    tableRange() {
      const shownRange = this.tableRange.map((v) => parseInt(v));
      this.filteredNodeList = this.nodeList.filter(
        (node) => node.value >= shownRange[0] && node.value <= shownRange[1]
      );
    },
    nodes() {
      const shownRange = this.tableRange.map((v) => parseInt(v));
      this.filteredNodeList = this.nodeList.filter(
        (node) => node.value >= shownRange[0] && node.value <= shownRange[1]
      );
    },
  },
  mounted() {
    this.fullRange = this.getFullRange();
    this.tableRange = this.fullRange;
  },
};
</script>

<template>
  <v-data-table
    v-model="selectedNodes"
    ref="table"
    :items="filteredNodeList || nodeList"
    :headers="headers"
    :dark="dark"
    sort-by="value"
    must-sort
    fixed-header
    hide-default-footer
    height="200px"
    dense
  >
    <template #top>
      <div
        :dark="dark"
        class="px-3 py-1 d-flex"
        style="justify-content: space-between; align-items: center"
      >
        <div class="text-caption">
          {{ nodeList.length }} Control Points
          <i>
            ({{ filteredNodeList.length }} shown,
            {{ selectedNodes.length }} selected)
          </i>
        </div>
        <div
          v-if="tableRange"
          class="ml-3 d-flex"
          style="column-gap: 5px; align-items: center"
        >
          Show
          <v-text-field
            :value="tableRange[0]"
            class="mt-0 pt-0"
            hide-details
            single-line
            type="number"
            style="width: 60px"
            :min="fullRange[0]"
            :max="tableRange[1]"
            @change="$set(tableRange, 0, $event)"
          ></v-text-field>
          ...
          <v-text-field
            :value="tableRange[1]"
            class="mt-0 pt-0"
            hide-details
            single-line
            type="number"
            style="width: 60px"
            :min="tableRange[0]"
            :max="fullRange[1]"
            @change="$set(tableRange, 1, $event)"
          ></v-text-field>
        </div>
      </div>
    </template>
    <template #item="{ item }">
      <tr
        :class="
          (selectedNodes.map((node) => node.id).includes(item.id)
            ? 'selected'
            : '') + (dark ? ' dark' : '')
        "
        @click="() => toggleSelectNode(item)"
      >
        <td style="width: 50px">
          <div
            :id="'color-square-' + item.id"
            :class="dark ? `color-square dark` : `color-square`"
            :style="`background-color: ` + item.rgb"
            @click="
              (e) => {
                e.stopPropagation();
                toggleColorPicker(item);
              }
            "
          ></div>
          <v-card
            ref="colorPicker"
            class="color-editor-pane"
            v-if="visibleColorPicker == item.id"
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
        </td>
        <td>
          <v-text-field
            :value="item.value"
            class="value-input"
            hide-details
            single-line
            type="number"
            @change="(newValue) => changeNodeValue(item.id, newValue)"
          />
        </td>
      </tr>
    </template>
    <template #footer>
      <div
        class="d-flex mt-2"
        style="justify-content: space-between; flex-wrap: wrap"
      >
        <v-btn small @click="toggleSelectAll">
          {{
            selectedNodes.length != filteredNodeList.length
              ? "Select"
              : "Deselect"
          }}
          all shown
        </v-btn>
        <v-btn small :disabled="selectedNodes.length > 0" @click="addNode">
          + Add control point
        </v-btn>
        <!-- <v-btn small :disabled="selectedNodes.length < 2"> Adjust range </v-btn> -->
        <v-btn
          small
          :disabled="selectedNodes.length == 0"
          @click="removeSelectedNodes"
        >
          Delete selected
          {{ selectedNodes.length > 0 ? "(" + selectedNodes.length + ")" : "" }}
        </v-btn>
      </div>
      <v-card :dark="dark" v-if="selectedNodes.length > 1" class="mt-3 pa-3">
        Adjust range for selected nodes
      </v-card>
    </template>
  </v-data-table>
</template>

<style>
tr.selected {
  background-color: rgba(0, 0, 0, 0.2);
}
tr.selected.dark {
  background-color: rgba(255, 255, 255, 0.2);
}
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
