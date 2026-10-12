<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

const { t } = useI18n()
const route = useRoute()

defineProps<{
  isOpen: boolean
}>()

const navItems = [
  { 
    name: 'home', 
    path: '/', 
    icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' 
  },
  { 
    name: 'search', 
    path: '/search', 
    icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' 
  },
  { 
    name: 'results', 
    path: '/results', 
    icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01' 
  },
  { 
    name: 'collection', 
    path: '/collection', 
    icon: 'M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z' 
  },
  { 
    name: 'assistant', 
    path: '/assistant', 
    icon: 'M7 8h10M7 12h6m5 4v5l-5-5H6a2 2 0 01-2-2V6a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2h-1z' 
  }
]
</script>

<template>
  <aside 
    class="fixed inset-y-0 left-0 z-20 w-64 bg-white dark:bg-neutral-800 border-r border-neutral-200 dark:border-neutral-700 pt-16 transform transition-transform duration-300 ease-in-out"
    :class="{ '-translate-x-full': !isOpen, 'translate-x-0': isOpen }"
  >
    <nav class="px-4 py-6">
      <ul class="space-y-2">
        <li v-for="item in navItems" :key="item.name">
          <router-link 
            :to="item.path"
            class="flex items-center px-4 py-3 rounded-lg transition-colors duration-200"
            :class="route.path === item.path ? 
              'bg-primary-50 dark:bg-primary-900 text-primary-600 dark:text-primary-400' : 
              'text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700'"
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor" 
              class="h-5 w-5 mr-3"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon"></path>
            </svg>
            <span>{{ t(`nav.${item.name}`) }}</span>
          </router-link>
        </li>
      </ul>
      
      <div class="mt-10 px-4">
        <h4 class="text-xs uppercase tracking-wider text-neutral-500 dark:text-neutral-400 font-semibold mb-3">{{ t('nav.categories') }}</h4>
        <ul class="space-y-1">
          <li v-for="i in 5" :key="i">
            <a href="#" class="block px-3 py-2 text-sm rounded-md text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700">
              {{ t('categories.example', { num: i }) }}
            </a>
          </li>
        </ul>
      </div>
    </nav>
  </aside>
  
  <!-- Overlay background for mobile -->
  <div 
    v-if="isOpen" 
    class="fixed inset-0 bg-neutral-900 bg-opacity-50 z-10 md:hidden transition-opacity duration-300"
    @click="$emit('toggle-sidebar')"
  ></div>
</template>