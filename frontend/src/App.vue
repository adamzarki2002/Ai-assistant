<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import TheNavbar from './components/layout/TheNavbar.vue'
import TheSidebar from './components/layout/TheSidebar.vue'
import TheFooter from './components/layout/TheFooter.vue'

const isSidebarOpen = ref(true)
const route = useRoute()

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

// Close sidebar automatically on mobile when route changes
watch(
  () => route.path,
  () => {
    if (window.innerWidth < 768) {
      isSidebarOpen.value = false
    }
  }
)
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <TheNavbar @toggle-sidebar="toggleSidebar" />
    
    <div class="flex flex-1 overflow-hidden">
      <TheSidebar :is-open="isSidebarOpen" />
      
      <main 
        class="flex-1 overflow-y-auto p-4 md:p-6 transition-all duration-300"
        :class="{ 'md:ml-64': isSidebarOpen }"
      >
        <div class="max-w-7xl mx-auto">
          <router-view v-slot="{ Component }">
            <transition 
              name="page" 
              mode="out-in"
              enter-active-class="transition-opacity duration-300"
              enter-from-class="opacity-0"
              enter-to-class="opacity-100"
              leave-active-class="transition-opacity duration-200"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
    
    <TheFooter />
  </div>
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>