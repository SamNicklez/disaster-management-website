import { createRouter, createWebHistory } from 'vue-router'
import { events } from '../stores/events.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      beforeEnter: () => {
        // Need to check if user is already logged in, if so redirect to profile
      },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      beforeEnter: () => {
        // Logic to check if user is logged in, please check with server before routing
        // if (localStorage.getItem('token') == null) {
        //   return '/login'
        // }
        // else {
        //   return true
        // }
      },
    },
    {
      path: '/event/:id',
      name: 'event',
      beforeEnter: (to, from, next) => {
        const eventData = events()
        let event = eventData.getEvent(to.params.id)
        if (event != null && event != undefined) {
          to.params.event = event
          next()
        } else {
          next('/notfound')
        }
      },
      component: () => import('../views/EventView.vue')
    },
    {
      path: '/donation/:id',
      name: 'donation',
      component: () => import('../views/DonationView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue')
    },
    {
      path: '/search/:query',
      name: 'search',
      component: () => import('../views/SearchView.vue')
    },
    {
      path: '/:catchAll(.*)',
      name: '404',
      component: () => import('../views/NotFoundView.vue')
    }
  ]
})

export default router
