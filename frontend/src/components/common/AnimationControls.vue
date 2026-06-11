<template>
  <div class="animation-controls">
    <el-button-group>
      <el-button :icon="DArrowLeft" @click="$emit('reset')" :disabled="disabled" />
      <el-button :icon="ArrowLeft" @click="$emit('prev')" :disabled="disabled || currentStep <= 0" />
      <el-button
        :icon="isPlaying ? VideoPause : VideoPlay"
        @click="isPlaying ? $emit('pause') : $emit('play')"
        :disabled="disabled"
        type="primary"
      />
      <el-button :icon="ArrowRight" @click="$emit('next')" :disabled="disabled || currentStep >= totalSteps - 1" />
    </el-button-group>
    <span class="step-indicator">
      步骤 {{ currentStep + 1 }} / {{ totalSteps }}
    </span>
    <el-slider
      v-model="speedValue"
      :min="0.5"
      :max="4"
      :step="0.5"
      :format-tooltip="v => v + 'x'"
      style="width: 120px"
      @change="$emit('speed-change', $event)"
    />
    <span class="speed-label">速度</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { VideoPlay, VideoPause, ArrowLeft, ArrowRight, DArrowLeft } from '@element-plus/icons-vue'

defineProps({
  currentStep: { type: Number, default: 0 },
  totalSteps: { type: Number, default: 1 },
  isPlaying: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
})

defineEmits(['play', 'pause', 'next', 'prev', 'reset', 'speed-change'])

const speedValue = ref(1)
</script>

<style scoped>
.step-indicator {
  font-size: 13px;
  color: #606266;
  min-width: 90px;
}
.speed-label {
  font-size: 12px;
  color: #909399;
}
</style>
