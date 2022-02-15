import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import locale from 'element-ui/lib/locale/lang/en'

import global_ from './components/Global'

Vue.use(ElementUI, { locale })

Vue.config.productionTip = false

// Set global variables for all components
Vue.prototype.GLOBAL = global_

new Vue({
  render: h => h(App),
}).$mount('#app')
