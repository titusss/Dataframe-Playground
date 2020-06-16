<template>
  <div>
    <b-form-select
      id="or"
      size="sm"
      class="mb-2 mr-sm-2 mb-sm-0"
      :options="[{text: 'or'}, 'and']"
      :value="null"
    ></b-form-select>
  </div>
</template>
    
<style scoped>
label {
    display: inline-flex !important;
    margin-right: 0.5rem;
    font-size: 0.875rem;
}
</style>