<!-- Generates a single Matrix.
To-Do: Replace this with a method that generates a single SVG (D3.js) for better performance -->

<template>
<div>
  <div class="table_preview">
    <svg v-for="matrix in matrices" :key="matrix.id" @click="selected = matrix.id, select_matrix(matrix)" :class="{hot:selected==matrix.id, active:selected==matrix.id}" :style="{'grid-area': `${matrix.y} / ${matrix.x} / auto / auto`, 'height': `${(matrix.height * gap)-(gap-rect_height)}px`, 'width': `${(matrix.width * gap)-(gap-rect_width)}px`}" v-b-tooltip :title=matrix.title trigger="click">
      <g v-for="column in matrix.height" :key="column" class="rows" :style="{transform: `translate(0px, ${column * gap - gap}px)`}" v-bind:class="{ active: matrix.isActive }">
        <rect v-for="row in matrix.width" :key="row" class="cells" :style="{transform: `translate(${row * gap - gap}px, 0px)`, width: rect_width, height: rect_height}"></rect>
      </g>
    </svg>
    </div>
    <div class="table_buttons">
      <b-button-group>
        <b-button v-b-popover.hover.bottom="'Merge uploaded data with selected table for differential expression.'" title="Differential Expression" :pressed.sync="myToggle" :disabled="button_enabled == 0" size="sm" variant="secondary"><img src="../assets/differential.svg" class="img_in_btn">Differential</b-button>
        <b-button v-b-modal.modal_delete :disabled="button_enabled == 0" size="sm" variant="danger"><img src="../assets/trash.svg" class="img_in_btn">Remove</b-button>
          <!-- <b-modal id="modal_delete" title="Confirm Deletion">
            <p class="my-4">Do you really want to remove the selected table?</p>
          </b-modal> -->
      </b-button-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "matrix",
  props: {
    gap: Number,
    rect_width: Number,
    rect_height: Number
  },
  data() {
    return {
      matrices: [],
      active_matrices: [],
      is_hot: false,
      selected: undefined,
      button_enabled: false,
      myToggle: false,
    }
  },
  created() {
    this.fetch_matrices();
  },
  methods: {
    fetch_matrices() {
      const url = './matrices.json';
        fetch(url)
        .then(data=>{return data.json()})
        .then(res=>{
          this.matrices = res
          this.get_active_matrices(this.matrices);
        })
    },
    select_matrix(matrix) {
      if (Object.prototype.hasOwnProperty.call(matrix, 'title')) {
        this.button_enabled = true;
      }
      else {
        this.button_enabled = false;
      }
      console.log(this.button_enabled);
    },
    get_active_matrices(matrices) {
      // Unneeded currently, remove in production
      var i = 0;
      for(i=0;i<matrices.length;i++) {
        if (Object.prototype.hasOwnProperty.call(this.matrices[i], 'title')) {
          this.active_matrices.push(this.matrices[i]);
        }
      }
      console.log(this.active_matrices);
    }
  }
};
</script>

<style>

:root {
  --cell-width: 16px;
  --cell-height: 16px;
  --cell-color: #E0E0E0;
}
rect {
  fill: var(--cell-color);
}

.rows {
  display: flex;
}

.active, svg:hover {
  --cell-color: #484848 !important;
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

@keyframes pulse {
  0% {opacity: 100%;}
  50% {opacity: 15%;}
  100% {opacity: 100%;}
}

</style>