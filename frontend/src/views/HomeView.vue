<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import StatCard from '../components/dashboard/StatCard.vue'
import RecentSearches from '../components/dashboard/RecentSearches.vue'
import RecommendedResources from '../components/dashboard/RecommendedResources.vue'

const { t } = useI18n()
const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
  }
}
</script>

<template>
  <div class="fade-in">
    <section class="mb-12">
      <div class="text-center max-w-3xl mx-auto mb-10">
        <h1 class="text-4xl font-bold mb-4 text-primary-700 dark:text-primary-400">
          {{ t('home.title') }}
        </h1>
        <p class="text-lg text-neutral-600 dark:text-neutral-300 mb-8">
          {{ t('home.subtitle') }}
        </p>
        
        <form @submit.prevent="handleSearch" class="relative max-w-2xl mx-auto">
          <input
            v-model="searchQuery"
            type="text"
            class="input py-3 pl-12 pr-4 w-full text-lg"
            :placeholder="t('home.search_placeholder')"
          />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6 text-neutral-400">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <button type="submit" class="btn btn-primary absolute right-1 top-1 bottom-1">
            {{ t('home.search_button') }}
          </button>
        </form>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard 
          title="Literature Database"
          value="50,000+"
          icon="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 19 7.5 19s3.332-.477 4.5-1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 19 16.5 19c-1.746 0-3.332-.477-4.5-1.253"
          color="primary"
        />
        <StatCard 
          title="Research Papers"
          value="25,000+"
          icon="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          color="secondary"
        />
        <StatCard 
          title="Users"
          value="2,500+"
          icon="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
          color="accent"
        />
      </div>
    </section>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <RecentSearches />
      <RecommendedResources />
    </div>
    
    <section class="mt-12 bg-primary-50 dark:bg-primary-900/20 rounded-lg p-6">
      <h2 class="text-2xl font-bold mb-4">{{ t('home.features.title') }}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="card slide-in" style="animation-delay: 0ms;">
          <div class="text-primary-600 dark:text-primary-400 mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-8 w-8">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">{{ t('home.features.search.title') }}</h3>
          <p class="text-neutral-600 dark:text-neutral-400">
            {{ t('home.features.search.description') }}
          </p>
        </div>
        
        <div class="card slide-in" style="animation-delay: 100ms;">
          <div class="text-secondary-500 dark:text-secondary-400 mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-8 w-8">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">{{ t('home.features.ml.title') }}</h3>
          <p class="text-neutral-600 dark:text-neutral-400">
            {{ t('home.features.ml.description') }}
          </p>
        </div>
        
        <div class="card slide-in" style="animation-delay: 200ms;">
          <div class="text-accent-300 dark:text-accent-300 mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-8 w-8">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">{{ t('home.features.organize.title') }}</h3>
          <p class="text-neutral-600 dark:text-neutral-400">
            {{ t('home.features.organize.description') }}
          </p>
        </div>
      </div>
    </section>
  </div>
</template>