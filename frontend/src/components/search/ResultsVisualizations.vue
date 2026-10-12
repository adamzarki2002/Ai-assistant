<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Bar } from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  Title, 
  Tooltip, 
  Legend 
} from 'chart.js'

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const { t } = useI18n()
const activeTab = ref('timeline')

const props = defineProps<{
  results: any[]
}>()

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
    },
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

// Process data for year distribution
const yearData = computed(() => {
  const years = [...new Set(props.results.map(r => r.year))].sort()
  const counts = years.map(year => 
    props.results.filter(r => r.year === year).length
  )
  
  return {
    labels: years,
    datasets: [
      {
        label: t('visualizations.publications_per_year'),
        data: counts,
        backgroundColor: '#2A9D8F',
      }
    ]
  }
})

// Dummy data for other visualizations
const topicData = {
  labels: ['Sustainability', 'AI in Mining', 'Safety', 'Resource Extraction', 'Environmental Impact'],
  datasets: [
    {
      label: t('visualizations.distribution_by_topic'),
      data: [35, 28, 42, 19, 33],
      backgroundColor: '#1D3557',
    }
  ]
}

const switchTab = (tab: string) => {
  activeTab.value = tab
}
</script>

<template>
  <div class="card">
    <h2 class="text-xl font-semibold mb-4">{{ t('visualizations.title') }}</h2>
    
    <!-- Tabs -->
    <div class="flex border-b border-neutral-200 dark:border-neutral-700 mb-4">
      <button 
        v-for="tab in ['timeline', 'topics', 'relationships']" 
        :key="tab"
        class="px-4 py-2 font-medium text-sm -mb-px transition-colors duration-200"
        :class="activeTab === tab ? 
          'border-b-2 border-primary-600 dark:border-primary-400 text-primary-600 dark:text-primary-400' : 
          'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white'"
        @click="switchTab(tab)"
      >
        {{ t(`visualizations.tabs.${tab}`) }}
      </button>
    </div>
    
    <!-- Timeline tab -->
    <div v-if="activeTab === 'timeline'" class="animate-fade-in">
      <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
        {{ t('visualizations.timeline_description') }}
      </p>
      <div class="h-80">
        <Bar :data="yearData" :options="chartOptions" />
      </div>
    </div>
    
    <!-- Topics tab -->
    <div v-else-if="activeTab === 'topics'" class="animate-fade-in">
      <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
        {{ t('visualizations.topics_description') }}
      </p>
      <div class="h-80">
        <Bar :data="topicData" :options="chartOptions" />
      </div>
    </div>
    
    <!-- Relationships tab -->
    <div v-else-if="activeTab === 'relationships'" class="animate-fade-in">
      <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
        {{ t('visualizations.relationships_description') }}
      </p>
      <div class="h-60 bg-neutral-100 dark:bg-neutral-800 rounded-lg flex items-center justify-center">
        <p class="text-neutral-500 dark:text-neutral-400">
          {{ t('visualizations.network_visualization') }}
        </p>
      </div>
    </div>
  </div>
</template>