<template>
  <div>
    <loading v-if="loading" style="position: absolute;z-index: 100;top: 0;left: 0;width: 100vw;" />
    <b-form @submit="onSubmit" inline>
      <b-card
        bg-variant="light"
        v-for="(form_block_array, index) in query"
        v-bind:key="index"
        class="block-wrapper"
      >
        <div class="form" v-for="form_block in form_block_array" v-bind:key="form_block">
          <div class="form-block" v-for="form in form_block.forms" v-bind:key="form.id">
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
              :style="form.style"
              required
            ></b-form-input>
            <input_autocomplete
              v-if="form.type === 'input-autocomplete'"
              :id="form.id"
              v-model="form.selected"
              v-bind:term_id="form.selected"
              v-on:update:term_id="form.selected = $event"
              v-bind:terms_list="form.source.items"
              v-bind:terms_key="form.source.key"
              class="mb-2 mr-sm-2 mb-sm-0"
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
          <b-dropdown-item
            v-on:click="add_inline_query_block('change_values', form_block_array)"
          >Change values...</b-dropdown-item>
          <b-dropdown-item
            v-on:click="add_inline_query_block('values_in_column', form_block_array)"
          >Values in column...</b-dropdown-item>
          <b-dropdown-item
            v-on:click="add_inline_query_block('values_in_row', form_block_array)"
          >Values in row...</b-dropdown-item>
        </b-dropdown>
        <b-button size="sm" variant="link" v-on:click="remove_query_block(form_block_array)">
          <b-icon icon="trash"></b-icon>
        </b-button>
      </b-card>

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
          <b-icon icon="plus-circle-fill"></b-icon>Add Query
        </template>
        <b-dropdown-group
          v-for="(filter_template_group, index) in filter_templates.items"
          :key="index"
          :header="index"
          id="dropdown-group-numeric"
        >
          <b-dropdown-item
            v-for="(template, index) in filter_template_group"
            :key="index"
            v-on:click="add_query_block(template, index)"
          >{{index}}</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
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
          <b-icon icon="intersect"></b-icon>Load Filter
        </template>
        <b-dropdown-group
          v-for="(filter_preset_group, index) in filter_presets.items"
          :key="index"
          :header="index"
          id="dropdown-group-numeric"
        >
          <b-dropdown-item
            v-for="(preset, index) in filter_preset_group"
            :key="index"
            v-on:click="add_query_block(preset, index)"
          >{{index}}</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
        </b-dropdown-group>
      </b-dropdown>
      <div class="submit-button-parent">
        <b-button type="submit" variant="primary" pill size="sm" class="submit-button">
          <!-- <b-spinner label="Loading..." class="search-spinner" v-if="loading"></b-spinner> -->
          <b-icon icon="search"></b-icon>Filter Data
        </b-button>
      </div>
    </b-form>
  </div>
</template>

<script>
import axios from "axios";
import input_autocomplete from "./input_autocomplete";
import loading from "./loading";
import salmonella_go_terms from "../assets/salmonella/filter_values/salmonella_go_terms_name_namespace.json";
import salmonella_kegg_terms from "../assets/salmonella/filter_values/salmonella_kegg_terms.json";
import salmonella_cog_categories from "../assets/salmonella/filter_values/salmonella_cog_categories.json";
import filter_presets from "../assets/salmonella/salmonella_filter_presets.json";
import filter_templates from "../assets/json/filter_templates.json";
export default {
  name: "search_query",
  components: {
    input_autocomplete,
    loading
  },
  methods: {
    deep_copy(input) {
      let output, value, key;
      if (typeof input !== "object" || input === null) {
        return input;
      }
      output = Array.isArray(input) ? [] : {};
      for (key in input) {
        value = input[key];
        output[key] = this.deep_copy(value);
      }
      return output;
    },
    add_query_block(block, index) {
      let added_block = {};
      added_block["forms"] = this.deep_copy(block);
      added_block["id"] = this.id;
      added_block["logic"] = true;
      added_block["block_name"] = index;
      this.query.push([added_block]);
      this.id++;
    },
    restructure_query() {
      let structured_query = []
      for (let array in this.query) {
        for (let sub_array in this.query[array]) {
          let structured_query_block = {}
          structured_query_block["name"] = this.query[array][sub_array]["block_name"]
          structured_query_block["forms"] = {}
          for (let form in this.query[array][sub_array]["forms"]) {
            structured_query_block["forms"][form] = this.query[array][sub_array]["forms"][form]["selected"]
          }
          structured_query.push(structured_query_block)
        }
      }
      return structured_query
    },
    // add_inline_query_block(block, form) {
    //   let added_block = this.form_blocks[block];
    //   if (block === "or" || block === "and") {
    //     added_block["logic"] = false;
    //   } else {
    //     added_block["logic"] = true;
    //   }
    //   this.query[this.query.indexOf(form)].push(added_block);
    //   this.id++;
    // },
    remove_query_block(block_array) {
      const index = this.query.indexOf(block_array);
      if (index > -1) {
        this.query.splice(index, 1);
      }
    },
    post_query() {
      const path = "http://0.0.0.0:5000/query";
      var data = new FormData();
      var structured_query = this.restructure_query();
      console.log(structured_query)
      data.append("query", JSON.stringify(structured_query));
      data.append("url", JSON.stringify(this.$route.query.config));
      console.log(this.query)
      console.log(data)
      let self = this;
      // self.$parent.$bvModal.hide('bv_modal_addData')
      axios
        .post(path, data)
        .then(res => {
          this.$nextTick(() => {
            self.$emit("dataframe_filtered", res);
            this.loading = false;
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    onSubmit(evt) {
      this.loading = true;
      evt.preventDefault();
      this.post_query();
    },
    load_autocomplete_json() {
      this.filter_templates.items["Filter by annotation"][
        "COG Category"
      ].filter_annotation.source.items = this.salmonella_cog_categories.items;
      this.filter_templates.items["Filter by annotation"][
        "GO Term"
      ].filter_annotation.source.items = this.salmonella_go_terms.items;
      this.filter_templates.items["Filter by annotation"][
        "GO Namespace"
      ].filter_annotation.source.items = this.salmonella_go_terms.items;
      this.filter_templates.items["Filter by annotation"][
        "KEGG Pathway"
      ].filter_annotation.source.items = this.salmonella_kegg_terms.items;
    }
  },
  created() {
    this.load_autocomplete_json();
  },
  data() {
    return {
      loading: false,
      id: 0,
      salmonella_go_terms,
      salmonella_kegg_terms,
      salmonella_cog_categories,
      filter_presets,
      filter_templates,
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
/* .search-spinner {
  width: 1em;
  height: 1em;
}
.spinner-border {
  border: 0.15em solid currentColor;
  border-right-color: transparent;
} */
</style>