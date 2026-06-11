import api from './index'

export function computeHash(message, hashBits = 16) {
  return api.post('/hash/compute', { message, hash_bits: hashBits })
}

export function startBirthdayAttack(hashBits = 16) {
  return api.post('/hash/birthday-attack/start', { hash_bits: hashBits })
}

export function getAttackProgress(taskId) {
  return api.get(`/hash/birthday-attack/${taskId}/progress`)
}

export function getAttackResult(taskId) {
  return api.get(`/hash/birthday-attack/${taskId}/result`)
}

export function cancelAttack(taskId) {
  return api.delete(`/hash/birthday-attack/${taskId}`)
}
