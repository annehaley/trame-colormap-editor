import components from './components';
import VueCompositionAPI from '@vue/composition-api'

// TODO: Don't invoke vue composition API here
export function install(Vue) {
  Vue.use(VueCompositionAPI)
  Object.keys(components).forEach((name) => {
    Vue.component(name, components[name]);
  });
}
