<script setup lang="ts">
defineProps<{
  title: string
  value: string
  icon: string
  color: 'primary' | 'secondary' | 'accent'
}>()

const getColorClass = (color: string) => {
  const colorMap = {
    primary: 'text-primary-600 dark:text-primary-400',
    secondary: 'text-secondary-500 dark:text-secondary-400',
    accent: 'text-accent-300 dark:text-accent-300'
  }
  return colorMap[color as keyof typeof colorMap] || colorMap.primary
}
</script>

<template>
  <div class="card flex items-center hover:shadow-md transition-shadow duration-300">
    <div class="mr-4 p-3 rounded-full" :class="[`bg-${color}-50 dark:bg-${color}-900/20`, getColorClass(color)]">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-8 w-8">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="icon"></path>
      </svg>
    </div>
    <div>
      <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ title }}</p>
      <p class="text-2xl font-bold" :class="getColorClass(color)">{{ value }}</p>
    </div>
  </div>
</template>