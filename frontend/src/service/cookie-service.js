import Cookies from 'js-cookie'

export const setCookie = function(name, value) {
  Cookies.set(name, value)
}

export const getCookie = function(name) {
  return Cookies.get(name)
}
