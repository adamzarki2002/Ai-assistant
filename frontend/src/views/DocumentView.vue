<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const { t } = useI18n()

const isLoading = ref(true)
const document = ref<any>(null)
const relatedDocuments = ref<any[]>([])

const articleFromRoute = history.state?.article
const downloadPDF = () => {
  const doc = document.value

  if (!doc || !doc.doi) {
    alert("Aucun lien PDF disponible.")
    return
  }

  const doi = doc.doi
  const lowerSource = (doc.journal || '').toLowerCase()

  let pdfUrl: string | null = null

  // IEEE
  if (doi.includes("10.1109") || lowerSource.includes("ieee")) {
    const ieeeId = doi.split('/').pop()
    pdfUrl = `https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=${ieeeId}`
  }

  // Elsevier / ScienceDirect
  else if (lowerSource.includes("sciencedirect") || lowerSource.includes("elsevier")) {
    pdfUrl = `https://www.sciencedirect.com/science/article/pii/${doi.split('/').pop()}`
  }

  // Springer
  else if (lowerSource.includes("springer")) {
    pdfUrl = `https://link.springer.com/article/${doi}`
  }

  // EuropePMC
  else if (lowerSource.includes("europepmc")) {
    pdfUrl = `https://europepmc.org/article/MED/${doi.split('/').pop()}`
  }

  // Fallback
  else {
    pdfUrl = `https://doi.org/${doi}`
  }

  window.open(pdfUrl, "_blank")
}


// 🧠 Fonction qui extrait un abstract via une URL (API FastAPI)
const fetchAbstractFromURL = async (url: string) => {
  try {
    const response = await fetch(`http://localhost:8000/api/extract?url=${encodeURIComponent(url)}`)
    const data = await response.json()
    document.value.abstract = data.abstract || 'Abstract non disponible.'
  } catch (error) {
    console.error('Erreur extraction abstract :', error)
    document.value.abstract = 'Erreur lors de l’extraction.'
  }
}

// 🧠 Fonction qui récupère le document par ID depuis l’API
const fetchDocumentById = async (id: string | number) => {
  try {
    const response = await fetch(`http://localhost:8000/api/document/${id}`)
    const data = await response.json()
    document.value = data
  } catch (error) {
    console.error('Erreur fetch par ID :', error)
    document.value = {
      title: 'Erreur de chargement',
      authors: ['Inconnu'],
      journal: 'Inconnu',
      year: 'N/A',
      abstract: 'Impossible de charger le document',
      keywords: [],
      metrics: {
        relevance: 0,
        methodQuality: 0,
        novelty: 0,
        impactFactor: 0
      },
      sections: [],
      references: 0,
      figures: 0,
      tables: 0,
      doi: ''
    }
  }
}

// 🚀 Lors du chargement du composant
onMounted(async () => {
  try {
    if (articleFromRoute) {
      document.value = articleFromRoute
    } else if (route.params.id) {
      await fetchDocumentById(route.params.id as string)
    }

    // 🔎 Génère l’URL à partir du champ `url` ou `doi`
    const articleUrl =
      document.value?.url ||
      (document.value?.doi ? `https://doi.org/${document.value.doi}` : null)

    // 🧪 Vérifie si l’abstract est vide ou invalide
    const abstractIsMissing = !document.value?.abstract ||
      document.value.abstract.toLowerCase().includes('not available') ||
      document.value.abstract.toLowerCase().includes('non trouvé')

    // 🚀 Extraction de l’abstract si nécessaire
    if (articleUrl && abstractIsMissing) {
      await fetchAbstractFromURL(articleUrl)
    }
  } catch (e) {
    console.error('Erreur au montage du document :', e)
  } finally {
    isLoading.value = false
  }
})

// Actions (boutons)
const copyReference = () => alert('Référence copiée !')
const saveDocument = () => alert('Document enregistré.')

</script>
<template>
  <div class="fade-in">
    <div v-if="isLoading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600"></div>
    </div>

    <div v-else class="pb-10">
      <!-- ===== Document Header ===== -->
      <div class="mb-8">
        <h1 class="text-2xl md:text-3xl font-bold mb-4 text-neutral-900 dark:text-neutral-100">
          {{ document.title }}
        </h1>

        <div class="flex flex-wrap items-center text-neutral-600 dark:text-neutral-400 mb-2">
          <p class="mr-4 mb-1">{{ (document.authors || []).join(', ') }}
