<template>
  <div>
    <b-form @submit="onSubmit" inline>
      <b-card
        bg-variant="light"
        v-for="form_block in query"
        v-bind:key="form_block"
        class="block-wrapper"
      >
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
        </div>
        <b-button size="sm" variant="link" v-on:click="remove_query_block(form_block.id)">
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
        id="add-dropdown"
        text="Add..."
        class="m-md-2 rounded"
        no-caret
        toggle-class="text-decoration-none"
      >
        <template v-slot:button-content>
          <b-icon icon="plus-circle"></b-icon> Add
        </template>
        <b-dropdown-item v-on:click="add_query_block('all_values')">All values...</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('values_in_column')">Values in column...</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('values_in_row')">Values in row...</b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item v-on:click="add_query_block('and')">and</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('or')">or</b-dropdown-item>
      </b-dropdown>
      <div class="submit-button-parent">
      <b-button
        type="submit"
        variant="primary"
        pill
        size="sm"
        class="submit-button"
      >
        <b-icon icon="search"></b-icon> Filter Data
      </b-button>
      </div>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "search_query",
  methods: {
    add_query_block(block) {
      let added_block = this.form_blocks[block];
      added_block["id"] = this.id;
      this.query.push(added_block);
      console.log(this.query);
      this.id++;
    },
    remove_query_block(block_id) {
      this.query.splice(
        this.query.findIndex(item => item.id === block_id),
        1
      );
    },
    post_query() {
      const path = "http://0.0.0.0:5000/query";
      var data = new FormData();
      data.append("query", JSON.stringify(this.query));
      let self = this;
      // self.$parent.$bvModal.hide('bv_modal_addData')
      axios
        .post(path, data)
        .then(res => {
          this.$nextTick(() => {
            console.log("after next tick res: ", res);
            console.log(JSON.stringify(res));
            self.$emit("dataframe_change", res);
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
      id: 0,
      query_form_data: {},
      test: true,
      form_blocks: {
        all_values: {
          logical_operator: {
            label: "Values are",
            type: "b-form-select",
            options: [
              "< less than",
              ">= more or equal to",
              "<= less or equal to",
              "= equal to",
              "!= not"
            ],
            id: "all_values_logical-operator",
            selected: null
          },
          value: {
            type: "b-form-input",
            id: "all_values_value",
            selected: null
          }
        },
        and: {
          and_form: {
            options: [{ text: "and" }, "or"],
            type: "b-form-select",
            id: "and",
            selected: null
          }
        },
        or: {
          or_form: {
            options: [{ text: "or" }, "and"],
            type: "b-form-select",
            id: "or",
            selected: null
          }
        },
        values_in_column: {
          column: {
            label: "Values in column",
            type: "b-form-select",
            options: [
              { text: "SP Tex (Biological replicate 1)" },
              "One",
              "Two",
              "Three"
            ],
            id: "values_in_column_column",
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
            id: "values_in_column_logical-operator",
            selected: null
          },
          value: {
            type: "b-form-input",
            id: "values_in_column_value",
            selected: null
          }
        },
        values_in_row: {
          row: {
            label: "Values in row",
            type: "b-form-select",
            options: [
              { text: "SP Tex (Biological replicate 1)" },
              "One",
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
</style>