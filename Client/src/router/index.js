import { createRouter, createWebHistory } from 'vue-router'
import { user } from '../stores/user.js'
import axios from 'axios'
import { loadingBar } from '../stores/loading.js'
import { alertStore } from '@/stores/alert.js'

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
      beforeEnter: (to, from, next) => {
        let userData = user()
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/verifyUser',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        }

        axios
          .request(config)
          .then(() => {
            loadingBar.loading = false
            next('/logout')
          })
          .catch(() => {
            loadingBar.loading = false
            next()
          })
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      beforeEnter: (to, from, next) => {
        let userData = user()
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/verifyUser',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        }
        axios
          .request(config)
          .then(() => {
            next()
          })
          .catch(() => {
            next('/login')
          })
      }
    },
    {
      path: '/event/:id',
      name: 'event',
      component: () => import('../views/EventView.vue'),
      beforeEnter: (to, from, next) => {
        let config = {
          method: 'get',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/event/isEvent?event_id=' + to.params.id
        }
        axios
          .request(config)
          .then((response) => {
            if (response.data['is_event'] === false) {
              next('/404')
            } else {
              next()
            }
          })
          .catch(() => {
            next('/404')
          })
      }
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
      path: '/logout',
      name: 'logout',
      component: () => import('../views/LogoutView.vue')
    },
    {
      path: '/createItem',
      name: 'createItem',
      component: () => import('../views/ItemCreateView.vue'),
      beforeEnter: (to, from, next) => {
        let userData = user()
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/verifyUser',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        }

        axios
          .request(config)
          .then(() => {
            next()
          })
          .catch(() => {
            alertStore.showInfo('You must be an admin to access that page', 'Access Error', true)
            next('/')
          })
      }
    },
    {
      path: '/createNotification',
      name: 'createNotification',
      component: () => import('../views/NotificationView.vue'),
      beforeEnter: (to, from, next) => {
        let userData = user()
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/verifyUser',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        }
        axios
          .request(config)
          .then(() => {
            next()
          })
          .catch(() => {
            alertStore.showInfo('You must be an admin to access that page', 'Access Error', true)
            next('/')
          })
          .catch(() => {
            next('/')
          })
      }
    },
    {
      path: '/eventManagement',
      name: 'eventManagement',
      component: () => import('../views/EventManagement.vue'),
      beforeEnter: (to, from, next) => {
        let userData = user()
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/verifyUser',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        }

        axios
          .request(config)
          .then(() => {
            next()
          })
          .catch(() => {
            alertStore.showInfo('You must be an admin to access that page', 'Access Error', true)
            next('/')
          })
      }
    },
    {
      path: '/pledge',
      name: 'pledge',
      component: () => import('../views/PledgeView.vue'),
      beforeEnter: (to, from, next) => {
        let userData = user()
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/verifyDonor',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        }
        axios
          .request(config)
          .then(() => {
            console.log(userData.getToken)
            next()
          })
          .catch(() => {
            alertStore.showInfo('You must be a donor to access that page', 'Access Error', true)
            next('/')
          })
      }
    },
    {
      path: '/forgotPassword',
      name: 'forgotPassword',
      component: () => import('../views/ForgotPasswordView.vue')
    },
    {
      path: '/match',
      name: 'match',
      component: () => import('../views/PledgeMatcherView.vue'),
      beforeEnter: (to, from, next) => {
        let userData = user()
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/users_bp/verifyUser',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          }
        }

        axios
          .request(config)
          .then(() => {
            next()
          })
          .catch(() => {
            alertStore.showInfo('You must be an admin to access that page', 'Access Error', true)
            next('/')
          })
      }
    },
    {
      path: '/notificationsList',
      name: 'notificationsList',
      component: () => import('../views/NotificationListView.vue')
    },
    {
      path: '/:catchAll(.*)',
      name: '404',
      component: () => import('../views/NotFoundView.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  loadingBar.loading = true
  scroll(0, 0)
  if (alertStore.overRide) {
    alertStore.overRide = false
    next()
  } else {
    alertStore.display = false
    next()
  }
})

router.afterEach(() => {
  loadingBar.loading = false
})

export default router
