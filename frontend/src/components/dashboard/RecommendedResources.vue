<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Mock data for recommended resources
const recommendations = [
  {
    id: 1,
    title: 'Advances in Sustainable Mining Techniques',
    authors: 'Schmidt, J., Wang, L.',
    journal: 'Journal of Mining Engineering',
    year: 2024,
    relevance: 98
  },
  {
    id: 2,
    title: 'Machine Learning Applications in Resource Extraction',
    authors: 'Garcia, M., Johnson, T., Lee, S.',
    journal: 'Data Science in Industrial Applications',
    year: 2025,
    relevance: 95
  },
  {
    id: 3,
    title: 'Environmental Impact Assessment of Modern Mining Operations',
    authors: 'Patel, A., Müller, K.',
    journal: 'Environmental Engineering Science',
    year: 2024,
    relevance: 92
  }
]
</script>

<template>
  <div class="card h-full">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">{{ t('dashboard.recommendations') }}</h2>
      <router-link to="/search" class="text-primary-600 dark:text-primary-400 hover:underline text-sm">
        {{ t('dashboard.more_like_these') }}
      </router-link>
    </div>
    
    <ul class="space-y-4">
      <li v-for="item in recommendations" :key="item.id" class="border border-neutral-200 dark:border-neutral-700 rounded-md p-3 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors duration-200">
        <router-link :to="`/document/${item.id}`">
          <h3 class="font-medium text-primary-600 dark:text-primary-400">{{ item.title }}</h3>
          <p class="text-sm text-neutral-600 dark:text-neutral-300 mt-1">{{ item.authors }}</p>
          <div class="flex justify-between items-center mt-2 text-xs text-neutral-500 dark:text-neutral-400">
            <span>{{ item.journal }}, {{ item.year }}</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-300">
              {{ t('dashboard.relevance', { score: item.relevance }) }}
            </span>
          </div>
        </router-link>
      </li>
    </ul>
    
    <div v-if="recommendations.length === 0" class="py-6 text-center text-neutral-500 dark:text-neutral-400">
      {{ t('dashboard.no_recommendations') }}
    </div>
  </div>
</template>