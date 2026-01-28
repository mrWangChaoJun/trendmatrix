import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory('/trendmatrix/'),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/dashboard/DashboardView.vue'),
      meta: {
        title: '仪表盘',
        requiresAuth: false
      }
    },
    {
      path: '/signals',
      name: 'signals',
      component: () => import('../views/signals/SignalsView.vue'),
      meta: {
        title: '信号系统',
        requiresAuth: false
      }
    },
    {
      path: '/signals/history',
      name: 'signalHistory',
      component: () => import('../views/signals/SignalHistoryView.vue'),
      meta: {
        title: '信号历史',
        requiresAuth: false
      }
    },
    {
      path: '/signals/:id',
      name: 'signalDetail',
      component: () => import('../views/signals/SignalDetailView.vue'),
      meta: {
        title: '信号详情',
        requiresAuth: false
      }
    },
    {
      path: '/solana',
      name: 'solana',
      component: () => import('../views/solana/SolanaView.vue'),
      meta: {
        title: 'Solana 生态分析',
        requiresAuth: false
      }
    },
    {
      path: '/solana/project/:id',
      name: 'solanaProject',
      component: () => import('../views/solana/SolanaProjectView.vue'),
      meta: {
        title: '项目分析',
        requiresAuth: false
      }
    },
    {
      path: '/solana/nft',
      name: 'solanaNft',
      component: () => import('../views/solana/SolanaNftView.vue'),
      meta: {
        title: 'NFT 市场分析',
        requiresAuth: false
      }
    },
    {
      path: '/solana/defi',
      name: 'solanaDefi',
      component: () => import('../views/solana/SolanaDefiView.vue'),
      meta: {
        title: 'DeFi 协议分析',
        requiresAuth: false
      }
    },
    {
      path: '/subscription/plans',
      name: 'subscriptionPlans',
      component: () => import('../views/subscription/SubscriptionPlansView.vue'),
      meta: {
        title: '订阅计划',
        requiresAuth: false
      }
    },
    {
      path: '/subscription/my',
      name: 'mySubscription',
      component: () => import('../views/subscription/MySubscriptionView.vue'),
      meta: {
        title: '我的订阅',
        requiresAuth: false
      }
    },
    {
      path: '/payment/methods',
      name: 'paymentMethods',
      component: () => import('../views/payment/PaymentMethodsView.vue'),
      meta: {
        title: '支付方式',
        requiresAuth: false
      }
    },
    {
      path: '/payment/history',
      name: 'paymentHistory',
      component: () => import('../views/payment/PaymentHistoryView.vue'),
      meta: {
        title: '支付历史',
        requiresAuth: false
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/settings/SettingsView.vue'),
      meta: {
        title: '系统设置',
        requiresAuth: false
      }
    },
    {
      path: '/auth/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: {
        title: '登录',
        requiresAuth: false
      }
    },
    {
      path: '/auth/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: {
        title: '注册',
        requiresAuth: false
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/common/NotFoundView.vue'),
      meta: {
        title: '页面不存在'
      }
    }
  ]
})

// 全局前置守卫，设置页面标题
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || 'TrendMatrix'} - TrendMatrix`

  // 不需要认证检查，直接允许所有页面访问
  next();
})

export default router