</p>
          <div class="flex items-center mb-1">
            <span class="mr-2">•</span>
            <p>{{ document.journal }}, {{ document.year }}, {{ document.volume }}({{ document.issue }}), {{ document.pages }}</p>
          </div>
        </div>

        <!-- Keywords -->
        <div class="flex flex-wrap gap-2 mt-3 mb-4">
          <span
            v-for="(keyword, index) in document.keywords"
            :key="index"
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300"
          >
            {{ keyword }}
          </span>
        </div>

        <!-- Action buttons -->
        <div class="flex flex-wrap gap-3 mt-5">
          <button class="btn btn-primary flex items-center" @click="saveDocument">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            {{ t('document.save') }}
          </button>

          <button class="btn btn-outline flex items-center" @click="copyReference">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            {{ t('document.cite') }}
          </button>

          <button class="btn btn-outline flex items-center" @click="downloadPDF">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            {{ t('document.download') }}
          </button>
          
          
        </div>
      </div>

      <!-- ===== Metrics Card ===== -->
      <div class="card mb-8 bg-primary-50 dark:bg-primary-900/20 border-none">
        <h2 class="text-lg font-semibold mb-3">{{ t('document.metrics') }}</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ document.metrics.relevance }}%</div>
            <div class="text-sm text-neutral-600 dark:text-neutral-400">{{ t('document.relevance') }}</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ document.metrics.methodQuality }}%</div>
            <div class="text-sm text-neutral-600 dark:text-neutral-400">{{ t('document.method_quality') }}</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ document.metrics.novelty }}%</div>
            <div class="text-sm text-neutral-600 dark:text-neutral-400">{{ t('document.novelty') }}</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ document.metrics.impactFactor }}</div>
            <div class="text-sm text-neutral-600 dark:text-neutral-400">{{ t('document.impact_factor') }}</div>
          </div>
        </div>
      </div>

<!-- ===== Abstract ===== -->
<div class="card mb-8">
  <h2 class="text-xl font-semibold mb-4">{{ t('document.abstract') }}</h2>
  <div
    v-html="document.abstract"
    style="color: #f1f1f1; background-color: #1f2937; padding: 1rem; border-radius: 0.5rem; line-height: 1.6; font-size: 1rem;"
  ></div>


<div v-if="document.url" class="card mb-8">
  <!-- DOI cliquable (si présent) -->
  <div v-if="document.doi" class="mb-2 text-sm">
    <span class="text-neutral-600 dark:text-neutral-400">DOI:</span>
    <a
      :href="`https://doi.org/${document.doi}`"
      target="_blank"
      class="text-blue-500 underline ml-1 break-all"
    >
      {{ document.doi }}
    </a>
  </div>

  <!-- Lien vers le site de l'éditeur -->
  <div class="flex flex-col gap-3 mt-2">
    <p class="text-sm text-neutral-500 dark:text-neutral-400">
      {{ t('document.view_on_publisher') }}
    </p>
    <a
      :href="document.url"
      target="_blank"
      rel="noopener"
      class="btn btn-primary inline-flex items-center w-fit"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 3h7v7m0 0L10 21l-7-7 11-11z" />
      </svg>
      {{ t('document.open_article') }}
    </a>
  </div>
</div>



      </div>

      <!-- Sections du document -->
<div class="card mb-8">
  <h2 class="text-xl font-semibold mb-4">{{ t('document.content') }}</h2>
  <div v-for="(section, index) in document.sections" :key="index" class="mb-6">
    <h3 class="text-lg font-semibold mb-2 text-neutral-800 dark:text-neutral-200">
      {{ section.title }}
    </h3>
    <p class="text-neutral-700 dark:text-neutral-300 leading-relaxed">
      {{ section.content }}
    </p>
  </div>

        <div class="flex flex-wrap gap-8 mt-6 text-sm text-neutral-600 dark:text-neutral-400">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 19 7.5 19s3.332-.477 4.5-1.253" />
            </svg>
            <span>{{ document.references }} {{ t('document.references') }}</span>
          </div>
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14" />
            </svg>
            <span>{{ document.figures }} {{ t('document.figures') }}</span>
          </div>
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8" />
            </svg>
            <span>{{ document.tables }} {{ t('document.tables') }}</span>
          </div>
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586l6-6A6 6 0 1121 9z" />
            </svg>
            <span>
  DOI:
  <a
    :href="`https://doi.org/${document.doi}`"
    target="_blank"
    class="text-blue-500 underline"
  >
    {{ document.doi }}
  </a>
</span>

          </div>
        </div>
      </div>

      <!-- ===== Related Documents ===== -->
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">{{ t('document.related') }}</h2>
        <div class="space-y-4">
          <div
            v-for="doc in relatedDocuments"
            :key="doc.id"
            class="border border-neutral-200 dark:border-neutral-700 rounded-md p-3 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors duration-200"
          >
            <router-link :to="`/document/${doc.id}`">
              <h3 class="font-medium text-primary-600 dark:text-primary-400">{{ doc.title }}</h3>
              <p class="text-sm text-neutral-600 dark:text-neutral-300 mt-1">{{ doc.authors }}</p>
              <div class="flex justify-between items-center mt-2 text-xs text-neutral-500 dark:text-neutral-400">
                <span>{{ doc.journal }}, {{ doc.year }}</span>
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-300">
                  {{ t('document.relevance_score', { score: doc.relevance }) }}
                </span>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
