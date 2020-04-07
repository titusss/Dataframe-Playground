<template>
  <div id="app">
    
    <div>
      <b-button id="show-btn" @click="$bvModal.show('bv_modal_addData')">Add table</b-button>
      <b-modal id="bv_modal_addData" hide-footer>
        <addDataForm @close="hide_modal" />
      </b-modal>
      <baseContainer @show="show_modal" />
    </div>
  </div>
</template>

<script>
import addDataForm from './components/addDataForm.vue'
import baseContainer from './components/baseContainer'

export default {
  name: 'App',
  components: {
    addDataForm,
    baseContainer
  },
  methods: {
    hide_modal() {
      this.$bvModal.hide('bv_modal_addData');
      console.log("ahhh");
    },
    show_modal() {
      this.$bvModal.show('bv_modal_addData');
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