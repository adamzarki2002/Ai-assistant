<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="py-12 px-4 sm:px-6 md:py-20 md:px-8">
    <div class="max-w-md mx-auto text-center">
      <h1 class="text-9xl font-bold text-primary-600 dark:text-primary-400">404</h1>
      <p class="mt-4 text-3xl font-bold tracking-tight text-neutral-900 dark:text-neutral-100">
        {{ t('not_found.title') }}
      </p>
      <p class="mt-4 text-base text-neutral-600 dark:text-neutral-400">
        {{ t('not_found.message') }}
      </p>
      <div class="mt-10">
        <router-link to="/" class="btn btn-primary">
          {{ t('not_found.go_home') }}
        </router-link>
      </div>
    </div>
  </div>
</template>