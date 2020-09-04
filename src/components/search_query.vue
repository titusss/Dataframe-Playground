<template>
  <div>
    <loading
      v-if="loading"
      :increment="20"
      style="position: fixed;z-index: 100;top: 0;left: 0;width: 100vw;"
    />
    <b-form @submit="onSubmit" inline>
      <b-card
        bg-variant="light"
        v-for="(form_block_array, index) in query"
        v-bind:key="index"
        class="block-wrapper"
      >
        <div class="form" v-for="form_block in form_block_array" v-bind:key="form_block">
          <div class="form-block" v-for="form in form_block.forms.items" v-bind:key="form.id">
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
        <!-- <b-dropdown
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
        </b-dropdown>-->
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
        <b-popover id="tutorial_popover" :no-fade="true" triggers="" placement="bottom" target="add-query-dropdown" title="2. Build filters">You can add multiple filters to search for all kinds of values, including GO terms, KEGG pathways, and COG categories.</b-popover>
        <template v-slot:button-content>
          <b-icon icon="plus-circle-fill"></b-icon> Add Filter
        </template>
        <b-dropdown-group
          v-for="(filter_template_group, index) in filter_templates.items.templates"
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
        <b-popover id="tutorial_popover" :no-fade="true" triggers="" placement="rightbottom" target="load-query-dropdown" title="3. Load preset filters">Load pre-filled filters to search for pathogenicity islands, sORF, or just faulty data.</b-popover>
        <template v-slot:button-content>
          <b-icon icon="intersect"></b-icon> Load Filter
        </template>
        <b-dropdown-group
          v-for="(filter_preset_group, index) in filter_templates.items.presets"
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
          <b-icon icon="search"></b-icon> Filter Data
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
import filter_templates from "../assets/json/filter_templates.json";
export default {
  name: "search_query",
  props: {
    df_categories: Array,
    server_queries: Array,
    backend_url: String,
  },
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
    convert_server_query_blocks(templates) {
      for (let i in this.server_queries) {
        let block_name = this.server_queries[i].name;
        template_type: for (let type in templates) {
          for (let query_group in templates[type]) {
            if (block_name in templates[type][query_group] === true) {
              let block = this.deep_copy(
                templates[type][query_group][block_name]
              );
              for (let form in this.server_queries[i].forms) {
                block.items[form].selected = this.server_queries[i].forms[form];
                if (
                  this.server_queries[i].forms.filter_annotation &&
                  block.items[form].source
                ) {
                  // Convert annotation id's to annotation name
                  let selected_parent = block.items[form].source.items.find(
                    item => item.id === block.items[form].selected
                  );
                  block.items[form].selected = selected_parent.name;
                }
              }
              this.add_query_block(block, block_name);
              break template_type;
            }
          }
        }
      }
    },
    add_query_block(block, index) {
      let added_block = {};
      added_block["forms"] = this.deep_copy(block);
      added_block["id"] = this.id;
      added_block["logic"] = true;
      added_block["block_name"] = index;
      this.query.push([added_block]);
      this.id++;
      // console.log(this.query);
    },
    restructure_query() {
      let structured_query = [];
      for (let array in this.query) {
        for (let sub_array in this.query[array]) {
          let structured_query_block = {};
          // console.log(this.query[array][sub_array]);
          structured_query_block["name"] = this.query[array][sub_array][
            "block_name"
          ];
          structured_query_block["properties"] = this.query[array][sub_array][
            "forms"
          ]["properties"];
          structured_query_block["forms"] = {};
          for (let form in this.query[array][sub_array]["forms"]["items"]) {
            structured_query_block["forms"][form] = this.query[array][
              sub_array
            ]["forms"]["items"][form]["selected"];
          }
          structured_query.push(structured_query_block);
        }
      }
      return structured_query;
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
      const path = `${this.backend_url}/query`;
      var data = new FormData();
      var structured_query = this.restructure_query();
      // console.log(structured_query);
      data.append("query", JSON.stringify(structured_query));
      data.append("url", JSON.stringify(this.$route.query.config));
      // console.log(this.query);
      // console.log(data);
      let self = this;
      // self.$parent.$bvModal.hide('bv_modal_addData')
      axios
        .post(path, data)
        .then(res => {
          if (res.data.error_type) {
            self.$emit("error_occured", res.data);
          } else {
            self.$emit("dataframe_filtered", res);
            this.$nextTick(() => {
              setTimeout(() => { // This forces the loading bar to stay alive for 2 additional seconds, to compensate the delay between backend work and frontend rendering of the dataframe table. This isn't very good.
                this.loading = false;
              }, 2000);
            });
          }
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
      this.filter_templates.items.templates["Filter by annotation"][
        "COG Category"
      ].items.filter_annotation.source.items = this.salmonella_cog_categories.items;
      this.filter_templates.items.templates["Filter by annotation"][
        "GO Term"
      ].items.filter_annotation.source.items = this.salmonella_go_terms.items;
      this.filter_templates.items.templates["Filter by annotation"][
        "GO Namespace"
      ].items.filter_annotation.source.items = this.salmonella_go_terms.items;
      this.filter_templates.items.templates["Filter by annotation"][
        "KEGG Pathway"
      ].items.filter_annotation.source.items = this.salmonella_kegg_terms.items;
    },
    load_categories_json(query_source, categories) {
      categories.unshift("any column", "all columns");
      for (let query_cat in query_source) {
        for (let query in query_source[query_cat]) {
          // Performance: It might be useful to check for a common condition and then do another nested
          // if else, instead of checking every entry for two diffferent conditions.
          if (typeof query_source[query_cat][query].items["filter_area"] !== "undefined") {
            query_source[query_cat][query].items["filter_area"]["options"] = categories;
          }
          else if (typeof query_source[query_cat][query].items["target_column"] !== "undefined") {
            query_source[query_cat][query].items["target_column"]["options"] = this.df_categories;
          }
        }
      }
    }
  },
  created() {
    this.load_categories_json(this.filter_templates.items.templates, this.df_categories.slice(0)); // The slice is needed to preserve the old df_categories
    this.load_categories_json(this.filter_templates.items.presets, this.df_categories.slice(0));
    this.load_autocomplete_json();
    this.convert_server_query_blocks(this.filter_templates.items);
  },
  data() {
    return {
      loading: false,
      id: 0,
      salmonella_go_terms,
      salmonella_kegg_terms,
      salmonella_cog_categories,
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