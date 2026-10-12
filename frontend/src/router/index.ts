import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Home'
      }
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue'),
      meta: {
        title: 'Literature Search'
      }
    },
    {
      path: '/results',
      name: 'results',
      component: () => import('../views/ResultsView.vue'),
      meta: {
        title: 'Search Results'
      }
    },
    {
      path: '/Assistant',
      name: 'Assistant',
      component: () => import('../views/AssistantChat.vue'),
      meta: {
        title: 'Assistant'
      }
    },
    {
      path: '/document/:id',
      name: 'document',
      component: () => import('../views/DocumentView.vue'),
      meta: {
        title: 'Document View'
      }
    },
    {
      path: '/collection',
      name: 'collection',
      component: () => import('../views/CollectionView.vue'),
      meta: {
        title: 'My Collection'
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: {
        title: 'User Profile'
      }
    },
    // 404 catch-all route
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: {
        title: '404 Not Found'
      }
    }
    
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Update page title
router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title} | ML-Assisted Literature Research`
  next()
})

export default router