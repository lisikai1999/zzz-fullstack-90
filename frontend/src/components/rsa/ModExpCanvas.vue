<template>
  <div class="canvas-container">
    <canvas ref="canvas" :width="width" :height="height"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'

const props = defineProps({
  steps: { type: Array, default: () => [] },
  currentStep: { type: Number, default: 0 },
  width: { type: Number, default: 700 },
  height: { type: Number, default: 320 },
})

const canvas = ref(null)

const animProgress = ref(1)
let animFrame = null

watch(() => props.currentStep, (newVal, oldVal) => {
  animProgress.value = 0
  animateTransition()
})

onMounted(() => draw())
watch([() => props.steps, animProgress], () => draw())

function animateTransition() {
  if (animFrame) cancelAnimationFrame(animFrame)
  const start = performance.now()
  const duration = 400
  function tick(now) {
    const t = Math.min((now - start) / duration, 1)
    animProgress.value = easeOut(t)
    if (t < 1) {
      animFrame = requestAnimationFrame(tick)
    }
  }
  animFrame = requestAnimationFrame(tick)
}

function easeOut(t) {
  return 1 - Math.pow(1 - t, 3)
}

function draw() {
  const ctx = canvas.value?.getContext('2d')
  if (!ctx || !props.steps.length) return
  const w = props.width
  const h = props.height

  ctx.clearRect(0, 0, w, h)

  const step = props.steps[props.currentStep]
  if (!step) return

  // Find the init step to get binary representation
  const initStep = props.steps.find(s => s.operation === 'init')
  const binary = initStep?.expression?.match(/= ([01]+)/)?.[1] || ''

  // Draw binary bits at top
  const bitY = 40
  const bitW = 40
  const totalBitWidth = binary.length * bitW
  const bitStartX = (w - totalBitWidth) / 2

  ctx.font = '12px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillStyle = '#666'
  ctx.fillText('指数二进制表示', w / 2, 16)

  for (let i = 0; i < binary.length; i++) {
    const x = bitStartX + i * bitW
    const bitIdx = i + 1 // steps after init correspond to bits
    const isActive = props.currentStep === bitIdx
    const isDone = props.currentStep > bitIdx

    ctx.fillStyle = isActive ? '#409eff' : isDone ? '#67c23a' : '#ebeef5'
    ctx.strokeStyle = isActive ? '#409eff' : isDone ? '#67c23a' : '#dcdfe6'
    ctx.lineWidth = isActive ? 2 : 1

    roundRect(ctx, x + 4, bitY - 14, bitW - 8, 28, 6)
    ctx.fill()
    ctx.stroke()

    ctx.fillStyle = isActive || isDone ? '#fff' : '#606266'
    ctx.font = `${isActive ? 'bold ' : ''}14px monospace`
    ctx.fillText(binary[i], x + bitW / 2, bitY + 4)
  }

  // Draw current operation visualization
  const opY = 110
  ctx.font = '13px sans-serif'
  ctx.textAlign = 'left'
  ctx.fillStyle = '#303133'

  if (step.operation === 'init') {
    ctx.textAlign = 'center'
    ctx.font = '16px sans-serif'
    ctx.fillStyle = '#409eff'
    ctx.fillText('准备：将指数转为二进制，从高位开始逐位处理', w / 2, opY)
    ctx.font = '24px monospace'
    ctx.fillStyle = '#303133'
    ctx.fillText(`${binary}₂`, w / 2, opY + 40)
  } else {
    const isSqMul = step.operation === 'square_and_multiply'
    const isSq = step.operation === 'square'

    // Operation label
    ctx.textAlign = 'center'
    ctx.font = 'bold 14px sans-serif'
    ctx.fillStyle = isSqMul ? '#e6a23c' : '#409eff'
    ctx.fillText(
      isSqMul ? '平方 → 再乘底数' : '仅平方',
      w / 2, opY - 10
    )

    // Value boxes animation
    const prevStep = props.steps[props.currentStep - 1]
    const prevVal = prevStep?.intermediate_value ?? 1
    const curVal = step.intermediate_value

    // Previous value -> operation -> new value
    const boxW = 100
    const boxH = 50
    const gap = 80

    // Left box: previous value
    const lx = w / 2 - boxW - gap
    ctx.fillStyle = '#f5f7fa'
    ctx.strokeStyle = '#dcdfe6'
    ctx.lineWidth = 1
    roundRect(ctx, lx, opY, boxW, boxH, 8)
    ctx.fill()
    ctx.stroke()
    ctx.fillStyle = '#606266'
    ctx.font = '12px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText('当前值', lx + boxW / 2, opY - 6)
    ctx.font = 'bold 20px monospace'
    ctx.fillStyle = '#303133'
    ctx.fillText(String(prevVal), lx + boxW / 2, opY + 32)

    // Arrow with operation label
    const arrowStartX = lx + boxW + 10
    const arrowEndX = w / 2 + gap - 10
    const arrowY = opY + boxH / 2
    ctx.strokeStyle = isSqMul ? '#e6a23c' : '#409eff'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(arrowStartX, arrowY)
    ctx.lineTo(arrowEndX * animProgress.value + arrowStartX * (1 - animProgress.value), arrowY)
    ctx.stroke()

    // Arrowhead
    if (animProgress.value > 0.8) {
      const ax = arrowEndX
      ctx.beginPath()
      ctx.moveTo(ax, arrowY)
      ctx.lineTo(ax - 8, arrowY - 5)
      ctx.lineTo(ax - 8, arrowY + 5)
      ctx.closePath()
      ctx.fillStyle = isSqMul ? '#e6a23c' : '#409eff'
      ctx.fill()
    }

    // Operation text on arrow
    ctx.font = '11px sans-serif'
    ctx.fillStyle = '#909399'
    ctx.textAlign = 'center'
    const midArrow = (arrowStartX + arrowEndX) / 2
    if (isSqMul) {
      ctx.fillText('² mod n', midArrow, arrowY - 14)
      ctx.fillText('× base mod n', midArrow, arrowY + 18)
    } else {
      ctx.fillText('² mod n', midArrow, arrowY - 10)
    }

    // Right box: new value (fades in with animation)
    const rx = w / 2 + gap
    ctx.globalAlpha = animProgress.value
    ctx.fillStyle = isSqMul ? '#fdf6ec' : '#ecf5ff'
    ctx.strokeStyle = isSqMul ? '#e6a23c' : '#409eff'
    ctx.lineWidth = 2
    roundRect(ctx, rx, opY, boxW, boxH, 8)
    ctx.fill()
    ctx.stroke()
    ctx.fillStyle = '#606266'
    ctx.font = '12px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText('新值', rx + boxW / 2, opY - 6)
    ctx.font = 'bold 20px monospace'
    ctx.fillStyle = isSqMul ? '#e6a23c' : '#409eff'
    ctx.fillText(String(curVal), rx + boxW / 2, opY + 32)
    ctx.globalAlpha = 1

    // Computation detail below
    ctx.font = '13px monospace'
    ctx.fillStyle = '#606266'
    ctx.textAlign = 'center'
    ctx.fillText(step.expression, w / 2, opY + boxH + 40)
  }

  // Progress bar at bottom
  const barY = h - 40
  const barW = w - 60
  const barH = 8
  const barX = 30
  ctx.fillStyle = '#ebeef5'
  roundRect(ctx, barX, barY, barW, barH, 4)
  ctx.fill()

  const progress = props.steps.length > 1 ? props.currentStep / (props.steps.length - 1) : 0
  ctx.fillStyle = '#409eff'
  roundRect(ctx, barX, barY, barW * progress, barH, 4)
  ctx.fill()

  ctx.font = '11px sans-serif'
  ctx.fillStyle = '#909399'
  ctx.textAlign = 'center'
  ctx.fillText(`步骤 ${props.currentStep + 1} / ${props.steps.length}`, w / 2, barY + 24)
}

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.lineTo(x + w - r, y)
  ctx.quadraticCurveTo(x + w, y, x + w, y + r)
  ctx.lineTo(x + w, y + h - r)
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
  ctx.lineTo(x + r, y + h)
  ctx.quadraticCurveTo(x, y + h, x, y + h - r)
  ctx.lineTo(x, y + r)
  ctx.quadraticCurveTo(x, y, x + r, y)
  ctx.closePath()
}
</script>
