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
    console.log("111",error) // for debug
    return Promise.reject(error)
  }
)

// 响应拦截器
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
    console.log(error.response)
    if (error.response.status === 403) {
      Message.error(error.response.data.detail)
    }
    // 如果返回等于402或401
    if (error.response.status === 402 || error.response.data.status === 401) {
      Message.error(error.response.data.detail)
      // this.$router.push({ path: '/login' })
      window.location.href='/'
    }
    return Promise.reject(error)
  }
)

export default service
