import router from './router'
import store from './store'
import {
  Message
} from 'element-ui'
import {
  getToken
} from '@/utils/auth' // 验权

const whiteList = ['/login', '/register'] // 不重定向白名单
router.beforeEach((to, from, next) => {
  if (getToken()) {
    if (to.path === '/login' || to.path == '/register') {
      next({
        path: '/'
      })
    } else {
      Web3Helper.isNetworkConnected();
      Web3Helper.isMetaMaskLogin();

      next()

    }
  } else {
    if (whiteList.indexOf(to.path) !== -1 || to.path.indexOf('/taskDetail') !== -1) {
      next()
    } else {
      next('/login')

    }
  }
})

router.afterEach((to, from, next) => {
  // 结束Progress
  window.scrollTo(0, 0);
})