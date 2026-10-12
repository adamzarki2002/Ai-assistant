<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Mock user data
const user = ref({
  name: 'Alex Johnson',
  email: 'alex.johnson@example.com',
  institution: 'Mining Research Institute',
  role: 'Researcher',
  joined: '2024-01-15',
  avatar: null,
  researchInterests: ['Sustainable Mining', 'Machine Learning', 'Resource Extraction', 'Environmental Impact'],
  settings: {
    emailNotifications: true,
    darkMode: false,
    defaultLanguage: 'en'
  }
})

// Mock research activity
const researchActivity = ref([
  { 
    type: 'search', 
    date: '2025-04-12T14:25:00', 
    details: { query: 'Machine learning optimization for mining operations' } 
  },
  { 
    type: 'save', 
    date: '2025-04-11T09:12:00', 
    details: { documentId: 2, title: 'Machine Learning Applications in Resource Extraction' } 
  },
  { 
    type: 'view', 
    date: '2025-04-10T16:45:00', 
    details: { documentId: 1, title: 'Advances in Sustainable Mining Techniques' } 
  },
  { 
    type: 'search', 
    date: '2025-04-08T11:30:00', 
    details: { query: 'Sustainable mining practices' } 
  }
])

const activeTab = ref('profile')

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat(undefined, { 
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).format(date)
}

