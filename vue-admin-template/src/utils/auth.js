import Cookies from 'js-cookie'

const TokenKey = 'vue_admin_token'
const UserKey="username"

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function setName(usename) {
  return Cookies.set(UserKey, usename)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
