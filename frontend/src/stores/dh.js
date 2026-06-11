import { defineStore } from 'pinia'
import { dhExchange, dhMitm, colorMixing } from '../api/dh'

export const useDhStore = defineStore('dh', {
  state: () => ({
    p: 23,
    g: 5,
    aPrivate: 6,
    bPrivate: 15,
    mPrivate: 9,
    aliceColor: '#ff0000',
    bobColor: '#0000ff',
    commonColor: '#ffff00',
    exchangeResult: null,
    mitmResult: null,
    colorResult: null,
    loading: false,
    error: null,
  }),
  actions: {
    async doExchange() {
      this.loading = true
      this.error = null
      try {
        const res = await dhExchange(this.p, this.g, this.aPrivate, this.bPrivate)
        this.exchangeResult = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async doMitm() {
      this.loading = true
      this.error = null
      try {
        const res = await dhMitm(this.p, this.g, this.aPrivate, this.bPrivate, this.mPrivate)
        this.mitmResult = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async doColorMixing() {
      this.loading = true
      this.error = null
      try {
        const res = await colorMixing(this.aliceColor, this.bobColor, this.commonColor)
        this.colorResult = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
  },
})
