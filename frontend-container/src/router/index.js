import Vue from 'vue';
import VueRouter from 'vue-router';
import ping from '../components/ping.vue';
import matrix from '../components/matrix.vue';

Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'matrix',
      component: matrix,
    },
    {
      path: '/ping',
      name: 'ping',
      component: ping,
    }
  ],
});

