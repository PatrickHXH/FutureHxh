import { login, logout, getInfo, getMenu } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router, { resetRouter } from '@/router'
import Layout from '@/layout'

const state = {
  token: getToken(),
  name: '',
  avatar: '',
  introduction: '',
  roles: []
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_INTRODUCTION: (state, introduction) => {
    state.introduction = introduction
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response // 等价于const data = response.data
        commit('SET_TOKEN', data.result.token)
        setToken(data.result.token)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo({ token: state.token }).then(response => {
        const { data } = response
        console.log('获取用户信息对象：', data.result)
        if (!data) {
          reject('Verification failed, please Login again.')
        }
        const { roles, username, checkout } = data.result
        console.log(roles, username, checkout)
        commit('SET_INTRODUCTION', 'I am a super administrator')
        commit('SET_ROLES', roles)
        commit('SET_NAME', username)
        commit('SET_AVATAR', checkout)
        resolve(data.result)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout({ username: state.name }).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      resolve()
    })
  },

  // get Menu
  getMenu({ commit, state }) {
    return new Promise((resolve, reject) => {
      getMenu({ token: state.token }).then(response => {
        const { result } = response.data
        result.map(i => {
          i.component = Layout
          i.meta = {
            'title': i.title,
            'icon': i.icon
          }
          i.name = i.title
          i.hidden = i.hidden
          i.children.map(j => {
            const cmp1 = j.cmp
            j.component = resolve => require([`@/views${cmp1}`], resolve)
            j.name = j.title
            j.meta = {
              'title': j.title,
              'icon': j.icon
            }
            j.hidden = j.hidden
            j.children.map(k => {
              const cmp2 = k.cmp
              k.name = k.title
              k.hidden = k.hidden
              k.component = resolve => require([`@/views/${cmp2}`], resolve)
              k.meta = {
                'title': k.title,
                'icon': k.icon
              }
            })
          })
        })
        // console.log('遍历后的菜单：', result, typeof (result))
        
      function readNodes (nodes = [], arr = []) {
        for (let item of nodes) {
            arr.push({
              "id":item.id,
              "children":item.children
            })
            if (item.children && item.children.length) readNodes(item.children, arr)
        }
        return arr
      }
      console.log("测试遍历树形结构",readNodes(result))
        resolve(result)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // dynamically modify permissions
  async changeRoles({ commit, dispatch }, role) {
    const token = state.token

    commit('SET_TOKEN', token)
    setToken(token)

    const { roles } = await dispatch('getInfo')

    resetRouter()

    // generate accessible routes map based on roles
    const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })
    // dynamically add accessible routes
    router.addRoutes(accessRoutes)

    // reset visited views and cached views
    dispatch('tagsView/delAllViews', null, { root: true })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
