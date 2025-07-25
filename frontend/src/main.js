import './assets/main.css'

import axios from 'axios'
import App from './App.vue'
import store from "./store"
import router from './router'
import { createApp } from 'vue'
import Notifications from '@kyvg/vue3-notification'

// server address
axios.defaults.baseURL = store.authState.SERVER_ADDR

const app = createApp(App)

// make accessable reactive store object to the entire app
app.provide("store", store)
app.use(router)
app.use(Notifications)
app.mount('#app')