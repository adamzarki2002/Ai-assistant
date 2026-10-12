<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t, locale } = useI18n()
const router = useRouter()
const isDropdownOpen = ref(false)
const isSearchOpen = ref(false)
const searchQuery = ref('')

const emit = defineEmits(['toggle-sidebar'])

const toggleSidebar = () => {
  emit('toggle-sidebar')
}

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const toggleSearch = () => {
  isSearchOpen.value = !isSearchOpen.value
  if (isSearchOpen.value) {
    setTimeout(() => {
      document.getElementById('header-search')?.focus()
    }, 100)
  }
}

const locales = [
  { code: 'en', label: 'English' },
  { code: 'de', label: 'Deutsch' }
]

const switchLocale = (code: string) => {
  locale.value = code
  isDropdownOpen.value = false
}

const submitSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
    searchQuery.value = ''
    isSearchOpen.value = false
  }
}

const currentLocaleName = computed(() => {
  return locales.find(l => l.code === locale.value)?.label || 'English'
})
</script>

<template>
  <header class="bg-white dark:bg-neutral-800 shadow-sm z-10 relative border-b border-neutral-200 dark:border-neutral-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Left side -->
        <div class="flex items-center">
          <button 
            type="button" 
            class="p-2 rounded-md text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-700"
            @click="toggleSidebar"
            aria-label="Toggle sidebar"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
          
          <router-link to="/" class="flex items-center ml-4 space-x-2">
            <img src="/src/assets/img/logoo.png" alt="Logo" class="h-[60px] w-auto" />

  <span class="text-primary-600 dark:text-primary-400 font-semibold text-xl">ML Literature</span>
</router-link>

        </div>
        
        <!-- Right side -->
        <div class="flex items-center">
          <!-- Search button -->
          <button 
            type="button"
            class="p-2 rounded-md text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-700 mr-2"
            @click="toggleSearch"
            aria-label="Search"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </button>
          
          <!-- Language selector -->
          <div class="relative ml-3">
            <button 
              type="button" 
              class="flex items-center p-2 rounded-md text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-700"
              @click="toggleDropdown"
              aria-label="Change language"
            >
              <span class="mr-2 text-sm">{{ currentLocaleName }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </button>
            
            <div 
              v-if="isDropdownOpen" 
              class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 focus:outline-none"
            >
              <div class="py-1" role="menu" aria-orientation="vertical">
                <button 
                  v-for="loc in locales" 
                  :key="loc.code"
                  class="block w-full text-left px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700"
                  role="menuitem"
                  @click="switchLocale(loc.code)"
                >
                  {{ loc.label }}
                </button>
              </div>
            </div>
          </div>
          
          <!-- Profile link -->
          <router-link 
            to="/profile" 
            class="ml-3 p-2 rounded-md text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-700"
            aria-label="View profile"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </router-link>
        </div>
      </div>
      
      <!-- Search overlay -->
      <div 
  v-if="isSearchOpen" 
  class="absolute top-0 left-1/2 transform -translate-x-1/2 bg-white dark:bg-neutral-800 py-3 px-4 border-b border-neutral-200 dark:border-neutral-700 shadow-md rounded-md w-full max-w-2xl animate-fade-in z-50"
>
  <form class="w-full flex items-center gap-2" @submit.prevent="submitSearch">
          <input 
            id="header-search"
            v-model="searchQuery"
            type="text" 
            class="input flex-1 mr-3"
            :placeholder="t('navbar.search_placeholder')"
          />
          <button 
            type="submit" 
            class="btn btn-primary mr-2"
          >
            {{ t('navbar.search') }}
          </button>
          <button 
            type="button"
            class="btn btn-outline"
            @click="toggleSearch"
          >
            {{ t('navbar.cancel') }}
          </button>
        </form>
      </div>
    </div>
  </header>
</template>