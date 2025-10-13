import { createApp } from "vue";
import { createPinia } from "pinia";
import { lightTheme, darkTheme, useOsTheme } from "naive-ui";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "@/styles/global.css";
import router from "./router";
import App from "./App.vue";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");