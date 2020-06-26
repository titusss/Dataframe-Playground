import Vue from 'vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'


Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.component('vue-bootstrap-typeahead', VueBootstrapTypeahead)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')