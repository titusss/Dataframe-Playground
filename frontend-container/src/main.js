import Vue from 'vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
<<<<<<< HEAD:frontend-container/src/main.js
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
=======
>>>>>>> bbb249f... Added flask server and sceleton backend:src/main.js

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.component('vue-typeahead-bootstrap', VueTypeaheadBootstrap)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
<<<<<<< HEAD:frontend-container/src/main.js
}).$mount('#app')
=======
}).$mount('#app')
>>>>>>> bbb249f... Added flask server and sceleton backend:src/main.js
