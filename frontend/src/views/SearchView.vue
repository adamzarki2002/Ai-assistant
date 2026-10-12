<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import SearchFilters from '../components/search/SearchFilters.vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const isSearching = ref(false)
const isAdvancedSearch = ref(false)

const advancedFilters = ref({
  yearFrom: 2020,
  yearTo: 2025,
  authors: '',
  journals: [],
  domains: [],
  fullTextSearch: true
})

// Initialize search query from URL parameter
onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q as string
  }
})

const toggleAdvancedSearch = () => {
  isAdvancedSearch.value = !isAdvancedSearch.value
}

const performSearch = () => {
  if (!searchQuery.value.trim()) return
  
  isSearching.value = true
  
  // Simulate search delay
  setTimeout(() => {
    router.push({
      path: '/results',
      query: { 
        q: searchQuery.value,
        ...isAdvancedSearch.value ? {
          yearFrom: advancedFilters.value.yearFrom,
          yearTo: advancedFilters.value.yearTo,
          authors: advancedFilters.value.authors,
          fullText: advancedFilters.value.fullTextSearch
        } : {}
      }
    })
    isSearching.value = false
  }, 800)
}

const suggestedQueries = computed(() => {
  if (!searchQuery.value.trim()) return []
  
  // Mock suggested queries based on current input
  return [
    `${searchQuery.value} methodology`,
    `${searchQuery.value} sustainability`,
    `${searchQuery.value} efficiency assessment`,
    `${searchQuery.value} safety protocols`
  ]
})

const recentSearches = [
  'Underground mining techniques',
  'Mining safety optimization',
  'Sustainable mining practices',
  'Mineral extraction efficiency'
]
</script>

<template>
  <div class="fade-in">
    <h1 class="text-3xl font-bold text-center mb-8">{{ t('search.title') }}</h1>
    
    <div class="max-w-4xl mx-auto mb-8">
      <form @submit.prevent="performSearch">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            class="input py-3 pl-12 pr-4 w-full text-lg shadow-sm"
            :placeholder="t('search.placeholder')"
            aria-label="Search query"
          />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6 text-neutral-400">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          
          <button 
            type="submit" 
            class="btn btn-primary absolute right-1 top-1 bottom-1 flex items-center"
            :disabled="isSearching || !searchQuery.trim()"
          >
            <span v-if="isSearching" class="mr-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isSearching ? t('search.searching') : t('search.search_button') }}
          </button>
        </div>
        
        <div class="flex justify-between mt-3">
          <button 
            type="button"
            class="text-sm text-primary-600 dark:text-primary-400 hover:underline flex items-center"
            @click="toggleAdvancedSearch"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-4 w-4 mr-1">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
            </svg>
            {{ isAdvancedSearch ? t('search.hide_advanced') : t('search.show_advanced') }}
          </button>
        </div>
        
        <transition 
          enter-active-class="transition-opacity duration-300 transition-max-height duration-500 overflow-hidden"
          enter-from-class="opacity-0 max-h-0"
          enter-to-class="opacity-100 max-h-[500px]"
          leave-active-class="transition-opacity duration-200 transition-max-height duration-300 overflow-hidden"
          leave-from-class="opacity-100 max-h-[500px]"
          leave-to-class="opacity-0 max-h-0"
        >
          <div v-if="isAdvancedSearch" class="mt-4 card animate-fade-in">
            <SearchFilters v-model="advancedFilters" />
          </div>
        </transition>
      </form>
      
      <!-- Search suggestions -->
      <div v-if="suggestedQueries.length > 0 && searchQuery.trim() && !isSearching" class="mt-3 card divide-y divide-neutral-200 dark:divide-neutral-700">
        <div class="py-2 px-3 bg-neutral-50 dark:bg-neutral-800 text-sm text-neutral-500 dark:text-neutral-400 rounded-t-md">
          {{ t('search.suggested_queries') }}
        </div>
        <ul>
          <li v-for="(query, index) in suggestedQueries" :key="index">
            <button 
              type="button"
              class="w-full text-left py-2 px-3 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors duration-200"
              @click="searchQuery = query; performSearch()"
            >
              {{ query }}
            </button>
          </li>
        </ul>
      </div>
    </div>
    
    <!-- Recent searches and trending topics -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">{{ t('search.recent_searches') }}</h2>
        <ul class="space-y-2">
          <li v-for="(search, index) in recentSearches" :key="index">
            <button 
              type="button"
              class="w-full text-left py-2 px-3 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-md transition-colors duration-200 text-primary-600 dark:text-primary-400"
              @click="searchQuery = search; performSearch()"
            >
              {{ search }}
            </button>
          </li>
        </ul>
      </div>
      
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">{{ t('search.trending_topics') }}</h2>
        <div class="flex flex-wrap gap-2">
          <button 
            v-for="i in 6" 
            :key="i"
            class="px-3 py-1 bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-sm hover:bg-primary-100 dark:hover:bg-primary-800/50 transition-colors duration-200"
            @click="searchQuery = `Mining Topic ${i}`; performSearch()"
          >
            Mining Topic {{ i }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>