<template>
  <div>
    <b-card>
      <div class="table-options">
        <b-form-group label="Filter" label-size="sm" label-for="filterInput" class="inline-element">
          <b-form-input
            v-model="filter"
            type="search"
            id="filterInput"
            size="sm"
            placeholder="Type to Search"
            class="inline-element"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Per page"
          label-size="sm"
          label-for="perPageSelect"
          class="inline-element"
        >
          <b-form-select v-model="perPage" id="perPageSelect" size="sm" :options="pageOptions" class="inline-element"></b-form-select>
        </b-form-group>
        <b-form-group class="inline-element">
          <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            align="fill"
            size="sm"
          ></b-pagination>
        </b-form-group>
        <b-form-group class="inline-element" id="toggle-filtered">
          <span class="col-form-label-sm">Show filtered</span>
            <label class="switch switch-label bv-no-focus-ring">
              <input
                type="checkbox"
                v-model="filtered_visible"
                value=false
                unchecked-value=true
              />
              <span class="slider round"></span>
            </label>
            <!-- <div class="filter-toggle-text">Filtered table is visible? {{ filtered_visible }}</div> -->
        </b-form-group>
      </div>
      <!-- User Interface controls -->
      <div class="table-wrapper" v-if="!filtered_visible">
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
      <div class="table-wrapper" v-if="filtered_visible">
        <b-table
          id="dataframe-filtered-table"
          ref="selectableTable"
          hover
          small
          selectable
          :select-mode="range"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
          :filterIncludedFields="filterOn"
          :items="dataframe_filtered"
          :fields="dataframe_filtered_headers"
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
    dataframe: Array,
    dataframe_filtered: Array
  },
  data() {
    return {
      dataframe_headers: [],
      totalRows: 1,
      currentPage: 1,
      perPage: 20,
      pageOptions: [20, 50, 100, 1000],
      filter: null,
      filterOn: [],
      filtered_visible: false
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
      let entry = {};
      entry["key"] = header;
      entry["sortable"] = true;
      this.dataframe_headers.push(entry);
    }
    console.log('haaaaaaaha')
    console.log(this.dataframe_filtered)
    if(this.dataframe_filtered.length() > 0) {
      this.filtered_visible = true;
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
  grid-template-columns: auto auto auto 1fr;
  grid-column-gap: 30px;
  align-items: center;
}
.pagination {
  width: min-content;
}
.switch-label {
  width: 42px !important;
}
.switch {
  position: relative;
  display: inline-block;
  width: 42px;
  height: 26px;
}

.inline-element>* {
  display: inline-block !important;
}
.form-group {
  display: inline-flex;
  margin-bottom: 0;
}
#toggle-filtered {
  text-align: right;
}
label, ul {
  margin-bottom: .5rem !important;
}
.bv-no-focus-ring {
  margin-left: 10px;
}
/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #007bff;
}

input:focus + .slider {
  box-shadow: 0 0 1px #007bff;
}

input:checked + .slider:before {
  -webkit-transform: translateX(16px);
  -ms-transform: translateX(16px);
  transform: translateX(16px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
.filter-toggle {
  display: flex;
}
.filter-toggle-text {
  font-size: 0.875rem;
  line-height: 1.5;
  margin-left: 5px;
}
</style>