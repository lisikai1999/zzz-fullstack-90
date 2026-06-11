import { ref, onUnmounted } from 'vue'

export function useAnimation(totalSteps, speed = ref(1)) {
  const currentStep = ref(0)
  const isPlaying = ref(false)
  let timer = null

  function play() {
    if (currentStep.value >= totalSteps.value - 1) {
      currentStep.value = 0
    }
    isPlaying.value = true
    scheduleNext()
  }

  function pause() {
    isPlaying.value = false
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
  }

  function next() {
    if (currentStep.value < totalSteps.value - 1) {
      currentStep.value++
    } else {
      pause()
    }
  }

  function prev() {
    if (currentStep.value > 0) {
      currentStep.value--
    }
  }

  function reset() {
    pause()
    currentStep.value = 0
  }

  function scheduleNext() {
    if (!isPlaying.value) return
    timer = setTimeout(() => {
      if (currentStep.value < totalSteps.value - 1) {
        currentStep.value++
        scheduleNext()
      } else {
        isPlaying.value = false
      }
    }, 1000 / speed.value)
  }

  onUnmounted(() => {
    if (timer) clearTimeout(timer)
  })

  return { currentStep, isPlaying, play, pause, next, prev, reset }
}
