import { login, logout, getInfo, register, getReal } from '@/api/api'
import { getToken, setToken, removeToken, setId, removeId } from '@/utils/auth'

const user = {
  state: {
    token: getToken(),
    name: '',
    avatar: '',
    real: '',
    // phone: ''
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_REAL: (state, real) => {
      state.real = real
    },
    // SET_PHONE: (state, phone) => {
    //   state.phone = phone
    // }
  },


  actions: {
    Login({ commit }, token) {
      setToken(token)
      commit('SET_TOKEN', token)
    },
    Register({ commit }, token) {
      setToken(token);
      commit('SET_TOkEN', token);
    },
    GetInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getInfo(state.token).then(response => {
          const data = response.data.result;
          commit('SET_NAME', data.username)
          commit('SET_AVATAR', data.avator)
         
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },
    GetRealName({ commit, state }) {
      return new Promise((resolve, reject) => {
        getReal().then(res => {
          if (res.errorCode !== "100003"&&res.identityDo.auditStatus == 1) {
            commit('SET_REAL', true)
            resolve(res);
          } else {
            commit('SET_REAL', false)
            resolve(res);
          }
        })
      })
    },
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    }
  }
}

export default user