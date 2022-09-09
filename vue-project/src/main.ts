import Vue from "vue";
import App from "./HomePage.vue";
import Vuetify from "vuetify";

Vue.config.productionTip = false;
Vue.use(Vuetify);

const vuetify = new Vuetify({});

interface ClickOutsideElement extends HTMLElement {
  clickOutsideEvent: (event: Event) => void;
}

Vue.directive("click-outside", {
  bind: function (el, binding) {
    (el as ClickOutsideElement).clickOutsideEvent = function (event: Event) {
      // here I check that click was outside the el and his children
      if (!(el == event.target || el.contains(event.target as HTMLElement))) {
        // and if it did, call method provided in attribute value
        binding.value(event);
      }
    };
    document.body.addEventListener(
      "click",
      (el as ClickOutsideElement).clickOutsideEvent
    );
  },
  unbind: function (el) {
    document.body.removeEventListener(
      "click",
      (el as ClickOutsideElement).clickOutsideEvent
    );
  },
});

new Vue({
  render: (h) => h(App),
  vuetify,
}).$mount("#app");
