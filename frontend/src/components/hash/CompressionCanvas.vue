<template>
  <div class="canvas-container">
    <canvas ref="canvas" :width="width" :height="height"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  rounds: { type: Array, default: () => [] },
  currentRound: { type: Number, default: 0 },
  width: { type: Number, default: 720 },
  height: { type: Number, default: 400 },
})

const canvas = ref(null)
const animProgress = ref(1)
let animFrame = null

watch(() => props.currentRound, () => {
  animProgress.value = 0
  animateTransition()
})

onMounted(() => draw())
watch([() => props.rounds, animProgress], () => draw())

function animateTransition() {
  if (animFrame) cancelAnimationFrame(animFrame)
  const start = performance.now()
  const duration = 500
  function tick(now) {
    const t = Math.min((now - start) / duration, 1)
    animProgress.value = easeOut(t)
    if (t < 1) animFrame = requestAnimationFrame(tick)
  }
  animFrame = requestAnimationFrame(tick)
}

function easeOut(t) { return 1 - Math.pow(1 - t, 3) }

function draw() {
  const ctx = canvas.value?.getContext('2d')
  if (!ctx || !props.rounds.length) return
  const w = props.width
  const h = props.height

  ctx.clearRect(0, 0, w, h)

  const round = props.rounds[props.currentRound]
  if (!round) return

  const regs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  const boxW = 72
  const boxH = 44
  const gap = 10
  const totalW = regs.length * (boxW + gap) - gap
  const startX = (w - totalW) / 2
  const beforeY = 60
  const afterY = 300

  // Title
  ctx.font = 'bold 14px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillStyle = '#303133'
  ctx.fillText(`第 ${round.round_number} 轮压缩`, w / 2, 20)
  ctx.font = '12px monospace'
  ctx.fillStyle = '#909399'
  ctx.fillText(`W[${round.round_number}] = ${round.W_i}  K[${round.round_number}] = ${round.K_i}`, w / 2, 38)

  // Draw "before" registers
  ctx.font = '11px sans-serif'
  ctx.fillStyle = '#909399'
  ctx.textAlign = 'center'
  ctx.fillText('压缩前状态', w / 2, beforeY - 10)

  for (let i = 0; i < regs.length; i++) {
    const x = startX + i * (boxW + gap)
    const reg = regs[i]
    const val = round.state_before[reg]
    const changed = round.state_before[reg] !== round.state_after[reg]

    ctx.fillStyle = '#f5f7fa'
    ctx.strokeStyle = '#dcdfe6'
    ctx.lineWidth = 1
    roundRect(ctx, x, beforeY, boxW, boxH, 6)
    ctx.fill()
    ctx.stroke()

    ctx.font = 'bold 11px sans-serif'
    ctx.fillStyle = '#909399'
    ctx.textAlign = 'center'
    ctx.fillText(reg.toUpperCase(), x + boxW / 2, beforeY + 14)

    ctx.font = '10px monospace'
    ctx.fillStyle = '#303133'
    ctx.fillText(val.slice(0, 4), x + boxW / 2, beforeY + 30)
    ctx.fillText(val.slice(4), x + boxW / 2, beforeY + 40)
  }

  // Draw operation boxes in the middle
  const midY = (beforeY + boxH + afterY) / 2
  const opBoxW = 80
  const opBoxH = 30

  // Sigma1 + Ch + temp1
  const ops = [
    { label: 'Σ1(e)', val: round.operations['Σ1(e)'], x: w * 0.2 },
    { label: 'Ch(e,f,g)', val: round.operations['Ch(e,f,g)'], x: w * 0.4 },
    { label: 'Σ0(a)', val: round.operations['Σ0(a)'], x: w * 0.6 },
    { label: 'Maj(a,b,c)', val: round.operations['Maj(a,b,c)'], x: w * 0.8 },
  ]

  for (const op of ops) {
    const ox = op.x - opBoxW / 2
    const oy = midY - opBoxH / 2

    ctx.globalAlpha = animProgress.value
    ctx.fillStyle = '#ecf5ff'
    ctx.strokeStyle = '#409eff'
    ctx.lineWidth = 1.5
    roundRect(ctx, ox, oy, opBoxW, opBoxH, 4)
    ctx.fill()
    ctx.stroke()

    ctx.font = '10px sans-serif'
    ctx.fillStyle = '#409eff'
    ctx.textAlign = 'center'
    ctx.fillText(op.label, op.x, oy + 12)
    ctx.font = '9px monospace'
    ctx.fillStyle = '#606266'
    ctx.fillText(op.val, op.x, oy + 24)
    ctx.globalAlpha = 1
  }

  // Draw animated arrows from before to after
  for (let i = 0; i < regs.length; i++) {
    const sx = startX + i * (boxW + gap) + boxW / 2
    const sy = beforeY + boxH
    const changed = round.state_before[regs[i]] !== round.state_after[regs[i]]

    // Arrow target: registers shift right (b←a, c←b, ...) with a and e getting new values
    let targetI = i
    if (i === 0 || i === 4) {
      // a and e get new computed values - draw special arrows
    }

    const ey = afterY
    const progress = animProgress.value

    ctx.strokeStyle = changed ? '#409eff' : '#dcdfe6'
    ctx.lineWidth = changed ? 1.5 : 0.5
    ctx.globalAlpha = 0.4 + 0.6 * progress
    ctx.setLineDash(changed ? [] : [3, 3])
    ctx.beginPath()
    ctx.moveTo(sx, sy + 4)
    const curEy = sy + 4 + (ey - sy - 8) * progress
    ctx.lineTo(sx, curEy)
    ctx.stroke()
    ctx.setLineDash([])
    ctx.globalAlpha = 1

    // Arrowhead
    if (progress > 0.9 && changed) {
      ctx.fillStyle = '#409eff'
      ctx.beginPath()
      ctx.moveTo(sx, ey - 4)
      ctx.lineTo(sx - 4, ey - 10)
      ctx.lineTo(sx + 4, ey - 10)
      ctx.closePath()
      ctx.fill()
    }
  }

  // Draw "after" registers
  ctx.font = '11px sans-serif'
  ctx.fillStyle = '#909399'
  ctx.textAlign = 'center'
  ctx.fillText('压缩后状态', w / 2, afterY - 10)

  for (let i = 0; i < regs.length; i++) {
    const x = startX + i * (boxW + gap)
    const reg = regs[i]
    const val = round.state_after[reg]
    const changed = round.state_before[reg] !== round.state_after[reg]

    ctx.globalAlpha = animProgress.value
    ctx.fillStyle = changed ? '#ecf5ff' : '#f5f7fa'
    ctx.strokeStyle = changed ? '#409eff' : '#dcdfe6'
    ctx.lineWidth = changed ? 2 : 1
    roundRect(ctx, x, afterY, boxW, boxH, 6)
    ctx.fill()
    ctx.stroke()

    ctx.font = 'bold 11px sans-serif'
    ctx.fillStyle = changed ? '#409eff' : '#909399'
    ctx.textAlign = 'center'
    ctx.fillText(reg.toUpperCase(), x + boxW / 2, afterY + 14)

    ctx.font = '10px monospace'
    ctx.fillStyle = changed ? '#409eff' : '#303133'
    ctx.fillText(val.slice(0, 4), x + boxW / 2, afterY + 30)
    ctx.fillText(val.slice(4), x + boxW / 2, afterY + 40)
    ctx.globalAlpha = 1
  }

  // Round progress bar
  const barY = h - 24
  const barW = w - 60
  const barX = 30
  ctx.fillStyle = '#ebeef5'
  roundRect(ctx, barX, barY, barW, 6, 3)
  ctx.fill()
  const rp = props.rounds.length > 1 ? props.currentRound / (props.rounds.length - 1) : 0
  ctx.fillStyle = '#67c23a'
  roundRect(ctx, barX, barY, barW * rp, 6, 3)
  ctx.fill()
  ctx.font = '10px sans-serif'
  ctx.fillStyle = '#909399'
  ctx.textAlign = 'center'
  ctx.fillText(`轮次 ${props.currentRound + 1} / ${props.rounds.length}`, w / 2, barY + 18)
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
