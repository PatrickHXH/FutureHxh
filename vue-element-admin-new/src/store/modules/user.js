import { login, logout, getInfo, getMenu } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router, { resetRouter } from '@/router'
import Layout from '@/layout'
import { Message } from 'element-ui'

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
        Message.error('无法登录')
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
        // result.map(i => {
        //   i.component = Layout
        //   i.meta = {
        //     'title': i.title,
        //     'icon': i.icon
        //   }
        //   i.name = i.title
        //   i.hidden = i.hidden
        //   i.children.map(j => {
        //     const cmp1 = j.cmp
        //     j.component = resolve => require([`@/views${cmp1}`], resolve)
        //     j.name = j.title
        //     j.meta = {
        //       'title': j.title,
        //       'icon': j.icon
        //     }
        //     j.hidden = j.hidden
        //     j.children.map(k => {
        //       const cmp2 = k.cmp
        //       k.name = k.title
        //       k.hidden = k.hidden
        //       k.component = resolve => require([`@/views/${cmp2}`], resolve)
        //       k.meta = {
        //         'title': k.title,
        //         'icon': k.icon
        //       }
        //     })
        //   })
        // })
        console.log("原来的节点结构:",result)
        // 读取树形结构所有节点
        function readNodes(nodes = [], arr = []) {
          for (const item of nodes) {
            if(item.parent_id ===0){
              arr.push({
                'id': item.id,
                'name':item.title,  
                'meta':{
                  'title':item.title,
                  'icon':item.icon
                },
                'path': item.path,
                'component': Layout,
                'parent_id': item.parent_id,
                'hidden': item.hidden,
                'children':[]
              })
            }else{
              arr.push({
                'id': item.id,
                'name':item.title,
                'meta':{
                  'title':item.title,
                  'icon':item.icon
                },
                'path': item.path,
                'component': resolve => require([`@/views${item.cmp}`], resolve),
                'parent_id': item.parent_id,
                'hidden': item.hidden,
                'children':[]
              })
            }

            if (item.children && item.children.length) readNodes(item.children, arr)
          }
          return arr
        }
        var all_nodes = readNodes(result)
        console.log("提取后端返回的树形节点：",all_nodes)
        
        // 递归，将子节点放入父节点，找出当前节点所有子节点并返回
        function tree_nodes(all_nodes =[], current_nodes=[]) {

          for (const i of all_nodes) {
            if (current_nodes.id === i.parent_id) {
              current_nodes.children.push(i)
              tree_nodes(all_nodes, i)
            }
          }
          return current_nodes
        }
        // 判断节点是否有子节点
        function children_node(all_nodes=[], current_nodes=[]) {
          for (const i of all_nodes) {
            if (current_nodes.id === i.parent_id) {
              return true
            }
          }
          return false
        }
        // 重新遍历树形结构组装
        const new_list = []
        for (const i of all_nodes) {
          const is_children = children_node(all_nodes, i)
          if (i.parent_id === 0 && is_children === false) {
            new_list.push(i)
          }
          if (i.parent_id === 0 && is_children === true) {
            const ret = tree_nodes(all_nodes, i)
            new_list.push(ret)
          }
        }
        console.log('重新遍历的节点', new_list)
        resolve(new_list)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // dynamically modify permissions
  // async changeRoles({ commit, dispatch }, role) {
  //   const token = state.token

  //   commit('SET_TOKEN', token)
  //   setToken(token)

  //   const { roles } = await dispatch('getInfo')

  //   resetRouter()

  //   // generate accessible routes map based on roles
  //   const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })
  //   // dynamically add accessible routes
  //   router.addRoutes(accessRoutes)

  //   // reset visited views and cached views
  //   dispatch('tagsView/delAllViews', null, { root: true })
  // }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
