<template>
  <div>
    <label for="form-dataframe">Values in dataframe</label>
    <b-form-select
      id="form-dataframe"
      size="sm"
      class="mb-2 mr-sm-2 mb-sm-0"
      :options="[{ text: 'SP Tex (Biological replicate 1)'}, 'One', 'Two', 'Three']"
      :value="null"
      no-caret
    ></b-form-select>
    <label for="logical-operator">are</label>
    <b-form-select
      id="logical-operator"
      size="sm"
      class="mb-2 mr-sm-2 mb-sm-0"
      :options="[{ text: 'more than'}, 'less than', 'more or equal to', 'less or equal to', 'equal to', 'not']"
      :value="null"
      no-caret
    ></b-form-select>
    <b-form-input v-model="text" size="sm"></b-form-input>
  </div>
</template>
    
<style scoped>
label {
    display: inline-flex !important;
    margin-right: 0.5rem;
    font-size: 0.875rem;
}
</style>