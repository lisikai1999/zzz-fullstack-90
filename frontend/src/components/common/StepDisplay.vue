<template>
  <div class="step-display">
    <div
      v-for="(step, idx) in steps"
      :key="idx"
      class="step-card"
      :class="{ active: idx === currentStep, completed: idx < currentStep }"
    >
      <el-card shadow="never">
        <template #header>
          <div class="step-header">
            <el-tag :type="idx === currentStep ? 'primary' : idx < currentStep ? 'success' : 'info'" size="small">
              {{ step.step_number || idx + 1 }}
            </el-tag>
            <span class="step-title">{{ step.title }}</span>
          </div>
        </template>
        <div v-if="idx <= currentStep">
          <div class="math-expr">{{ step.expression }}</div>
          <p v-if="step.explanation" class="step-explanation">{{ step.explanation }}</p>
          <div v-if="step.intermediate_value != null" class="intermediate">
            结果: <strong>{{ step.intermediate_value }}</strong>
          </div>
          <el-collapse v-if="step.sub_steps && step.sub_steps.length" class="sub-steps">
            <el-collapse-item title="展开详细步骤">
              <div v-for="(sub, si) in step.sub_steps" :key="si" class="sub-step">
                <code>{{ sub.expression }}</code>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
defineProps({
  steps: { type: Array, required: true },
  currentStep: { type: Number, default: 999 },
})
</script>

<style scoped>
.step-header {
  display: flex;
  align-items: center;
  gap: 8px;
}
.step-title {
  font-weight: 600;
}
.step-explanation {
  margin-top: 8px;
  color: #606266;
  font-size: 13px;
}
.intermediate {
  margin-top: 8px;
  padding: 4px 8px;
  background: #f0f9eb;
  border-radius: 4px;
  font-family: monospace;
}
.sub-steps {
  margin-top: 8px;
}
.sub-step {
  padding: 4px 0;
  font-size: 13px;
}
</style>