const formatDateTime = (dateTimeString: string) => {
  const date = new Date(dateTimeString)
  return new Intl.DateTimeFormat(undefined, { 
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const switchTab = (tab: string) => {
  activeTab.value = tab
}

const updateProfile = () => {
  // In a real app, this would send the updated profile to the server
  alert('Profile updated successfully!')
}

const removeInterest = (interest: string) => {
  user.value.researchInterests = user.value.researchInterests.filter(i => i !== interest)
}

const newInterest = ref('')
const addInterest = () => {
  if (newInterest.value.trim() && !user.value.researchInterests.includes(newInterest.value)) {
    user.value.researchInterests.push(newInterest.value)
    newInterest.value = ''
  }
}
</script>

<template>
  <div class="fade-in max-w-5xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">{{ t('profile.title') }}</h1>
    
    <!-- Profile tabs -->
    <div class="mb-6 border-b border-neutral-200 dark:border-neutral-700">
      <div class="flex space-x-4">
        <button
          v-for="tab in ['profile', 'activity', 'settings']"
          :key="tab"
          class="px-4 py-2 border-b-2 font-medium text-sm transition-colors duration-200"
          :class="activeTab === tab ? 
            'border-primary-600 dark:border-primary-400 text-primary-600 dark:text-primary-400' : 
            'border-transparent text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white'"
          @click="switchTab(tab)"
        >
          {{ t(`profile.tabs.${tab}`) }}
        </button>
      </div>
    </div>
    
    <!-- Profile Information Tab -->
    <div v-if="activeTab === 'profile'" class="animate-fade-in">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- User Info Card -->
        <div class="card md:col-span-2">
          <h2 class="text-xl font-semibold mb-4">{{ t('profile.personal_info') }}</h2>
          
          <div class="space-y-4">
            <div>
              <label for="name" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                {{ t('profile.name') }}
              </label>
              <input 
                id="name"
                v-model="user.name" 
                type="text" 
                class="input"
              />
            </div>
            
            <div>
              <label for="email" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                {{ t('profile.email') }}
              </label>
              <input 
                id="email"
                v-model="user.email" 
                type="email" 
                class="input"
              />
            </div>
            
            <div>
              <label for="institution" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                {{ t('profile.institution') }}
              </label>
              <input 
                id="institution"
                v-model="user.institution" 
                type="text" 
                class="input"
              />
            </div>
            
            <div>
              <label for="role" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
                {{ t('profile.role') }}
              </label>
              <input 
                id="role"
                v-model="user.role" 
                type="text" 
                class="input"
              />
            </div>
            
            <div class="pt-4 flex justify-end">
              <button class="btn btn-primary" @click="updateProfile">
                {{ t('profile.update') }}
              </button>
            </div>
          </div>
        </div>
        
        <!-- Research Interests Card -->
        <div class="card md:col-span-1">
          <h2 class="text-xl font-semibold mb-4">{{ t('profile.research_interests') }}</h2>
          
          <div class="mb-4">
            <div class="flex">
              <input 
                v-model="newInterest"
                type="text" 
                class="input rounded-r-none"
                :placeholder="t('profile.add_interest')"
              />
              <button 
                class="btn btn-primary rounded-l-none"
                @click="addInterest"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="flex flex-wrap gap-2">
            <div
              v-for="(interest, index) in user.researchInterests"
              :key="index"
              class="flex items-center bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 px-3 py-1 rounded-full text-sm"
            >
              <span>{{ interest }}</span>
              <button 
                class="ml-1 text-primary-500 hover:text-primary-700 dark:hover:text-primary-200"
                @click="removeInterest(interest)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t border-neutral-200 dark:border-neutral-700">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">
              {{ t('profile.member_since') }}: {{ formatDate(user.joined) }}
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Activity Tab -->
    <div v-else-if="activeTab === 'activity'" class="animate-fade-in">
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">{{ t('profile.recent_activity') }}</h2>
        
        <div class="space-y-6">
          <div
            v-for="(activity, index) in researchActivity"
            :key="index"
            class="flex"
          >
            <div class="mr-4">
              <div class="h-10 w-10 rounded-full flex items-center justify-center"
                :class="{
                  'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400': activity.type === 'search',
                  'bg-secondary-100 dark:bg-secondary-900/30 text-secondary-600 dark:text-secondary-400': activity.type === 'save',
                  'bg-accent-100 dark:bg-accent-900/30 text-accent-600 dark:text-accent-400': activity.type === 'view'
                }"
              >
                <svg v-if="activity.type === 'search'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <svg v-else-if="activity.type === 'save'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
                <svg v-else-if="activity.type === 'view'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
            </div>
            
            <div class="flex-1">
              <div v-if="activity.type === 'search'">
                <p class="font-medium">{{ t('profile.activity.searched') }}</p>
                <p class="text-neutral-700 dark:text-neutral-300">
                  "{{ activity.details.query }}"
                </p>
              </div>
              
              <div v-else-if="activity.type === 'save'">
                <p class="font-medium">{{ t('profile.activity.saved') }}</p>
                <router-link :to="`/document/${activity.details.documentId}`" class="text-primary-600 dark:text-primary-400 hover:underline">
                  {{ activity.details.title }}
                </router-link>
              </div>
              
              <div v-else-if="activity.type === 'view'">
                <p class="font-medium">{{ t('profile.activity.viewed') }}</p>
                <router-link :to="`/document/${activity.details.documentId}`" class="text-primary-600 dark:text-primary-400 hover:underline">
                  {{ activity.details.title }}
                </router-link>
              </div>
              
              <p class="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
                {{ formatDateTime(activity.date) }}
              </p>
            </div>
          </div>
        </div>
        
        <div v-if="researchActivity.length === 0" class="py-6 text-center text-neutral-500 dark:text-neutral-400">
          {{ t('profile.no_activity') }}
        </div>
      </div>
    </div>
    
    <!-- Settings Tab -->
    <div v-else-if="activeTab === 'settings'" class="animate-fade-in">
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">{{ t('profile.app_settings') }}</h2>
        
        <div class="space-y-4">
          <div class="flex items-center justify-between py-2">
            <div>
              <h3 class="font-medium">{{ t('profile.settings.email_notifications') }}</h3>
              <p class="text-sm text-neutral-500 dark:text-neutral-400">
                {{ t('profile.settings.email_notifications_desc') }}
              </p>
            </div>
            <label class="inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="user.settings.emailNotifications" class="sr-only peer">
              <div class="relative w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-neutral-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-neutral-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between py-2 border-t border-neutral-200 dark:border-neutral-700">
            <div>
              <h3 class="font-medium">{{ t('profile.settings.dark_mode') }}</h3>
              <p class="text-sm text-neutral-500 dark:text-neutral-400">
                {{ t('profile.settings.dark_mode_desc') }}
              </p>
            </div>
            <label class="inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="user.settings.darkMode" class="sr-only peer">
              <div class="relative w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-neutral-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-neutral-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
          
          <div class="py-2 border-t border-neutral-200 dark:border-neutral-700">
            <h3 class="font-medium mb-2">{{ t('profile.settings.language') }}</h3>
            <select v-model="user.settings.defaultLanguage" class="input">
              <option value="en">English</option>
              <option value="de">Deutsch</option>
            </select>
          </div>
          
          <div class="pt-4 flex justify-end border-t border-neutral-200 dark:border-neutral-700">
            <button class="btn btn-primary" @click="updateProfile">
              {{ t('profile.save_settings') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>