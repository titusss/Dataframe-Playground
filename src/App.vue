<template>
  <div id="app">
    <div>
      <b-button id="show-btn" @click="$bvModal.show('bv-modal-addData')">Add table</b-button>
      <b-modal id="bv-modal-addData" hide-footer>
        <addDataContainer/>
      </b-modal>
    </div>
  </div>
</template>

<script>
import addDataContainer from './components/addDataContainer.vue'

export default {
  name: 'App',
  components: {
    addDataContainer
  }
}
</script>

<style>
#app {
  font-family: SF Compact Rounded, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
.img_in_btn {
  margin-right: 5px;
}
.center {
  text-align: center;
}
#bv-modal-addData>* {
  max-width: 90vw !important;
}
</style>
