<template>
  <div>
    <div class="table_preview">
      <svg
        v-for="matrix in matrices"
        :key="matrix.id"
        @click="selected = matrix.id, select_matrix(matrix)"
        :class="{hot:selected==matrix.id, active:selected==matrix.id}"
        :style="{'grid-area': `${matrix.y} / ${matrix.x} / auto / auto`, 'height': `${(matrix.height * gap)-(gap-rect_height)}px`, 'width': `${(matrix.width * gap)-(gap-rect_width)}px`}"
        v-b-tooltip
        :title="matrix.title"
        trigger="click"
      >
        <g
          v-for="column in matrix.height"
          :key="column"
          class="rows"
          :style="{transform: `translate(0px, ${column * gap - gap}px)`}"
          v-bind:class="{ active: matrix.isActive }"
        >
          <rect
            v-for="row in matrix.width"
            :key="row"
            class="cells"
            :style="{transform: `translate(${row * gap - gap}px, 0px)`, width: rect_width, height: rect_height}"
          />
        </g>
      </svg>
    </div>
    <div class="table_buttons">
      <b-button-group>
        <b-button
          v-b-toggle.collapse-differential
          v-b-popover.hover.top="'Merges uploaded data with selected table for differential expression when selected.'"
          title="Differential Expression"
          :pressed.sync="is_differential"
          :disabled="button_enabled == 0"
          size="sm"
          variant="secondary"
        >
          <img src="../assets/differential.svg" class="img_in_btn" />Differential
        </b-button>
        <b-button v-b-modal.modal_delete @click="on_delete_matrix(selected)" :disabled="button_enabled == 0" size="sm" variant="danger">
          <img src="../assets/trash.svg" class="img_in_btn" />Remove
        </b-button>
      </b-button-group>

      <b-collapse id="collapse-differential" class="mt-2">
        <b-card>
          <p class="card-text">Select base column for normalization.</p>
          <div class>
            <b-form>
              <b-form-select
                id="input-3"
                v-model="form.normalization_column"
                :options="columns"
                required
              ></b-form-select>
            </b-form>
          </div>
        </b-card>
      </b-collapse>
    </div>
  </div>
</template>

<script>
export default {
  name: "matrix",
  props: {
    gap: Number,
    rect_width: Number,
    rect_height: Number,
    matrices: Array
  },
  data() {
    return {
      is_hot: false,
      selected: undefined,
      button_enabled: false,
      is_differential: false,
      form: {
        normalization_column: null
      },
      columns: [
        { text: "Select One", value: null },
        "Mouse 1",
        "Mouse 2 Cow",
        "Pig",
        "Chicken Macrophage",
        "SPI2",
        "NO",
        "SPI2",
        "H2O2",
        "SPI2",
        "-Mg2",
        "SPI2"
      ]
    };
  },
  methods: {
    select_matrix(matrix) {
      console.log(matrix);
      this.$emit('matrix_activated',matrix);
      if (Object.prototype.hasOwnProperty.call(matrix, "title")) {
        this.button_enabled = true;
      } else {
        this.button_enabled = false;
      }
    },
    on_delete_matrix(deleted_matrix_id) {
      this.$emit('delete', deleted_matrix_id);
    }
  }
};
</script>

<style>
:root {
  --cell-width: 16px;
  --cell-height: 16px;
  --cell-color: #e0e0e0;
}
rect {
  fill: var(--cell-color);
}

.rows {
  display: flex;
}

.active,
svg:hover {
  --cell-color: #484848;
}

.table_preview {
  display: inline-grid;
}

rect {
  transition: fill 200ms ease-out;
}

svg {
  margin: 5px;
  cursor: pointer;
}

.hot {
  animation-name: pulse;
  animation-duration: 1.5s;
  animation-iteration-count: infinite;
}

.btn-secondary:not(:disabled):not(.disabled).active {
  background-color: #007bff !important;
  border-color: #007bff !important;
}

@keyframes pulse {
  0% {
    opacity: 100%;
  }
  50% {
    opacity: 15%;
  }
  100% {
    opacity: 100%;
  }
}
</style>