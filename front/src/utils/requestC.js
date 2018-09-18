import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import store from '../store'
import { getToken } from '@/utils/auth'

const service = axios.create({
   baseURL: process.env.BASE_API,
  timeout: 15000
})
const getTimestamp = new Date().getTime();
service.interceptors.request.use(config => {
  if (store.getters.token) {
    config.headers['client_name'] = 'jwt';
    // config.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
    config.headers['token'] = getToken(); // 让每个请求携带自定义token 请根据实际情况自行修改
    config.url += "?timestamp="+getTimestamp;;
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
   if (res.errorCode == '2000') {
      Message({
        message: '服务器打盹了，请稍后再试',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100000') {
      Message({
        message: '您没有权限执行此操作',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100002') {
      Message({
        message: '储存文件错误',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100002') {
      Message({
        message: '储存文件错误',
        type: 'error',
        duration: 5 * 1000
      })
    }

    else if (res.errorCode == '100005') {
      Message({
        message: '数据重复了',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100006') {
      Message({
        message: '储存信息失败',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100007') {
      Message({
        message: '修改信息失败',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100009') {
      Message({
        message: '审核中，不能修改信息',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100010') {
      Message({
        message: '获取github头像失败',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100014') {
      Message({
        message: '主节点申请通过才能进行绑定',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100015') {
      Message({
        message: '赏金任务信息不存在',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100016') {
      Message({
        message: '获取公共的用户信息出错',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100018') {
      Message({
        message: '获取用户列表信息失败',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100019') {
      Message({
        message: '此状态下不能进行此操作',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100020') {
      Message({
        message: '敏感词校验不通过',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100021') {
      Message({
        message: res.errorMsg,
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100022') {
      Message({
        message: '此用户不是主节点用户',
        type: 'error',
        duration: 5 * 1000
      })
    } 
    else if (res.errorCode == '100023') {
      Message({
        message: '此提案名称已存在',
        type: 'error',
        duration: 5 * 1000
      })
    } 
    else if (res.errorCode == '100025') {
      Message({
        message: '此交易ID已存在',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100026') {
      Message({
        message: '此交易ID对应的数据值错误',
        type: 'error',
        duration: 5 * 1000
      })
    }
    else if (res.errorCode == '100027') {
      Message({
        message: '本期提案已经进入结算时间，请等待结算完成后再进行提交',
        type: 'error',
        duration: 5 * 1000
      })
    } 
    else if (res.errorCode == '100028') {
      Message({
        message: '此提案还未通过审核，请等待审核通过后再次进行操作',
        type: 'error',
        duration: 5 * 1000
      })
    } 
    else if (res.errorCode == '100029') {
      Message({
        message: '此提案未通过审核',
        type: 'error',
        duration: 5 * 1000
      })
    } 
    else {
      return res
    }
  },
  error => {
    Message({
      message: '服务器打盹了，请稍后再试',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service