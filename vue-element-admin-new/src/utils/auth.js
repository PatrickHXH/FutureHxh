import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'
const UserKey = 'username'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function setName(usename) {
  return Cookies.set(UserKey, usename)
}

export function getName() {
  return Cookies.get(UserKey)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
