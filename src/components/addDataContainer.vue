<template>
    <b-container class="bv-example-row">
      <b-row>
        <b-col>
          <h2>Add Data</h2>
          <addDataForm/>
        </b-col>
        <b-col class="center">
          <h2>Matrix Preview</h2>
          <matrix v-bind:rect_width="15" v-bind:rect_height="15" v-bind:gap="20"/>
        </b-col>
      </b-row>
    </b-container>
</template>

<script>
import addDataForm from './addDataForm.vue'
import matrix from './matrix.vue'

export default {
  name: 'addDataContainer',
  components: {
    addDataForm,
    matrix
  }
}
</script>