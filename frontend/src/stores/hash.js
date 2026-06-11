import { defineStore } from 'pinia'
import { computeHash, startBirthdayAttack, getAttackProgress, getAttackResult } from '../api/hash'

export const useHashStore = defineStore('hash', {
  state: () => ({
    message: 'Hello',
    hashBits: 16,
    hashResult: null,
    attackTaskId: null,
    attackProgress: null,
    attackResult: null,
    loading: false,
    error: null,
  }),
  actions: {
    async doComputeHash() {
      this.loading = true
      this.error = null
      try {
        const res = await computeHash(this.message, this.hashBits)
        this.hashResult = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async doStartAttack() {
      this.error = null
      this.attackResult = null
      this.attackProgress = null
      try {
        const res = await startBirthdayAttack(this.hashBits)
        this.attackTaskId = res.data.task_id
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      }
    },
    async pollProgress() {
      if (!this.attackTaskId) return
      try {
        const res = await getAttackProgress(this.attackTaskId)
        this.attackProgress = res.data
        if (res.data.status === 'complete') {
          const result = await getAttackResult(this.attackTaskId)
          this.attackResult = result.data
        }
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      }
    },
  },
})
