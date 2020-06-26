<template>
  <div>
    <b-form @submit="onSubmit" inline>
      <b-card
        bg-variant="light"
        v-for="(form_block_array, index) in query"
        v-bind:key="index"
        class="block-wrapper"
      >
        <div class="form" v-for="form_block in form_block_array" v-bind:key="form_block">
          <div class="form-block" v-for="form in form_block" v-bind:key="form.id">
            <label v-if="form.label" :for="form.id">{{form.label}}</label>
            <b-form-select
              v-if="form.type === 'b-form-select'"
              :options="form.options"
              :value="null"
              :id="form.id"
              v-model="form.selected"
              size="sm"
              class="mb-2 mr-sm-2 mb-sm-0"
              required
            ></b-form-select>
            <b-form-input
              v-if="form.type === 'b-form-input'"
              :id="form.id"
              v-model="form.selected"
              size="sm"
              class="mb-2 mr-sm-2 mb-sm-0"
              required
            ></b-form-input>
            <input_autocomplete
              v-if="form.type === 'input-autocomplete'"
              :id="form.id"
              v-model="form.selected"
              size="sm"
              class="mb-2 mr-sm-2 mb-sm-0"
              :suggestions="cities" 
              :selection.sync="complete_value"
              required
            ></input_autocomplete>
          </div>
        </div>
        <b-dropdown
          v-if="form_block_array[form_block_array.length-1]['logic']"
          size="sm"
          variant="link"
          pill
          id="add-dropdown"
          text="Add..."
          class="m-md-2 rounded"
          no-caret
          toggle-class="text-decoration-none"
        >
          <template v-slot:button-content>
            <b-icon icon="plus-circle"></b-icon>
          </template>
          <b-dropdown-item v-on:click="add_inline_query_block('and', form_block_array)">and</b-dropdown-item>
          <b-dropdown-item v-on:click="add_inline_query_block('or', form_block_array)">or</b-dropdown-item>
        </b-dropdown>
        <b-dropdown
          v-if="form_block_array[form_block_array.length-1]['logic'] === false"
          size="sm"
          variant="link"
          pill
          id="add-dropdown"
          text="Add..."
          class="m-md-2 rounded"
          no-caret
          toggle-class="text-decoration-none"
        >
          <template v-slot:button-content>
            <b-icon icon="plus-circle"></b-icon>
          </template>
          <b-dropdown-item v-on:click="add_inline_query_block('change_values', form_block_array)">Change values...</b-dropdown-item>
          <b-dropdown-item v-on:click="add_inline_query_block('values_in_column', form_block_array)">Values in column...</b-dropdown-item>
          <b-dropdown-item v-on:click="add_inline_query_block('values_in_row', form_block_array)">Values in row...</b-dropdown-item>
        </b-dropdown>
        <b-button size="sm" variant="link" v-on:click="remove_query_block(form_block_array)">
          <b-icon icon="trash"></b-icon>
        </b-button>
      </b-card>

      <!-- <div v-for="block in blocks" v-bind:key="block.id" class="block-wrapper">
        <b-card bg-variant="light">
          <component class="component-inline" v-bind:is="block.name" v-bind.sync="form"></component>
        </b-card>
        <b-button size="sm" variant="link" v-on:click="remove_query_block(block.id)">
          <b-icon icon="trash"></b-icon>
        </b-button>
      </div>-->
      <b-dropdown
        size="sm"
        variant="link"
        pill
        id="add-query-dropdown"
        text="Add..."
        class="m-md-2 rounded"
        no-caret
        toggle-class="text-decoration-none"
      >
        <template v-slot:button-content>
          <b-icon icon="plus-circle-fill"></b-icon> Add Query
        </template>
        <b-dropdown-group id="dropdown-group-numeric" header="Numeric operations">
        <b-dropdown-item v-on:click="add_query_block('change_values')">Change values</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('values_in_column')">Remove columns</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('values_in_row')">Remove rows</b-dropdown-item>
        </b-dropdown-group>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-group id="dropdown-group-numeric" header="Genome annotation">
        <b-dropdown-item v-on:click="add_query_block('gene_relevant')">Gene relevant in...</b-dropdown-item>
        </b-dropdown-group>
      </b-dropdown>
      <b-dropdown
        size="sm"
        variant="link"
        pill
        id="load-query-dropdown"
        text="Add..."
        class="m-md-2 rounded"
        no-caret
        toggle-class="text-decoration-none"
      >
        <template v-slot:button-content>
          <b-icon icon="intersect"></b-icon> Load Filter
        </template>
        <b-dropdown-group id="dropdown-group-numeric" header="Genome Annotation">
        <b-dropdown-item v-on:click="add_query_block('change_values')">Filter gastro genes</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('values_in_column')">Filter pathogenic</b-dropdown-item>
        </b-dropdown-group>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-group id="dropdown-group-numeric" header="Data Cleanup">
          <b-dropdown-item v-on:click="add_query_preset('change_values')">Remove faulty data</b-dropdown-item>
          <b-dropdown-item v-on:click="add_query_block('change_values')">Remove strings</b-dropdown-item>
        </b-dropdown-group>
      </b-dropdown>
      <div class="submit-button-parent">
        <b-button type="submit" variant="primary" pill size="sm" class="submit-button">
          <b-icon icon="search"></b-icon> Filter Data
        </b-button>
      </div>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
