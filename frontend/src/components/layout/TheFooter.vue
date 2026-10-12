<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <footer class="bg-white dark:bg-neutral-800 border-t border-neutral-200 dark:border-neutral-700 py-4 px-4 sm:px-6">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
      <div class="mb-4 md:mb-0">
        <p class="text-sm text-neutral-500 dark:text-neutral-400">
          &copy; {{ new Date().getFullYear() }} {{ t('footer.copyright') }}
        </p>
      </div>
      
      <div class="flex space-x-6">
        <a 
          href="#" 
          class="text-sm text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors duration-200"
        >
          {{ t('footer.terms') }}
        </a>
        <a 
          href="#" 
          class="text-sm text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors duration-200"
        >
          {{ t('footer.privacy') }}
        </a>
        <a 
          href="#" 
          class="text-sm text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white transition-colors duration-200"
        >
          {{ t('footer.about') }}
        </a>
      </div>
    </div>
  </footer>
</template>