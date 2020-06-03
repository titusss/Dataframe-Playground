<template>
  <div class="query_operators">
    <b-form-select v-model="object" :options="options_object" size="sm" class="mt-3"></b-form-select>
    <p>is</p>
    <b-form-select v-model="compare" :options="options_compare" size="sm" class="mt-3"></b-form-select>
    <b-form-textarea v-model="number" placeholder="31020239" rows="1" max-rows="1"></b-form-textarea>
    <b-form-select v-model="operator" :options="options_operator" size="sm" class="mt-3"></b-form-select>
    <p>is</p>
    <b-form-select v-model="compare_not" :options="options_compare" size="sm" class="mt-3"></b-form-select>
    <b-form-textarea v-model="text" placeholder="'145', 'NaN', 'true'" rows="1" max-rows="1"></b-form-textarea>
    <p class="h4 mb-4"><b-icon icon="plus-circle-fill"></b-icon></p>
    <!-- <div class="mt-3">Selected: <strong>{{ selected }}</strong></div> -->
  </div>
</template>

<script>
  export default {
    data() {
      return {
        object: 'current',
        options_object: [
          { value: 'current', text: 'Cell value' },
          { value: 'a', text: 'This is First option' },
          { value: 'b', text: 'Selected Option' },
          { value: { C: '3PO' }, text: 'This is an' },
          { value: 'd', text: 'This one is disabled', disabled: true }
        ],
        compare: 'current',
        options_compare: [
          { value: 'current', text: 'less than' },
          { value: 'a', text: 'equal to' },
          { value: 'b', text: 'more than' },
          { value: 'c', text: 'not' }
        ],
        operator: 'current',
        options_operator: [
          { value: 'current', text: 'and' },
          { value: 'a', text: 'or' }
        ]
      }
    }
  }
</script>

<style scoped>
.query_operators>* {
    display: inline-block;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    vertical-align: middle;
    margin-right: 1rem;
}
.custom-select, .form-control {
    width: auto;
    height: calc(1.5em + 0.5rem + 2px);
}
</style>