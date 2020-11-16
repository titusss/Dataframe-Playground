<template>
  <div>
    <vue-typeahead-bootstrap
      v-model="query"
      :showOnFocus="true"
      v-bind:class="{invalid: invalid, valid: !invalid}"
      class="input-autocomplete"
      id="input-autocomplete-target"
      :data="terms_list"
      :serializer="term => term[terms_key]"
      @hit="term_name_selected($event)"
      :state="false"
      size="sm"
    />
    <!-- <b-form-input id="input-invalid" :state="false" placeholder="Invalid input"></b-form-input> -->
  </div>
</template>

<script>
export default {
  props: {
    server_term: Object,
    term_id: String,
    terms_list: Array,
    terms_key: String
  },
  created() {
    if(this.server_term) {  
      this.term_name_selected(this.server_term)
      this.query = this.server_term.name
    }
  },
  data() {
    return {
      invalid: true,
      query: "",
      last_valid: ""
    };
  },
  methods: {
    term_name_selected(event) {
      this.last_valid = event.name;
      this.invalid = false;
      this.$emit("update:term_id", event.id);
    }
  },
  watch: {
    query: function(val, oldVal) {
      if (val != this.last_valid) {
        this.invalid = true;
        console.log(oldVal);
      }
    }
  }
};
</script>

<style>
.input-autocomplete {
  width: 40vw;
  max-width: 500px;
}
.invalid > .input-group > .form-control {
  border-color: #dc3545;
  padding-right: calc(1.5em + 0.75rem);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%23dc3545' viewBox='0 0 12 12'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
}
.invalid > .input-group > .form-control:focus {
  -webkit-box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}
.valid > .input-group > .form-control {
  border-color: #28a745 !important;
  padding-right: calc(1.5em + 0.75rem);
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath fill='%2328a745' d='M2.3 6.73L.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z'/%3e%3c/svg%3e");
}
.valid > .input-group > .form-control:focus {
  -webkit-box-shadow: rgba(40, 167, 69, 0.25) 0px 0px 0px 3.2px;
  box-shadow: rgba(40, 167, 69, 0.25) 0px 0px 0px 3.2px;
}
</style>