import { defineStore } from 'pinia'
import { generateKeys, encrypt, decrypt } from '../api/rsa'

export const useRsaStore = defineStore('rsa', {
  state: () => ({
    p: 61,
    q: 53,
    e: 17,
    keyGenResult: null,
    encryptResult: null,
    decryptResult: null,
    loading: false,
    error: null,
  }),
  actions: {
    async doGenerateKeys() {
      this.loading = true
      this.error = null
      try {
        const res = await generateKeys(this.p, this.q, this.e || null)
        this.keyGenResult = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async doEncrypt(message) {
      this.loading = true
      this.error = null
      try {
        const { e, n } = this.keyGenResult.public_key
        const res = await encrypt(message, e, n)
        this.encryptResult = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async doDecrypt(ciphertext) {
      this.loading = true
      this.error = null
      try {
        const { d, n } = this.keyGenResult.private_key
        const res = await decrypt(ciphertext, d, n)
        this.decryptResult = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
  },
})
