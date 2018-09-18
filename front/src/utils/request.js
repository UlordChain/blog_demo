import axios from 'axios'
import {
  Message,
  MessageBox
} from 'element-ui'
import store from '../store'
import {
  getToken
} from '@/utils/auth'

const service = axios.create({
  baseURL: process.env.BASE_API,
  timeout: 15000
})

// request拦截器
service.interceptors.request.use(config => {
  if (store.getters.token) {
    if (config.url.indexOf('logout') !== -1) {
      return config
    }
    config.url += '?client_name=jwt&token=' + getToken();
    // config.params['client_name'] = 'jwt';
    // config.params['token'] = getToken(); // 让每个请求携带自定义token 请根据实际情况自行修改
  }
  return config
}, error => {
  // Do something with request error
  console.log(error) // for debug''
  Promise.reject(error)
})



service.interceptors.response.use(
  response => {

    const res = response.data;
    if (res.errorCode == '1007') {
      Message({
        message: '验证码错误',
        type: 'error',
        duration: 5 * 1000
      })
    } else if (res.errorCode == '1005') {
      Message({
        message: '短信请求太频繁，12小时后再试',
        type: 'error',
        duration: 5 * 1000
      })
    } else {
      return response
    }
  },
  error => {
    Message({
      message: '服务异常,请稍后再试',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service