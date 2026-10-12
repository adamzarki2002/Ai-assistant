import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import './style.css'

// Import translations
import en from './locales/en.json'
import de from './locales/de.json'

// Create i18n instance
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    de
  }
})

// Create and mount the app
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')