<template>
  <div>
    <div class="canvas-container">
      <canvas ref="canvas" :width="width" :height="height"></canvas>
    </div>
    <div class="animation-controls" style="justify-content: center; margin-top: 12px">
      <el-button-group>
        <el-button @click="phase = 0">重置</el-button>
        <el-button type="primary" @click="playAll" :disabled="playing">播放动画</el-button>
      </el-button-group>
      <span style="font-size: 13px; color: #606266; margin-left: 12px">
        {{ phaseLabels[phase] || '' }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  colorResult: { type: Object, default: null },
  width: { type: Number, default: 680 },
  height: { type: Number, default: 420 },
})

const canvas = ref(null)
const phase = ref(0)
const phaseProgress = ref(1)
const playing = ref(false)
let animFrame = null

const phaseLabels = [
  '初始：展示公共颜色和私有颜色',
  '第一步：各自将私有颜色混入公共颜色',
  '第二步：通过公开信道交换混合后的颜色',
  '第三步：再各自混入自己的私有颜色',
  '完成：双方得到相同的共享颜色!',
]

onMounted(() => draw())
watch([phase, phaseProgress, () => props.colorResult], () => draw())

async function playAll() {
  playing.value = true
  phase.value = 0
  phaseProgress.value = 1
  draw()
  await sleep(800)
  for (let p = 1; p <= 4; p++) {
    phase.value = p
    await animatePhase()
    await sleep(600)
  }
  playing.value = false
}

function animatePhase() {
  return new Promise(resolve => {
    phaseProgress.value = 0
    const start = performance.now()
    const duration = 800
    function tick(now) {
      const t = Math.min((now - start) / duration, 1)
      phaseProgress.value = easeInOut(t)
      if (t < 1) {
        animFrame = requestAnimationFrame(tick)
      } else {
        resolve()
      }
    }
    animFrame = requestAnimationFrame(tick)
  })
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)) }
function easeInOut(t) { return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2,3)/2 }