import input_autocomplete from "./input_autocomplete";
export default {
  name: "search_query",
  components: {
    input_autocomplete
  },
  methods: {
    add_query_preset(preset) {
      let added_preset = this.form_blocks[preset];
      added_preset["id"] = this.id;
      added_preset["logic"] = true;
      added_preset["logical_operator"]["selected"] = "!= not"
      added_preset["value"]["selected"] = "NaN, Null, undefined, 0, null"
      console.log(added_preset);
      this.query.push([added_preset]);
      this.id++;
    },
    add_query_block(block) {
      let added_block = this.form_blocks[block];
      added_block["id"] = this.id;
      added_block["logic"] = true;
      this.query.push([added_block]);
      console.log(this.query);
      this.id++;
    },
    add_inline_query_block(block, form) {
      let added_block = this.form_blocks[block];
      if (block === "or" || block === "and") {
        added_block["logic"] = false;
      } else {
        added_block["logic"] = true;
      }
      console.log(this.query[0]);
      console.log(this.query.indexOf(form));
      this.query[this.query.indexOf(form)].push(added_block);
      console.log(this.query);
      this.id++;
    },
    remove_query_block(block_array) {
      console.log(block_array);
      const index = this.query.indexOf(block_array);
      if (index > -1) {
        this.query.splice(index, 1);
      }
    },
    post_query() {
      const path = "http://0.0.0.0:5000/query";
      var data = new FormData();
      data.append("query", JSON.stringify(this.query));
      data.append("url", JSON.stringify(this.$route.query.config));
      let self = this;
      // self.$parent.$bvModal.hide('bv_modal_addData')
      axios
        .post(path, data)
        .then(res => {
          this.$nextTick(() => {
            console.log("after next tick res: ", res);
            console.log(JSON.stringify(res));
            self.$emit("dataframe_filtered", res);
            this.show_loading_overlay = false;
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.post_query();
    }
  },
  data() {
    return {
      cities : [
            'Bangalore','Chennai','Cochin',
            'Delhi','Kolkata','Mumbai', 'Gastro intake'
        ],
      complete_value: '',
      id: 0,
      query_form_data: {},
      test: true,
      form_blocks: {
        change_values: {
          logical_operator: {
            label: "Change values that are",
            type: "b-form-select",
            options: [
              "< less than",
              "> more than",
              ">= more or equal to",
              "<= less or equal to",
              "= equal to",
              "!= not"
            ],
            id: "change_values_logical-operator",
            selected: null
          },
          current_value: {
            type: "b-form-input",
            id: "change_values_current-value",
            selected: null
          },
          target_value: {
            label: "to",
            type: "b-form-input",
            id: "change_values_target-value",
            selected: null
          }
        },
        and: {
          and: {
            options: [{ text: "and" }, "or"],
            type: "b-form-select",
            id: "and",
            selected: null
          }
        },
        or: {
          or: {
            options: [{ text: "or" }, "and"],
            type: "b-form-select",
            id: "or",
            selected: null
          }
        },
        values_in_column: {
          column: {
            label: "Remove columns",
            type: "b-form-select",
            options: [
              { text: "SP Tex (Biological replicate 1)" },
              "One",
              "Two",
              "Three"
            ],
            id: "values_in_column_column",
            selected: null
          }
        },
        values_in_row: {
          row: {
            label: "Remove rows, where values of column",
            type: "b-form-select",
            options: [
              { text: "SP Tex (Biological replicate 1)" },
              "Any column",
              "Two",
              "Three"
            ],
            id: "values_in_row_row",
            selected: null
          },
          logical_operator: {
            label: "are",
            type: "b-form-select",
            options: [
              "< less than",
              ">= more or equal to",
              "<= less or equal to",
              "= equal to",
              "!= not"
            ],
            id: "values_in_row_logical-operator",
            selected: null
          },
          value: {
            type: "b-form-input",
            id: "values_in_row_value",
            selected: null
          }
        },
        gene_relevant: {
          search: {
            label: "Gene relevant in",
            type: "input-autocomplete",
            id: "gene_relevant_search",
            selected: null
          }
        }
      },
      query: []
    };
  }
};
</script>

<style scoped>
label {
  margin-right: 0.5rem;
  font-size: 0.875rem;
}
svg,
button {
  margin: 0;
  text-decoration: none !important;
}
.block-wrapper {
  width: 100%;
}
#add-dropdown {
  margin: 0 !important;
}
.card-body {
  padding: 0.35rem;
}
.card {
  margin-bottom: 0.5rem;
  display: inline-block;
}
.form-block {
  display: inline-flex;
}
.submit-button-parent {
  flex: 1;
  text-align: right;
}
.form {
  display: inline-flex;
}
</style>