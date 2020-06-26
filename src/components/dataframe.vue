<template>
  <div>
    <b-card>
      <div class="table-options">
        <div class="form-group-item">
          <b-form-group
            label="Filter"
            label-cols-sm="3"
            label-align-sm="right"
            label-size="sm"
            label-for="filterInput"
            class="mb-0"
          >
            <b-input-group size="sm">
              <b-form-input
                v-model="filter"
                type="search"
                id="filterInput"
                placeholder="Type to Search"
              ></b-form-input>
            </b-input-group>
          </b-form-group>
        </div>

        <div class="form-group-item">
          <b-form-group
            label="Per page"
            label-cols-sm="6"
            label-cols-md="4"
            label-cols-lg="3"
            label-align-sm="right"
            label-size="sm"
            label-for="perPageSelect"
            class="mb-0"
          >
            <b-form-select v-model="perPage" id="perPageSelect" size="sm" :options="pageOptions"></b-form-select>
          </b-form-group>
        </div>

        <div class="form-group-item">
          <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            align="fill"
            size="sm"
            class="my-0"
          ></b-pagination>
        </div>
      </div>

      <!-- User Interface controls -->
      <div class="table-wrapper">
        <b-table
          id="dataframe-table"
          ref="selectableTable"
          hover
          small
          selectable
          :select-mode="range"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
          :filterIncludedFields="filterOn"
          :items="dataframe"
          :fields="dataframe_headers"
          head-variant="light"
          @filtered="onFiltered"
        >
          <template v-slot:cell()="data">{{data.value}}</template>
          <template v-slot:cell(GeneID)="data">{{data.value}}</template>
        </b-table>
      </div>
    </b-card>
  </div>
</template>

<script>
export default {
  props: {
    dataframe: Array
  },
  data() {
    return {
      dataframe_headers: [],
      totalRows: 1,
      currentPage: 1,
      perPage: 20,
      pageOptions: [20, 50, 100, 1000],
      filter: null,
      filterOn: []
    };
  },
  methods: {
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  },
  created() {
    for (let header in this.dataframe[0]) {
      console.log(header);
      let entry = {};
      entry["key"] = header;
      entry["sortable"] = true;
      this.dataframe_headers.push(entry);
    }
  },
  mounted() {
    this.totalRows = this.items.length;
  }
};
</script>

<style scoped>
table#dataframe-table .flip-list {
  transition: transform 1s;
}
table {
  font-family: "SF Mono", "Courier New", Courier, monospace;
  font-size: 0.8rem;
}
.card {
  width: 95vw;
  border-radius: 20px;
  background-color: #fff;
}
.table-wrapper {
  overflow: auto;
  border-radius: 8px;
}
.table-options {
  display: grid;
  grid-template-columns: repeat(3, auto);
  grid-column-gap: 30px;
  margin-bottom: 1rem;
}
label {
  display: inline-flex !important;
  flex: none !important;
  width: auto !important;
}
.pagination {
  width: min-content;
}
</style>