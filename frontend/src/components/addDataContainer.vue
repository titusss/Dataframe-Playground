<template>
  <b-container class="bv-example-row">
    <b-row>
      <b-col>
        <h2>Add Data</h2>
        <addDataForm />
        <pre class="mt-3 mb-0">{{ text }}</pre>
        <b-button type="submit" variant="primary">Add</b-button>
        <b-button type="reset" variant="danger" @click="$bvModal.hide('bv_modal_addData')">Cancel</b-button>
      </b-col>
      <b-col class="center">
        <h2>Matrix Preview</h2>
        <matrix v-bind:rect_width="15" v-bind:rect_height="15" v-bind:gap="20" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import addDataForm from "./addDataForm.vue";
import matrix from "./matrix.vue";

export default {
  name: "addDataContainer",
  components: {
    addDataForm,
    matrix
  }
};
</script>