import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/users/login',
    method: 'post',
    data
  })
}

export function getInfo(data) {
  return request({
    url: '/api/users/getinfo/',
    method: 'post',
    data
  })
}

export function logout(data) {
  return request({
    url: '/api/users/logout/',
    method: 'post',
    data
  })
}

