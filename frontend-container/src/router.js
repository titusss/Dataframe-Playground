import Vue from 'vue';
import VueRouter from 'vue-router';
import visualization from './components/visualization.vue';
import matrix from './components/matrix.vue';

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
    {
      path: '/hallo/ja',
      name: 'matrix',
      component: matrix,
    },
    {
        path: '/', 
        component: visualization,
        props(route) {
          return {  myprop: route.query.config }
        }
      }
  ],
});