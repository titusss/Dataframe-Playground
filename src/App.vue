<!--<template>
  <div id="app">
    <div>
      <b-button id="show-btn" @click="$bvModal.show('bv_modal_addData')">Add table</b-button>
      <b-modal id="bv_modal_addData" hide-footer>
        <addDataForm @dataframe_change="get_vis_link"/>
      </b-modal>
      <baseContainer @show="show_modal" />
      <div class="visualization">
        <visualization v-bind:vis_link="vis_link"/>
      </div>
    </div>
  </div>
</template>-->

<template>
  <div id="app">
    <div v-if="loading"><b-spinner variant="primary" label="Spinning"></b-spinner> Loading ...</div>
    <div v-if="config">
    <div class="grid_container">
      <!-- <div class="header">
        <b-button variant="secondary" size="sm"><b-icon icon="cloud-download" aria-hidden="true"></b-icon></b-button>
        <b-button variant="secondary" size="sm"><b-icon icon="upload" aria-hidden="true"></b-icon></b-button>
      </div> -->
      <div class="main_cell">
        <div class="main_cell_header">
          <div class="cell_title_ud"><h5 class="title">Upload data</h5></div>
          <div class="cell_upload_data field">
            <b-button variant="secondary"><b-icon icon="table"></b-icon>Upload</b-button>
          </div>
          <div class="cell_title_sp"><h5 class="title">Select the visualization</h5></div>
          <div class="cell_select_plugin field plugins">
            <plugins v-on:plugin_clicked="show_modal('bv_modal_addData')" v-for="plugin in plugin_list" :key="plugin.name" :title="plugin.name" :desc="plugin.desc" :img="plugin.icon"/>
            <plugins v-on:plugin_clicked="show_modal('modal_add_plugin')" :title="'Add Plugin'" :desc="'Connect a new visualization'" :img="'add_plugin.svg'" @click="$bvModal.show('bv_modal_addData')"/>
          </div>
        </div>
        <h5 class="title">Filter queries</h5>
        <div class="field">
          <!-- <search_query/> -->
        </div>
        <div>
          <visualization v-bind:vis_link="this.config.vis_link"/>
        </div>
      </div>
      <div class="menu"></div>
      <div class="footer"></div>
    </div>

    <div>
      <b-modal id="bv_modal_addData" hide-footer>
        <addDataForm v-bind:matrices="this.config.preview_matrices" @dataframe_change="redirect_to_config"/>
      </b-modal>
      <b-modal id="modal_add_plugin" hide-footer>
        <add_plugin @plugins_change="get_plugins"/>
      </b-modal>
    </div>
    <router-link :to="{ path: '/', query: { config: 'https://titusebbecke.com'}}">
      About
    </router-link>
  </div>
  </div>

</template>

<script>
import addDataForm from './components/addDataForm.vue'
import visualization from './components/visualization'
import plugins from './components/plugins'
import add_plugin from './components/add_plugin'
// import search_query from './components/search_query'
import axios from 'axios'
export default {
  name: 'App',
  components: {
    addDataForm,
    visualization,
    plugins,
    add_plugin,
    // search_query,
  },
  data() {
    return {
      loading: false,
      config: null,
      plugin_list: [
        {url: "", name:"Clustergrammer", desc:"Clustering Heatmap by Ma'ayan Laboratory", icon: "clustergrammer_preview.svg"},
        {url: "", name:"SandDance", desc:"Microsoft's 2D & 3D data exploration tool.", icon: "sanddance_logo.svg"}
      ]
    }
  },
  created() {
    this.load_config()
    console.log(this.config)
  },
  watch: {
    '$route': 'load_config'
  },
  methods: {
    load_config() {
      this.config = null
      this.loading = true
      const path = "http://192.168.1.31:5000/config";
      var payload = new FormData();
        payload.append('url', JSON.stringify(this.$route.query.config));
      axios
        .post(path, payload)
        .then(res => {
          this.config = res.data.db_entry
          this.$nextTick(() => {
            this.loading = false
            console.log(this.config)
          });
        })
        .catch(error => {
          console.log(error);
        });
      
    },
    get_plugins(res) {
      this.hide_modal('modal_add_plugin');
      console.log(res.data.plugin_list);
      this.plugin_list = res.data.plugin_list;
    },
    hide_modal(modal_id) {
      this.$bvModal.hide(modal_id);
    },
    show_modal(modal_id) {
      this.$bvModal.show(modal_id);
    },
    redirect_to_config(res) {
      // this.config = null
      this.$router.push({ path: '/', query: { config: res.data.db_entry_id["$oid"]}})
      this.hide_modal('bv_modal_addData');
    }
  }
}
</script>

<style>
#app {
  /* font-family: "SF Compact Rounded", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 0px;
  min-height: 100vh;
  padding: 2rem;
}
h5 {
  font-size: .9rem !important;
  font-weight: 600 !important;
}
button {
  margin: 5px !important;
}
.img_in_btn {
  margin-right: 5px;
}
.center {
  text-align: center;
}
#bv_modal_addData>* {
  max-width: 90vw !important;
}
.grid_container {
  display: grid;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}
.main_cell {
  grid-area: 2 / 1 / 3 / 4;
}
.main_cell_header {
  display: grid;
  grid-template-columns: repeat(2, auto);
  grid-template-rows: repeat(2, auto);
  grid-column-gap: 1rem;
  grid-row-gap: 1rem;
  margin-bottom: 1rem;
}
.field {
  background-color: #e9ecef;
  padding: 20px;
  border-radius: 20px;
}
.plugins {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(1, 1fr);
  grid-column-gap: 20px;
  grid-row-gap: 20px;
}
.header {
  grid-area: 1 / 1 / 2 / 4;
  height: 6vh;
  margin-bottom: 2em;
}
.menu {
  width: 10vw;
  grid-area: 2 / 1 / 3 / 2;
}
.footer {
  height: 10vh;
  grid-area: 3 / 1 / 4 / 4;
}
.title {
  margin-bottom: 1em;
}
.cell_upload_data {
  grid-area: 2 / 1 / 3 / 2;
}
.cell_select_plugin {
  grid-area: 2 / 2 / 3 / 3;
}
</style>