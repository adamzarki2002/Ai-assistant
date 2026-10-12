<script setup lang="ts">
import { ref, watch, toRefs } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  modelValue: {
    yearFrom: number
    yearTo: number
    authors: string
    journals: string[]
    domains: string[]
    fullTextSearch: boolean
  }
}>()

const emit = defineEmits(['update:modelValue'])

const { 
  yearFrom, 
  yearTo, 
  authors, 
  journals, 
  domains, 
  fullTextSearch 
} = toRefs(props.modelValue)

const localYearFrom = ref(yearFrom.value)
const localYearTo = ref(yearTo.value)
const localAuthors = ref(authors.value)
const localJournals = ref(journals.value)
const localDomains = ref(domains.value)
const localFullTextSearch = ref(fullTextSearch.value)

const availableJournals = [
  { id: 'jme', name: 'Journal of Mining Engineering' },
  { id: 'ijms', name: 'International Journal of Mining Science' },
  { id: 'rees', name: 'Resources, Energy, & Environmental Science' },
  { id: 'jsd', name: 'Journal of Sustainable Development' },
  { id: 'dsia', name: 'Data Science in Industrial Applications' }
]

const availableDomains = [
  { id: 'um', name: 'Underground Mining' },
  { id: 'sm', name: 'Surface Mining' },
  { id: 'mp', name: 'Mineral Processing' },
  { id: 'env', name: 'Environmental Impact' },
  { id: 'saf', name: 'Safety & Health' },
  { id: 'sus', name: 'Sustainability' },
  { id: 'ml', name: 'Machine Learning & AI' }
]

// Update parent when any local value changes
watch([
  localYearFrom, 
  localYearTo, 
  localAuthors, 
  localJournals, 
  localDomains, 
  localFullTextSearch
], () => {
  emit('update:modelValue', {
    yearFrom: localYearFrom.value,
    yearTo: localYearTo.value,
    authors: localAuthors.value,
    journals: localJournals.value,
    domains: localDomains.value,
    fullTextSearch: localFullTextSearch.value
  })
})

const toggleJournal = (journalId: string) => {
  if (localJournals.value.includes(journalId)) {
    localJournals.value = localJournals.value.filter(id => id !== journalId)
  } else {
    localJournals.value = [...localJournals.value, journalId]
  }
}

const toggleDomain = (domainId: string) => {
  if (localDomains.value.includes(domainId)) {
    localDomains.value = localDomains.value.filter(id => id !== domainId)
  } else {
    localDomains.value = [...localDomains.value, domainId]
  }
}

const resetFilters = () => {
  localYearFrom.value = 2020
  localYearTo.value = 2025
  localAuthors.value = ''
  localJournals.value = []
  localDomains.value = []
  localFullTextSearch.value = true
}
</script>

<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <div>
        <label class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
          {{ t('search.filters.year_range') }}
        </label>
        <div class="flex items-center space-x-2">
          <input 
            v-model.number="localYearFrom" 
            type="number" 
            min="1900" 
            :max="localYearTo"
            class="input"
            aria-label="Year from"
          />
          <span class="text-neutral-500">–</span>
          <input 
            v-model.number="localYearTo" 
            type="number" 
            :min="localYearFrom" 
            :max="new Date().getFullYear()"
            class="input"
            aria-label="Year to"
          />
        </div>
      </div>
      
      <div>
        <label for="authors" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
          {{ t('search.filters.authors') }}
        </label>
        <input 
          id="authors"
          v-model="localAuthors" 
          type="text" 
          class="input"
          :placeholder="t('search.filters.authors_placeholder')"
        />
      </div>
    </div>
    
    <div class="mb-4">
      <h3 class="text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
        {{ t('search.filters.journals') }}
      </h3>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="journal in availableJournals"
          :key="journal.id"
          type="button"
          class="px-3 py-1 rounded-full text-sm transition-colors duration-200"
          :class="localJournals.includes(journal.id) ? 
            'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300' : 
            'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'"
          @click="toggleJournal(journal.id)"
        >
          {{ journal.name }}
        </button>
      </div>
    </div>
    
    <div class="mb-4">
      <h3 class="text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
        {{ t('search.filters.domains') }}
      </h3>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="domain in availableDomains"
          :key="domain.id"
          type="button"
          class="px-3 py-1 rounded-full text-sm transition-colors duration-200"
          :class="localDomains.includes(domain.id) ? 
            'bg-secondary-100 dark:bg-secondary-900 text-secondary-700 dark:text-secondary-300' : 
            'bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-700'"
          @click="toggleDomain(domain.id)"
        >
          {{ domain.name }}
        </button>
      </div>
    </div>
    
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <input 
          id="fullTextSearch" 
          v-model="localFullTextSearch" 
          type="checkbox" 
          class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded"
        />
        <label for="fullTextSearch" class="ml-2 block text-sm text-neutral-700 dark:text-neutral-300">
          {{ t('search.filters.full_text') }}
        </label>
      </div>
      
      <button 
        type="button" 
        class="text-sm text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white"
        @click="resetFilters"
      >
        {{ t('search.filters.reset') }}
      </button>
    </div>
  </div>
</template>