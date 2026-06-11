import { ref, onUnmounted } from 'vue'

export function usePolling(fetchFn, interval = 500) {
  const data = ref(null)
  const isPolling = ref(false)
  let timer = null

  async function start() {
    isPolling.value = true
    await poll()
  }

  async function poll() {
    if (!isPolling.value) return
    try {
      data.value = await fetchFn()
    } catch (e) {
      stop()
      return
    }
    if (isPolling.value) {
      timer = setTimeout(poll, interval)
    }
  }

  function stop() {
    isPolling.value = false
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
  }

  onUnmounted(stop)

  return { data, isPolling, start, stop }
}
