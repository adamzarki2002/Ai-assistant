<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// ✅ Ajouter le champ `useInChat` par défaut si absent
const rawSaved = JSON.parse(localStorage.getItem('starredDocuments') || '[]')
const savedDocuments = ref<any[]>(
  rawSaved.map(doc => ({
    ...doc,
    useInChat: doc.useInChat ?? false
  }))
)

const collections = ref([
  { name: 'All Documents', count: savedDocuments.value.length },
  { name: 'Sustainability', count: 2 },
  { name: 'Machine Learning', count: 1 },
  { name: 'Technical', count: 2 },
  { name: 'Environmental', count: 1 }
])

const activeCollection = ref('All Documents')
const sortBy = ref('date_added')

const setActiveCollection = (name: string) => {
  activeCollection.value = name
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).format(date)
}
const removeFromCollection = (id: number | string) => {
  const index = savedDocuments.value.findIndex(doc => doc.id === id)
  if (index !== -1) {
    savedDocuments.value.splice(index, 1)
    localStorage.setItem('starredDocuments', JSON.stringify(savedDocuments.value))
  }
}
const syncWithBackend = async (doc: any) => {
  try {
    await fetch('http://localhost:8000/api/cache-document', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(doc),
    })
    console.log('🔄 Document synchronisé avec le backend:', doc.title)
  } catch (err) {
    console.error('❌ Erreur de synchronisation :', err)
  }
}


// 📥 Extraction de l’abstract depuis l’URL
const fetchAbstractIfNeeded = async (doc: any) => {
  const abstractIsMissing =
    !doc.abstract ||
    doc.abstract.toLowerCase().includes('not available') ||
    doc.abstract.toLowerCase().includes('non trouvé') ||
    doc.abstract.toLowerCase().includes('erreur')

  const articleUrl = doc.url || (doc.doi ? `https://doi.org/${doc.doi}` : null)

  if (abstractIsMissing && articleUrl) {
    try {
      const response = await fetch(`http://localhost:8000/api/extract?url=${encodeURIComponent(articleUrl)}`)
      const data = await response.json()
      doc.abstract = data.abstract || 'Abstract non disponible'
    } catch (error) {
      doc.abstract = `Erreur lors de l'extraction : ${error}`
    }
  }
}

// 🔁 À l’affichage : vérifier et compléter les abstracts
onMounted(async () => {
  for (const doc of savedDocuments.value) {
    await fetchAbstractIfNeeded(doc)
  }
})
// ✅ Observer les changements et sauvegarder localement
watch(
  () => savedDocuments.value.map(d => d.useInChat),
  async (_, __) => {
    localStorage.setItem('starredDocuments', JSON.stringify(savedDocuments.value))  // 🛠 Ajouté
    for (const doc of savedDocuments.value) {
      await syncWithBackend(doc)
    }
  },
  { deep: true }
)


