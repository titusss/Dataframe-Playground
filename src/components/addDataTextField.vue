<template>
  <div>
    <b-form-textarea
      id="textarea"
      v-model="text"
      placeholder="Paste comma-seperated values..."
      rows="9"
      max-rows="600"
    ></b-form-textarea>

    <pre class="mt-3 mb-0">{{ text }}</pre>
  </div>
</template>

<script>
  export default {
    name: 'addDataTextField',
    data() {
      return {
        text: ''
      }
    }
  }
</script>

<style scoped>
#textarea {
    border: none;
    background-color: #F2F2F2;
}
</style>