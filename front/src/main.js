// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/fonts/fonts.scss'
import '@/styles/index.scss'

import Vue from 'vue'
import App from './App'
import store from './store'
import router from './router'



import promise from 'es6-promise';
promise.polyfill();
Vue.config.productionTip = false
import '@/permission' // permission control
Vue.use(ElementUI, {

})
Vue.filter('timeDate', function(value) {
  var d = new Date(value * 1000);
  var year = d.getFullYear();
  var month = d.getMonth() + 1;
  var day = d.getDate() <10 ? '0' + d.getDate() : '' + d.getDate();
  var hour = d.getHours();
  var minutes = d.getMinutes();
  var seconds = d.getSeconds();
  return  year+ '-' + month + '-' + day;
})
Vue.filter('timeDate2', function(value) {
  var d = new Date(value * 1000);
  var year = d.getFullYear();
  var month = d.getMonth() + 1;
  var day = d.getDate() <10 ? '0' + d.getDate() : '' + d.getDate();
  var hour = d.getHours();
  var minutes = d.getMinutes();
  var seconds = d.getSeconds();
  return  year+ '-' + month + '-' + day + ' ' + hour + ':' + minutes + ':' + seconds;
})
Vue.filter('timeDay', function(value) {
  var d = new Date(value * 1000);
  var year = d.getFullYear();
  var month = d.getMonth() + 1;
  var day = d.getDate() <10 ? '0' + d.getDate() : '' + d.getDate();
  return  year+ '-' + month + '-' + day;
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