</script>
<template>
  <div class="fade-in">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">{{ t('collection.title') }}</h1>
      <div class="flex items-center">
        <div class="relative">
          <label for="sortCollection" class="sr-only">Sort collection</label>
          <select
            id="sortCollection"
            v-model="sortBy"
            class="input py-1 pl-2 pr-8 text-sm"
          >
            <option value="date_added">{{ t('collection.sort.date_added') }}</option>
            <option value="title">{{ t('collection.sort.title') }}</option>
            <option value="author">{{ t('collection.sort.author') }}</option>
            <option value="year">{{ t('collection.sort.year') }}</option>
          </select>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="md:col-span-1">
        <div class="card sticky top-20">
          <h2 class="text-lg font-semibold mb-3">{{ t('collection.folders') }}</h2>
          <ul class="space-y-1">
            <li v-for="collection in collections" :key="collection.name">
              <button
                class="w-full text-left px-3 py-2 rounded-md flex justify-between items-center transition-colors duration-200"
                :class="activeCollection === collection.name ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300' : 'text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700'"
                @click="setActiveCollection(collection.name)"
              >
                <span>{{ collection.name }}</span>
                <span class="text-xs bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-full px-2 py-0.5">
                  {{ collection.count }}
                </span>
              </button>
            </li>
          </ul>
          <div class="mt-4 pt-4 border-t border-neutral-200 dark:border-neutral-700">
            <button class="w-full btn btn-outline text-sm flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              {{ t('collection.create_folder') }}
            </button>
          </div>
        </div>
      </div>

      <div class="md:col-span-3">
        <div v-if="savedDocuments.length === 0" class="card flex flex-col items-center justify-center py-10">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
          </svg>
          <h2 class="text-xl font-medium mt-4 mb-2">{{ t('collection.empty_title') }}</h2>
          <p class="text-neutral-500 dark:text-neutral-400 text-center max-w-md mb-6">
            {{ t('collection.empty_description') }}
          </p>
          <router-link to="/search" class="btn btn-primary">
            {{ t('collection.start_searching') }}
          </router-link>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="document in savedDocuments"
            :key="document.id"
            class="card hover:shadow-md transition-shadow duration-300 p-4"
          >
      <div class="flex justify-between items-start">
  <div class="flex flex-col">
    <router-link :to="`/document/${document.id}`" class="text-lg font-semibold text-primary-700 dark:text-primary-300 hover:underline">
      {{ document.title }}
    </router-link>
  </div>

  <div class="flex items-start gap-2">
    <span v-if="document.ml_score !== undefined" :class="[
      'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
      document.ml_score >= 0.8
        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
        : document.ml_score >= 0.5
        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
        : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
    ]">
      {{ (document.ml_score * 100).toFixed(0) }}%
    </span>
<!-- ✅ Toggle pour activer dans chatbot -->
<label class="flex items-center cursor-pointer mr-2">
  <input
    type="checkbox"
    v-model="document.useInChat"
    class="sr-only"
  />
  <div
    class="w-10 h-6 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out"
    :class="document.useInChat ? 'bg-green-500' : 'bg-gray-300'"
  >
    <div
      class="bg-white w-4 h-4 rounded-full shadow-md transform duration-300 ease-in-out"
      :class="{ 'translate-x-4': document.useInChat }"
    ></div>
  </div>
</label>

    <!-- Bouton Supprimer -->
    <button
      @click="removeFromCollection(document.id)"
      class="text-neutral-400 hover:text-red-500"
      title="Supprimer cet article"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</div>


            <p class="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
              {{ document.authors.join(', ') }}
            </p>
            <p class="text-sm text-neutral-500 dark:text-neutral-500 mt-1">
              {{ document.journal }}, {{ document.year }}
            </p>
            <div class="mt-2 flex flex-wrap gap-1">
              <span v-for="(keyword, index) in document.keywords" :key="index" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-300">
                {{ keyword }}
              </span>
            </div>
            <div class="mt-3">
              <button type="button" class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300 flex items-center" @click="document.showAbstract = !document.showAbstract">
                <span>{{ document.showAbstract ? t('results.hide_abstract') : t('results.show_abstract') }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" :class="{ 'transform rotate-180': document.showAbstract }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-if="document.showAbstract" class="mt-2 text-sm text-neutral-300 bg-neutral-800 p-3 rounded-md animate-fade-in">
                <div v-if="document.abstract && document.abstract.trim() !== ''" v-html="document.abstract"></div>
                <em v-else class="text-neutral-400">Abstract not available</em>
              </div>
            </div>
            <div class="mt-3 flex flex-wrap gap-4 items-center text-sm text-neutral-600 dark:text-neutral-400">
              <router-link :to="`/document/${document.id}`" class="hover:underline">
                {{ t('results.view_document') }}
              </router-link>
              <button class="hover:text-neutral-900 dark:hover:text-white">
                {{ t('results.save') }}
              </button>
              <button @click="() => copyCite(document)" class="hover:text-neutral-900 dark:hover:text-white">
                {{ t('results.cite') }}
              </button>
              <button v-if="document.url && document.url.startsWith('http')" @click="() => openExternalLink(document.url)" class="text-sm text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 3h7v7m0 0L10 21l-7-7 11-11z" />
                </svg>
                {{ t('results.open_article') }}
              </button>
            </div>
            <span class="text-xs text-neutral-500 dark:text-neutral-400 mt-2 block">
              {{ t('collection.added') }}: {{ formatDate(document.dateAdded) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>