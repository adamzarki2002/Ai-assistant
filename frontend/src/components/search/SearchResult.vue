<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()

const showToast = ref(false)
const toastMessage = ref('')
const showAbstract = ref(false)
const isStarred = ref(false)

const toggleAbstract = () => {
  showAbstract.value = !showAbstract.value
}

const openExternalLink = (url: string) => {
  window.open(url, '_blank')
}
onMounted(() => {
  const favorites = JSON.parse(localStorage.getItem('starredDocuments') || '[]')
  isStarred.value = favorites.some((item: any) => item.id === props.result.id)
})
const toggleStar = () => {
  const favorites = JSON.parse(localStorage.getItem('starredDocuments') || '[]')

  if (isStarred.value) {
    const updated = favorites.filter((item: any) => item.id !== props.result.id)
    localStorage.setItem('starredDocuments', JSON.stringify(updated))
    isStarred.value = false
  } else {
    favorites.push({ ...props.result, dateAdded: new Date().toISOString() }) // On ajoute dateAdded
    localStorage.setItem('starredDocuments', JSON.stringify(favorites))
    isStarred.value = true
  }
}
const cacheAndGoToDocument = async (article: any) => {
  const res = await fetch('http://localhost:8000/api/cache-document', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(article),
  })
  const data = await res.json()
  router.push({ name: 'document', params: { id: data.id } })
}

const cite = (article: any) => {
  const citation = `${article.authors.join(', ')}. (${article.year}). ${article.title}. ${article.journal}. DOI: ${article.doi || 'N/A'}`
  navigator.clipboard.writeText(citation)
  toastMessage.value = '📋 Zitat in die Zwischenablage kopiert!'
  showToast.value = true
  setTimeout(() => showToast.value = false, 3000)
}

// 👇 Props du composant
const props = defineProps<{
  result: {
    id: number | string
    title: string
    authors: string[]
    journal: string
    year: number | string
    abstract: string
    keywords: string[]
    relevance: number
    doi?: string
    url?: string
    ml_score?: number
  }
}>()

const fetchAbstractFromURL = async (url: string) => {
  try {
    const response = await fetch(`http://localhost:8000/api/extract?url=${encodeURIComponent(url)}`)
    const data = await response.json()
    props.result.abstract = data.abstract || 'Abstract not available'
  } catch (error) {
    console.error("Erreur d'extraction :", error)
    props.result.abstract = 'Abstract not available'
  }
}

const loadAbstractOnDemand = async () => {
  // Si déjà chargé correctement → toggle
  if (
    props.result.abstract &&
    !/not available|erreur|non disponible|non trouvé/i.test(props.result.abstract)
  ) {
    showAbstract.value = !showAbstract.value
    return
  }

  // Marque comme “chargement” visible immédiatement
  props.result.abstract = '<em style="color:#aaa">Loading abstract...</em>'
  showAbstract.value = true

  const articleUrl = props.result.url || (props.result.doi ? `https://doi.org/${props.result.doi}` : '')

  try {
    const res = await fetch(`http://localhost:8000/api/extract?url=${encodeURIComponent(articleUrl)}`)
    const data = await res.json()

    props.result.abstract = data.abstract && data.abstract.trim() !== ''
      ? data.abstract
      : '<em style="color:#aaa">Abstract non disponible</em>'
  } catch (e) {
    props.result.abstract = '<em style="color:#aaa">Erreur lors de l’extraction</em>'
  }
}


</script>

<template>
  <div class="card hover:shadow-md transition-shadow duration-300 p-4">
    <!-- Title + relevance -->
    <div class="flex justify-between items-start">
      <button
        @click="cacheAndGoToDocument(result)"
        class="text-lg font-semibold text-primary-700 dark:text-primary-300 hover:underline text-left"
      >
        {{ result.title }}
       

      </button>

   <span
  :class="[
    'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
    result.ml_score >= 0.8
      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
      : result.ml_score >= 0.5
      ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
      : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
  ]"
>
  {{ (result.ml_score * 100).toFixed(0) }}%
</span>


    </div>

    <!-- Authors + source -->
    <p class="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
      {{ result.authors.join(', ') }}
    </p>
    <p class="text-sm text-neutral-500 dark:text-neutral-500 mt-1">
      {{ result.journal }}, {{ result.year }}
    </p>
       <span class="inline-block mt-1 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
  {{ result.source }}
</span>


    <!-- Keywords -->
    <div class="mt-2 flex flex-wrap gap-1">
      <span
        v-for="(keyword, index) in result.keywords"
        :key="index"
        class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-300"
      >
        {{ keyword }}
      </span>
    </div>

    <!-- Abstract toggle -->
    <div class="mt-3">
     <button 
  type="button"
  class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300 flex items-center"
  @click="loadAbstractOnDemand"
>

        <span>{{ showAbstract ? t('results.hide_abstract') : t('results.show_abstract') }}</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" :class="{ 'transform rotate-180': showAbstract }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

     <!-- Abstract -->
<div v-if="showAbstract" class="mt-2 text-sm text-neutral-300 bg-neutral-800 p-3 rounded-md animate-fade-in">
  <div v-if="result.abstract && result.abstract.trim() !== ''" v-html="result.abstract"></div>
  <em v-else class="text-neutral-400">Abstract not available</em>
</div>


    </div>

  <div class="mt-3 flex flex-wrap gap-4 items-center text-sm text-neutral-600 dark:text-neutral-400">
  <button @click="cacheAndGoToDocument(result)" class="hover:underline">
    {{ t('results.view_document') }}
  </button>

  <button class="hover:text-neutral-900 dark:hover:text-white">
    {{ t('results.save') }}
  </button>

  <button @click="cite(result)" class="hover:text-neutral-900 dark:hover:text-white">
    {{ t('results.cite') }}
  </button>
    <!-- ⭐️ Star button -->
      <button
        @click="toggleStar"
        :class="[
          'flex items-center text-lg',
          isStarred ? 'text-yellow-400' : 'text-neutral-400 hover:text-yellow-500'
        ]"
        title="Add to collection"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
          <path
            :d="isStarred 
              ? 'M12 17.27L18.18 21 16.54 13.97 22 9.24 14.81 8.63 12 2 9.19 8.63 2 9.24 7.46 13.97 5.82 21z'
              : 'M22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.64-7.03L22 9.24z'"
          />
        </svg>
      </button>

<!-- Bouton cliquable -->
<button
  v-if="result.url && result.url.startsWith('http')"
  @click="openExternalLink(result.url)"
  class="text-sm text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1"
>
  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 3h7v7m0 0L10 21l-7-7 11-11z" />
  </svg>
  {{ t('results.open_article') }}
</button>




</div>


    <!-- Toast -->
    <transition name="fade">
      <div
        v-if="showToast"
        class="fixed bottom-5 right-5 bg-green-600 text-white px-4 py-2 rounded-md shadow-md z-50"
      >
        {{ toastMessage }}
      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

button.star-button {
  transition: color 0.3s ease;
}

button.star-button:hover {
  color: #fbbf24; /* Tailwind 'yellow-400' */
}

svg.star-icon {
  transition: fill 0.3s ease;
}
</style>
