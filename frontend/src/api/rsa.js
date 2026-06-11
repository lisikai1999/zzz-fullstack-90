import api from './index'

export function generateKeys(p, q, e = null) {
  return api.post('/rsa/generate-keys', { p, q, e })
}

export function encrypt(message, e, n) {
  return api.post('/rsa/encrypt', { message, e, n })
}

export function decrypt(ciphertext, d, n) {
  return api.post('/rsa/decrypt', { ciphertext, d, n })
}
