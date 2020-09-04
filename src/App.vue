<template>
  <div id="app">
    <error_alert
      :error="error"
      @error_alert_dismissed="error = null"
      style="position:fixed;top:10px;width:100vw;z-index:1060;"
    />
    <loading
      v-if="loading.state"
      :increment="this.loading.increment"
      style="position: fixed;z-index: 100;top: 0;left: 0;width: 100vw;"
    />
    <!-- <b-progress v-if="loading.state" :value="loading.bar.value" :variant="loading.bar.variant" :key="loading.bar.variant" height="6px"></b-progress> -->
    <!-- <div class="loading" v-if="loading"><b-spinner label="Spinning"></b-spinner><span>Loading ...</span></div> -->
    <div>
      <div v-if="loading.state === false">
        <toolbar :locked="config.locked" :backend_url="backend_url" @error_occured="error_occured" />
      </div>
      <div class="grid_container">
        <!-- <div class="header">
        <b-button variant="secondary" size="sm"><b-icon icon="cloud-download" aria-hidden="true"></b-icon></b-button>
        <b-button variant="secondary" size="sm"><b-icon icon="upload" aria-hidden="true"></b-icon></b-button>
        </div>-->
        <div class="main_cell">
          <div class="main_cell_header block">
            <div class="cell_title_ud">
              <h5 class="title">Upload data</h5>
            </div>
            <div
              class="cell_upload_data field"
              @click="show_modal('bv_modal_addData')"
              id="upload_data_parent"
            >
              <b-popover
                id="tutorial_popover"
                :no-fade="true"
                triggers
                placement="right"
                target="upload_data_parent"
                title="1. Upload your data"
              >Click on the + to upload, merge, or remove multiple datasets from our databases or your computer.</b-popover>
              <addDataButton v-on:plugin_clicked="show_modal('modal_add_plugin')" />
              <!-- <b-button variant="secondary"><b-icon icon="table"></b-icon>Upload</b-button> -->
            </div>
            <div class="cell_title_sp">
              <h5 class="title">Select the visualization</h5>
            </div>
            <div
              class="cell_select_plugin field plugins"
              id="select_plugin_parent"
              v-if="config.plugins"
            >
              <b-popover
                id="tutorial_popover"
                :no-fade="true"
                triggers
                placement="top"
                target="select_plugin_parent"
                title="5. Visualize your data"
              >Click on one of the plugins (e.g. Clustergrammer, Plotly) above to generate a plot.</b-popover>
              <plugins
                @click.native="select_plugin(plugin)"
                :active_plugin="this.config.active_plugin_id"
                v-for="plugin in config.plugins"
                :key="plugin.name"
                :title="plugin.name"
                :desc="plugin.desc"
                :image_url="plugin.image_url"
                :id="plugin._id.$oid"
              />
              <!-- <plugins
                v-on:plugin_clicked="show_modal('modal_add_plugin')"
                :title="'Add Plugin'"
                :desc="'Connect a new visualization'"
                :img="'add_plugin.svg'"
              />-->
            </div>
          </div>
          <!-- <h5 class="title">Filter queries</h5> -->
          <div class="field block" v-if="this.config.transformed_dataframe.length > 0">
            <search_query
              @dataframe_filtered="redirect_to_config($event); update_filtered(true)"
              @error_occured="error_occured"
              v-bind:df_categories="Object.keys(this.config.transformed_dataframe[0])"
              v-bind:server_queries="this.config.query"
              v-bind:backend_url="backend_url"
              v-if="!this.loading.state"
            />
          </div>
          <div>
            <visualization v-bind:vis_link="this.active_vis_link" v-if="this.active_vis_link" />
          </div>
          <div class="html_dataframe" v-if="config.transformed_dataframe.length > 0">
            <dataframe
              v-bind:dataframe="this.config.transformed_dataframe"
              v-bind:dataframe_filtered="this.config.filtered_dataframe"
              v-bind:update_is_filter="this.filtered"
            />
          </div>
        </div>
        <div class="menu"></div>
        <div class="footer"></div>
      </div>

      <div>
        <b-modal id="bv_modal_addData" hide-footer>
          <addDataForm
            v-bind:matrices="this.config.preview_matrices"
            v-bind:plugins="this.config.plugins"
            v-bind:df_categories="Object.keys(this.config.transformed_dataframe)"
            v-bind:backend_url="backend_url"
            @dataframe_change="redirect_to_config($event); update_filtered(false);"
            @error_occured="error_occured"
          />
        </b-modal>
        <b-modal id="modal_add_plugin" hide-footer>
          <add_plugin @plugins_change="redirect_to_config" :backend_url="backend_url" />
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import addDataForm from "./components/addDataForm.vue";
import visualization from "./components/visualization";
import plugins from "./components/plugins";
import add_plugin from "./components/add_plugin";
import addDataButton from "./components/addDataButton";
import search_query from "./components/search_query";
import axios from "axios";
import toolbar from "./components/toolbar";
import dataframe from "./components/dataframe";
import loading from "./components/loading";
import error_alert from "./components/error_alert";
export default {
  name: "App",
  components: {
    addDataForm,
    visualization,
    plugins,
    add_plugin,
    addDataButton,
    search_query,
    toolbar,
    dataframe,
    loading,
    error_alert
  },
  data() {
    return {
      backend_url: 'https://hiri-test-service-dks4e6fxka-ew.a.run.app',
      loading: {
        state: true,
        increment: 10,
        bar: {
          variant: "primary",
          value: 0,
          timer: null
        }
      },
      config: null,
      active_vis_link: "",
      error: null,
      filtered: false
    };
  },
  created() {
    this.load_config();
    console.log(this.config);
    console.log(this.error);
  },
  watch: {
    $route: "load_config"
  },
  methods: {
    select_plugin(plugin) {
      if (this.config.active_matrices.length > 0) {
        console.log(this.config)
        this.active_vis_link = "";
        let new_active_plugin_id = "";
        if (plugin._id.$oid != this.config.active_plugin_id) {
          new_active_plugin_id = plugin._id.$oid;
          let vis_exists = false;
          for (let i in this.config.vis_links) {
            if (this.config.vis_links[i].plugin_id == new_active_plugin_id) {
              this.active_vis_link = this.config.vis_links[i].link;
              vis_exists = true;
              break;
            }
          }
          if (vis_exists === false) {
            // console.log("doesn't contain");
            this.generate_vis_link(plugin);
          }
        }
        const path = `${this.backend_url}/active_plugin_id`;
        var payload = new FormData();
        payload.append("active_plugin_id", JSON.stringify(new_active_plugin_id));
        payload.append("url", JSON.stringify(this.$route.query.config));
        axios.post(path, payload).then(res => {
          if (res.data.error_type) {
            this.error_occured(res.data);
          } else {
            this.load_config();
          }
        });
      }
    },
    update_filtered(state) {
      this.filtered = state;
    },
    generate_vis_link(plugin) {
      this.loading.state = true;
      this.loading.increment = 2;
      const path = `${this.backend_url}/visualization`;
      var payload = new FormData();
      payload.append("plugin", JSON.stringify(plugin));
      payload.append("url", JSON.stringify(this.$route.query.config));
      axios.post(path, payload).then(res => {
        // console.log(res);
        if (res.data.error_type) {
          this.error_occured(res.data);
          // console.log(res);
        } else {
          // this.config.vis_links.push(res);
          // this.load_config()
          // console.log(res);
          this.load_config();
          this.active_vis_link = res.data.vis_link.link;
        }
        this.loading.state = false;
      });
    },
    load_config() {
      this.loading.state = true;
      this.loading.increment = 5;
      // this.active_plugin_id = null;
      this.active_vis_link = null;
      this.config = null;
      const path = `${this.backend_url}/config`;
      var payload = new FormData();
      payload.append("url", JSON.stringify(this.$route.query.config));
      axios
        .post(path, payload)
        .then(res => {
          if (res.data.error_type) {
            this.error_occured(res.data);
          } else {
            this.config = res.data.db_entry;
            this.$nextTick(() => {
              this.loading.state = false;
              console.log(this.config);
              // console.log(res);
              // console.log(this.config.plugins[0]);
            });
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    get_plugins(res) {
      this.hide_modal("modal_add_plugin");
      this.plugins = res.data;
    },
    hide_modal(modal_id) {
      this.$bvModal.hide(modal_id);
    },
    show_modal(modal_id) {
      this.$bvModal.show(modal_id);
    },
    error_occured(error) {
      this.error = error;
      console.log(this.error);
    },
    redirect_to_config(res) {
      // this.config = null
      // console.log("res: ", res);
      // console.log(this.config);
      // console.log(res.data.db_entry_id["$oid"]);
      if (this.config._id == res.data.db_entry_id["$oid"]) {
        // this.$router.go()
        this.active_vis_link = null;
        // this.active_plugin_id = null;
        this.load_config();
      } else {
        this.$router.push({
          path: "/",
          query: { config: res.data.db_entry_id["$oid"] }
        });
      }
      this.hide_modal("bv_modal_addData");
    },
    refresh(modal) {
      this.$router.go();
      this.hide_modal(modal);
    }
  },
  mounted() {
    this.loading.bar.timer = setInterval(() => {
      this.loading.bar.value = this.loading.bar.value + 50 * Math.random(3, 4);
    }, 500);
  },
  beforeDestroy() {
    clearInterval(this.loading.bar.timer);
    this.loading.bar.timer = null;
  }
};
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
  font-size: 0.9rem !important;
  font-weight: 600 !important;
}
.popover {
  z-index: 1030 !important;
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
#bv_modal_addData > * {
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
}
.block {
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