import { createApp } from "vue";
import { createPinia } from "pinia";

import router from "./router";

// 从 npm 包引入全局样式库
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

import "./styles/global/main.css";
import "./styles/global/alert.css";
import "./styles/global/badge.css";
import "./styles/global/button.css";
import "./styles/global/card.css";

import App from "./App.vue";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");
