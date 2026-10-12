<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import SearchResult from '../components/search/SearchResult.vue'
import ResultsVisualizations from '../components/search/ResultsVisualizations.vue'

const { t } = useI18n()
const route = useRoute()

const searchQuery = ref('')
const isLoading = ref(true)
const results = ref<any[]>([])
const currentPage = ref(1)
const totalResults = ref(0)
const resultsPerPage = 10
const sortBy = ref('relevance')
const showVisualizations = ref(false)

const fetchResults = async () => {
  const start = performance.now()  // ← ajoute cette ligne ici
  isLoading.value = true
  try {
    const response = await fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(searchQuery.value)}`)
    const data = await response.json()

    const end = performance.now()
    console.log(`⏱ fetchResults duration: ${(end - start).toFixed(2)} ms`)

results.value = data.map((item: any, index: number) => ({
  id: item.id ?? index + 1,
  title: item.title || 'No Title',
  authors: item.authors || ['Unknown Author'],
  journal: item.source || 'Unknown Journal',
  source:  item.source || 'Unknown Source',
  year: item.year || 'N/A',
  abstract: item.abstract || 'Abstract not available',
  keywords: item.keywords || [],
  doi: item.doi || '',
  url: item.url || '',
  references: item.references || 0,
  figures: item.figures || 0,
  tables: item.tables || 0,
  citations: item.citations || 0,
  metrics: item.metrics || {
    relevance: 80,
    methodQuality: 70,
    novelty: 60,
    impactFactor: 3.2
  },
  sections: item.sections || [],
  ml_score: item.ml_score || 0  // ✅ AJOUT ICI
}))


    totalResults.value = results.value.length
        totalResults.value = results.value.length

    // 🧠 Sauvegarder la recherche dans sessionStorage
    sessionStorage.setItem("searchQuery", searchQuery.value)
    sessionStorage.setItem("searchResults", JSON.stringify(results.value))
    sessionStorage.setItem("totalResults", totalResults.value.toString())

  } catch (error) {
    console.error('Erreur lors de la récupération :', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {

  // 🧠 Vérifier si on a des résultats en cache
  const cachedQuery = sessionStorage.getItem("searchQuery")
  const cachedResults = sessionStorage.getItem("searchResults")
  const cachedTotal = sessionStorage.getItem("totalResults")

  // Si on revient à la même recherche → restaurer
  if (cachedQuery && cachedResults && route.query.q === cachedQuery) {
    searchQuery.value = cachedQuery
    results.value = JSON.parse(cachedResults)
    totalResults.value = parseInt(cachedTotal || "0")
    isLoading.value = false
    console.log("✅ Résultats restaurés depuis sessionStorage")
    return
  }

  // 🔎 Sinon, faire une vraie recherche
  if (route.query.q) {
    searchQuery.value = route.query.q as string
    await fetchResults()
  }
})


const handleSortChange = (event: Event) => {
  sortBy.value = (event.target as HTMLSelectElement).value
}

const paginatedResults = computed(() => {
  let sorted = [...results.value]

  switch (sortBy.value) {
    case 'date_desc':
      sorted.sort((a, b) => b.year - a.year)
      break
    case 'date_asc':
      sorted.sort((a, b) => a.year - b.year)
      break
    case 'citations':
      sorted.sort((a, b) => b.citations - a.citations)
      break
    case 'relevance':
    default:
      sorted.sort((a, b) => b.ml_score - a.ml_score)
      break
  }

  const start = (currentPage.value - 1) * resultsPerPage
  return sorted.slice(start, start + resultsPerPage)
})


const totalPages = computed(() => Math.ceil(totalResults.value / resultsPerPage))

const changePage = (page: number) => {
  if (page > 0 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const toggleVisualizations = () => {
  showVisualizations.value = !showVisualizations.value
}
</script>

<template>
  <div class="fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">
        {{ t('results.title', { query: searchQuery }) }}
      </h1>

      <div class="flex items-center mt-3 md:mt-0">
        <!-- Toggle visualizations -->
        <button
          class="btn btn-outline flex items-center mr-3"
          @click="toggleVisualizations"
          aria-label="Toggle visualizations"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5 mr-1">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          {{ showVisualizations ? t('results.hide_visualizations') : t('results.show_visualizations') }}
        </button>

        <!-- Sorting -->
        <div class="flex items-center">
          <label for="sortOrder" class="text-sm text-neutral-600 dark:text-neutral-400 mr-2">
            {{ t('results.sort_by') }}
          </label>
     <select
  id="sortOrder"
  v-model="sortBy"
  class="input py-1 pl-2 pr-8 text-sm"
  @change="handleSortChange"
>
  <option value="relevance">Relevance</option>
  <option value="date_desc">Newest First</option>
  <option value="date_asc">Oldest First</option>
  <option value="citations">Most Cited</option>
</select>

        </div>
      </div>
    </div>

    <!-- Loading spinner -->
    <div v-if="isLoading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600"></div>
    </div>

    <!-- Results content -->
    <div v-else>
      <!-- Visualizations -->
      <transition
        enter-active-class="transition-opacity duration-300 transition-max-height duration-500 overflow-hidden"
        enter-from-class="opacity-0 max-h-0"
        enter-to-class="opacity-100 max-h-[800px]"
        leave-active-class="transition-opacity duration-200 transition-max-height duration-300 overflow-hidden"
        leave-from-class="opacity-100 max-h-[800px]"
        leave-to-class="opacity-0 max-h-0"
      >
        <ResultsVisualizations
          v-if="showVisualizations && results.length"
          :results="results"
          class="mb-8"
        />
      </transition>

      <!-- Results count -->
      <p class="text-neutral-600 dark:text-neutral-400 mb-4">
        {{ t('results.showing_results', {
          start: (currentPage - 1) * resultsPerPage + 1,
          end: Math.min(currentPage * resultsPerPage, totalResults),
          total: totalResults
        }) }}
      </p>

      <!-- Results list -->
      <div class="space-y-4 mb-8">
        <SearchResult
          v-for="result in paginatedResults"
          :key="result.id"
          :result="result"
        />
      </div>

      <!-- Pagination -->
      <div class="flex justify-center">
        <nav class="inline-flex rounded-md shadow-sm" aria-label="Pagination">
          <!-- Previous -->
          <button
            type="button"
            class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700"
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
            aria-label="Previous page"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>

          <!-- Pages -->
          <template v-for="page in totalPages" :key="page">
            <button
              v-if="page === 1 || page === totalPages || (page >= currentPage - 1 && page <= currentPage + 1)"
              type="button"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                page === currentPage
                  ? 'z-10 bg-primary-50 dark:bg-primary-900 border-primary-300 dark:border-primary-700 text-primary-600 dark:text-primary-300'
                  : 'bg-white dark:bg-neutral-800 border-neutral-300 dark:border-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700'
              ]"
              @click="changePage(page)"
              :aria-label="`Page ${page}`"
            >
              {{ page }}
            </button>

            <!-- Ellipsis -->
            <span
              v-else-if="(page === 2 && currentPage > 3) || (page === totalPages - 1 && currentPage < totalPages - 2)"
              class="relative inline-flex items-center px-4 py-2 border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-sm font-medium text-neutral-500"
            >
              ...
            </span>
          </template>

          <!-- Next -->
          <button
            type="button"
            class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700"
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
            aria-label="Next page"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
        </nav>
      </div>
    </div>
  </div>

</template>
