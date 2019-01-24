import Vue from 'vue';
import Router from 'vue-router';
import Cases from '@/components/Cases';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Cases',
      component: Cases,
    },
  ],
  mode: 'hash',
});
