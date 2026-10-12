<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Mock data for recent searches
const recentSearches = [
  {
    id: 1,
    query: 'Underground mining techniques',
    date: '2025-04-10',
    count: 157
  },
  {
    id: 2,
    query: 'Mining safety protocols optimization',
    date: '2025-04-08',
    count: 85
  },
  {
    id: 3,
    query: 'Sustainable mining practices',
    date: '2025-04-05',
    count: 134
  },
  {
    id: 4,
    query: 'Mineral extraction efficiency',
    date: '2025-04-02',
    count: 96
  }
]

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat(undefined, { 
    month: 'short', 
    day: 'numeric'
  }).format(date)
}
</script>

<template>
  <div class="card h-full">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">{{ t('dashboard.recent_searches') }}</h2>
      <router-link to="/search" class="text-primary-600 dark:text-primary-400 hover:underline text-sm">
        {{ t('dashboard.view_all') }}
      </router-link>
    </div>
    
    <ul class="divide-y divide-neutral-200 dark:divide-neutral-700">
      <li v-for="search in recentSearches" :key="search.id" class="py-3">
        <router-link 
          :to="{ path: '/results', query: { q: search.query } }"
          class="block hover:bg-neutral-50 dark:hover:bg-neutral-800 -mx-4 px-4 py-2 rounded-md transition-colors duration-200"
        >
          <div class="flex justify-between">
            <p class="font-medium text-neutral-800 dark:text-neutral-200">{{ search.query }}</p>
            <span class="text-neutral-500 dark:text-neutral-400 text-sm">{{ formatDate(search.date) }}</span>
          </div>
          <p class="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
            {{ t('dashboard.results_found', { count: search.count }) }}
          </p>
        </router-link>
      </li>
    </ul>
    
    <div v-if="recentSearches.length === 0" class="py-6 text-center text-neutral-500 dark:text-neutral-400">
      {{ t('dashboard.no_recent_searches') }}
    </div>
  </div>
</template>