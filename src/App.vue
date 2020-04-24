<template>
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
</template>

<script>
import axios from "axios"
import addDataForm from './components/addDataForm.vue'
import baseContainer from './components/baseContainer'
import visualization from './components/visualization'

export default {
  name: 'App',
  components: {
    addDataForm,
    baseContainer,
    visualization
  },
  data() {
    return {
      vis_link: ""
    }
  },
  created() {
    this.get_vis_link()
  },
  methods: {
    hide_modal() {
      this.$bvModal.hide('bv_modal_addData');
    },
    show_modal() {
      this.$bvModal.show('bv_modal_addData');
    },
    get_vis_link() {
      this.hide_modal();
      console.log("get_vis_link");
      const path = "http://localhost:5000/visualization";
      axios
          .get(path)
          .then(res => {
              console.log(res);
              this.vis_link = res.data.vis_link;
          })
          .catch(error => {
              console.error(error);
              this.get_vis_link();
          });
        }
    }
}
</script>

<style>
#app {
  font-family: "SF Compact Rounded", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 0px;
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
</style>