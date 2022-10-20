import axios from 'axios'
import { Message } from 'element-ui'
// import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API
})
// 请求拦截器
service.interceptors.request.use(
  config => {
    // 存储token
    let token = getToken()
    if (token) {
      token = `bearer ${token}`
      config.headers['Authorization'] = token
    }
    return config
  },
  error => {
    // 请求错误时返回
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// 相应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    // 如果返回等于200
    if (res.success === true) {
      return response
    } else {
      return response
    }
  },
  error => {
    console.log('err' + error)
    // 如果返回等于402或401
    if (error.response.data.status === 402 || error.response.data.status === 401) {
      Message.error(new Error('token失效'))
      this.$router.push({ path: '/login' })
    }
    return Promise.reject(error)
  }
)

export default service
