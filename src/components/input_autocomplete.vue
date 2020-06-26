<template>
<div>
    <vue-bootstrap-typeahead 
  v-model="query"
  :data="this.annotations"
/>
  </div>
</template>

<script>
import annotations_json from '../assets/ecoli_go_annotations.json'
export default {
  data() {
    return {
      annotations: []
    };
  },
  created() {
      this.annotations = annotations_json
  },
}
</script>