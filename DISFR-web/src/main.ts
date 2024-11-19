/*
 * @Author: lin-dongyizhi7 2985956026@qq.com
 * @Date: 2024-11-15 00:20:21
 * @LastEditors: lin-dongyizhi7 2985956026@qq.com
 * @LastEditTime: 2024-11-19 17:26:10
 * @FilePath: \systemic financial crises\DISFR-web\src\main.ts
 * @Description: Systemic Financial Crises
 */
// main.ts
import {createApp} from 'vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

import request from "./utils/request";

import i18n from './i18n/index';
import {Pinia} from 'pinia';

import App from './App.vue';

const app = createApp(App);

app.use(ElementPlus);
app.use(i18n);
app.mount('#app');