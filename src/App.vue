<template>
  <div id="app">
    <div class="loading" v-if="loading"><b-spinner label="Spinning"></b-spinner><span>Loading ...</span></div>
    <div v-if="config">
      <toolbar :locked="config.locked"/>
    <div class="grid_container">
      <!-- <div class="header">
        <b-button variant="secondary" size="sm"><b-icon icon="cloud-download" aria-hidden="true"></b-icon></b-button>
        <b-button variant="secondary" size="sm"><b-icon icon="upload" aria-hidden="true"></b-icon></b-button>
      </div> -->
      <div class="main_cell">
        <div class="main_cell_header">
          <div class="cell_title_ud"><h5 class="title">Upload data</h5></div>
          <div class="cell_upload_data field" @click="show_modal('bv_modal_addData')">
            <addDataButton v-on:plugin_clicked="show_modal('modal_add_plugin')"/>
            <!-- <b-button variant="secondary"><b-icon icon="table"></b-icon>Upload</b-button> -->
          </div>
          <div class="cell_title_sp"><h5 class="title">Select the visualization</h5></div>
          <div class="cell_select_plugin field plugins">
            <plugins @click.native="select_plugin(plugin.name)" :active_plugin="active_plugin" v-for="plugin in config.plugins" :key="plugin.name" :title="plugin.name" :desc="plugin.desc" :img="plugin.filename"/>
            <plugins v-on:plugin_clicked="show_modal('modal_add_plugin')" :title="'Add Plugin'" :desc="'Connect a new visualization'" :img="'add_plugin.svg'"/>
          </div>
        </div>
        <!-- <h5 class="title">Filter queries</h5> -->
        <div class="field">
          <search_query/>
        </div>
        <div>
          <visualization v-bind:vis_link="this.active_vis_link"/>
        </div>
      </div>
      <div class="menu"></div>
      <div class="footer"></div>
    </div>

    <div>
      <b-modal id="bv_modal_addData" hide-footer>
        <addDataForm v-bind:matrices="this.config.preview_matrices" v-bind:plugins="this.config.plugins" @dataframe_change="redirect_to_config"/>
      </b-modal>
      <b-modal id="modal_add_plugin" hide-footer>
        <add_plugin @plugins_change="redirect_to_config"/>
      </b-modal>
    </div>
  </div>
  </div>

</template>

<script>
import addDataForm from './components/addDataForm.vue'
import visualization from './components/visualization'
import plugins from './components/plugins'
import add_plugin from './components/add_plugin'
import addDataButton from './components/addDataButton'
import search_query from './components/search_query'
import axios from 'axios'
import toolbar from './components/toolbar'
export default {
  name: 'App',
  components: {
    addDataForm,
    visualization,
    plugins,
    add_plugin,
    addDataButton,
    search_query,
    toolbar
  },
  data() {
    return {
      loading: false,
      config: null,
      active_plugin: null,
      active_vis_link: '',
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
    select_plugin(plugin_name) {
      console.log(plugin_name)
      this.active_plugin = plugin_name;
      this.active_vis_link = ''
      console.log(this.config.vis_links[0].plugin_name)
      for (let i = 0; i < this.config.vis_links.length; i++) {
        console.log("hallo")
        if (this.config.vis_links[i].plugin_name == this.active_plugin) {
          this.active_vis_link = this.config.vis_links[i].link;
        }
      }
      console.log(this.active_vis_link)
    },
    load_config() {
      this.config = null
      this.loading = true
      const path = "http://0.0.0.0:5000/config";
      var payload = new FormData();
        payload.append('url', JSON.stringify(this.$route.query.config));
      axios
        .post(path, payload)
        .then(res => {
          this.config = res.data.db_entry
          this.$nextTick(() => {
            this.loading = false
            console.log(this.config)
            console.log(res)
            console.log(this.config.plugins[0])
          });
        })
        .catch(error => {
          console.log(error);
        });
      
    },
    get_plugins(res) {
      this.hide_modal('modal_add_plugin');
      console.log(res.data);
      this.plugins = res.data;
      console.log(this.plugins)
    },
    hide_modal(modal_id) {
      this.$bvModal.hide(modal_id);
    },
    show_modal(modal_id) {
      this.$bvModal.show(modal_id);
    },
    redirect_to_config(res) {
      // this.config = null
      console.log(this.config)
      console.log(res.data.db_entry_id["$oid"])
      if(this.config._id == res.data.db_entry_id["$oid"]) {
        this.$router.go()
      }
      else {
        this.$router.push({ path: '/', query: { config: res.data.db_entry_id["$oid"]}})
      }
      this.hide_modal('bv_modal_addData');
    },
    refresh(modal) {
      this.$router.go();
      this.hide_modal(modal);
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
}
h5 {
  font-size: .9rem !important;
  font-weight: 600 !important;
}
/* button {
  margin: 5px !important;
} */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
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
  padding: 0 2rem 2rem 2rem;
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
  padding: 15px;
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