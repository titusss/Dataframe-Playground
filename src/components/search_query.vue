<template>
  <div>
    <b-form inline>
      <div v-for="block in blocks" v-bind:key="block.id" class="block-wrapper">
        <b-card bg-variant="light">
          <component class="component-inline" v-bind:is="block.name"></component>
        </b-card>
        <b-button size="sm" variant="link" v-on:click="remove_query_block(block.id)">
          <b-icon icon="trash"></b-icon>
        </b-button>
      </div>

      <b-dropdown
        size="sm"
        variant="link"
        id="add-dropdown"
        text="Add..."
        class="m-md-2 rounded"
        no-caret
        toggle-class="text-decoration-none"
      >
        <template v-slot:button-content>
          <b-icon icon="plus-circle-fill"></b-icon>
          <span class="sr-only">Search</span>
        </template>
        <b-dropdown-item v-on:click="add_query_block('all_values')">All values...</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('values_in_column')">Values in column...</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('values_in_row')">Values in row...</b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item v-on:click="add_query_block('and')">and</b-dropdown-item>
        <b-dropdown-item v-on:click="add_query_block('or')">or</b-dropdown-item>
      </b-dropdown>
    </b-form>
  </div>
</template>

<script>
import values_in_column from "@/components/query_blocks/values_in_column.vue";
import and from "@/components/query_blocks/and.vue";
import or from "@/components/query_blocks/or.vue";
import values_in_row from "@/components/query_blocks/values_in_row.vue";
import values_in_dataframe from "@/components/query_blocks/values_in_dataframe.vue";
import all_values from "@/components/query_blocks/all_values.vue";
export default {
  name: "search_query",
  components: {
    values_in_column,
    and,
    or,
    values_in_row,
    all_values,
    values_in_dataframe
  },
  methods: {
    add_query_block(block) {
      this.blocks.push({ name: block, id: this.id });
      this.id++;
      console.log(this.blocks);
    },
    remove_query_block(block_id) {
      this.blocks.splice(
        this.blocks.findIndex(function(i) {
          return i.id === block_id;
        }), 1);
    }
  },
  data() {
    return {
      blocks: [],
      id: 0
    };
  }
};
</script>

<style scoped>
label {
  margin-right: 0.5rem;
  font-size: 0.875rem;
}
svg {
  margin: 0;
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
</style>