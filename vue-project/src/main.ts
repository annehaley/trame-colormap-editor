import Vue from "vue";
import App from "./HomePage.vue";
import Vuetify from "vuetify";

Vue.config.productionTip = false;
Vue.use(Vuetify);

new Vue({
  render: (h) => h(App),
}).$mount("#app");