function draw() {
  const ctx = canvas.value?.getContext('2d')
  if (!ctx || !props.colorResult) return
  const w = props.width
  const h = props.height
  const r = props.colorResult
  const p = phase.value
  const prog = phaseProgress.value

  ctx.clearRect(0, 0, w, h)

  const colW = w / 3
  const aliceX = colW / 2
  const channelX = w / 2
  const bobX = colW * 2 + colW / 2

  // Background columns
  ctx.fillStyle = '#fafafa'
  ctx.fillRect(0, 0, colW, h)
  ctx.fillStyle = '#f0f0f0'
  ctx.fillRect(colW, 0, colW, h)
  ctx.fillStyle = '#fafafa'
  ctx.fillRect(colW * 2, 0, colW, h)

  // Column headers
  ctx.font = 'bold 14px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillStyle = '#303133'
  ctx.fillText('Alice', aliceX, 24)
  ctx.fillText('公开信道', channelX, 24)
  ctx.fillText('Bob', bobX, 24)

  const radius = 28
  const labelOffset = radius + 18

  // Phase 0: Show initial colors
  // Private colors
  drawColorCircle(ctx, aliceX, 80, radius, r.alice.private_color, '私有色')
  drawColorCircle(ctx, bobX, 80, radius, r.bob.private_color, '私有色')

  // Common color in center
  drawColorCircle(ctx, channelX, 80, radius, r.common_color, '公共色')

  if (p >= 1) {
    // Phase 1: Mix private into common
    const mixY = 170
    const startY = 80
    const curY = startY + (mixY - startY) * (p === 1 ? prog : 1)

    // Show common color moving to both sides
    if (p === 1) {
      ctx.globalAlpha = prog
    }
    drawColorCircle(ctx, aliceX, mixY, radius, r.alice.mixed_public, '混合后')
    drawColorCircle(ctx, bobX, mixY, radius, r.bob.mixed_public, '混合后')
    ctx.globalAlpha = 1

    // Draw "+" operation indicator during animation
    if (p === 1 && prog < 1) {
      ctx.font = 'bold 20px sans-serif'
      ctx.fillStyle = '#409eff'
      ctx.fillText('+', aliceX, 130)
      ctx.fillText('+', bobX, 130)
    }
  }

  if (p >= 2) {
    // Phase 2: Exchange mixed colors through channel
    const fromY = 170
    const toY = 260

    // Alice's mixed color travels to Bob
    const aliceTravelX = aliceX + (bobX - aliceX) * (p === 2 ? prog : 1)
    const bobTravelX = bobX + (aliceX - bobX) * (p === 2 ? prog : 1)
    const travelY = fromY + (toY - fromY) * 0.5

    if (p === 2) {
      // Animate circles moving across
      ctx.globalAlpha = 0.8
      drawColorCircle(ctx, aliceTravelX, travelY + 20 * Math.sin(prog * Math.PI), radius * 0.7, r.alice.mixed_public, '')
      drawColorCircle(ctx, bobTravelX, travelY + 20 * Math.sin(prog * Math.PI), radius * 0.7, r.bob.mixed_public, '')
      ctx.globalAlpha = 1

      // Draw arrows
      ctx.strokeStyle = '#409eff'
      ctx.lineWidth = 2
      ctx.setLineDash([5, 3])
      ctx.beginPath()
      ctx.moveTo(aliceX + radius, travelY)
      ctx.lineTo(aliceX + radius + (bobX - aliceX - 2 * radius) * prog, travelY)
      ctx.stroke()
      ctx.beginPath()
      ctx.moveTo(bobX - radius, travelY + 30)
      ctx.lineTo(bobX - radius - (bobX - aliceX - 2 * radius) * prog, travelY + 30)
      ctx.stroke()
      ctx.setLineDash([])
    }

    if (p >= 3) {
      // Show received colors
      drawColorCircle(ctx, bobX, toY, radius * 0.8, r.alice.mixed_public, '收到Alice的')
      drawColorCircle(ctx, aliceX, toY, radius * 0.8, r.bob.mixed_public, '收到Bob的')
    }
  }

  if (p >= 3) {
    // Phase 3: Final mixing
    const finalY = 350

    if (p === 3) {
      ctx.globalAlpha = prog
    }

    drawColorCircle(ctx, aliceX, finalY, radius, r.alice.final_shared, '最终密钥色')
    drawColorCircle(ctx, bobX, finalY, radius, r.bob.final_shared, '最终密钥色')

    if (p === 3 && prog < 1) {
      ctx.globalAlpha = prog
      ctx.font = 'bold 18px sans-serif'
      ctx.fillStyle = '#409eff'
      ctx.fillText('+', aliceX, 310)
      ctx.fillText('+', bobX, 310)
      ctx.globalAlpha = 1
    }
    ctx.globalAlpha = 1
  }

  if (p >= 4) {
    // Phase 4: Reveal they're the same
    ctx.globalAlpha = prog
    ctx.strokeStyle = '#67c23a'
    ctx.lineWidth = 3
    ctx.setLineDash([8, 4])
    ctx.beginPath()
    ctx.moveTo(aliceX + radius + 10, 350)
    ctx.lineTo(bobX - radius - 10, 350)
    ctx.stroke()
    ctx.setLineDash([])

    ctx.font = 'bold 16px sans-serif'
    ctx.fillStyle = '#67c23a'
    ctx.fillText('= 相同!', channelX, 355)

    // Eavesdropper note
    ctx.font = '12px sans-serif'
    ctx.fillStyle = '#f56c6c'
    ctx.fillText('窃听者只能看到混合后的颜色', channelX, h - 15)
    ctx.fillText('无法分离出私有颜色!', channelX, h - 2)
    ctx.globalAlpha = 1
  }
}

function drawColorCircle(ctx, x, y, r, color, label) {
  // Shadow
  ctx.shadowColor = 'rgba(0,0,0,0.1)'
  ctx.shadowBlur = 6
  ctx.shadowOffsetY = 2

  ctx.beginPath()
  ctx.arc(x, y, r, 0, Math.PI * 2)
  ctx.fillStyle = color
  ctx.fill()
  ctx.strokeStyle = 'rgba(0,0,0,0.2)'
  ctx.lineWidth = 1
  ctx.stroke()

  ctx.shadowColor = 'transparent'
  ctx.shadowBlur = 0
  ctx.shadowOffsetY = 0

  if (label) {
    ctx.font = '10px sans-serif'
    ctx.fillStyle = '#606266'
    ctx.textAlign = 'center'
    ctx.fillText(label, x, y + r + 14)
  }
}

onUnmounted(() => {
  if (animFrame) cancelAnimationFrame(animFrame)
})
</script>
