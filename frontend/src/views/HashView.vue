<template>
  <div class="page-container">
    <h2>哈希函数 — 交互式演示</h2>
    <el-alert type="info" :closable="false" style="margin-bottom: 16px">
      哈希函数将任意长度输入压缩为固定长度输出。此处使用简化的 SHA 结构（16 轮）演示分块→压缩→链接的过程。
    </el-alert>

    <el-row :gutter="24">
      <el-col :span="8">
        <el-card header="哈希计算">
          <el-form label-position="top">
            <el-form-item label="输入消息">
              <el-input v-model="store.message" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item label="输出位数">
              <el-slider v-model="store.hashBits" :min="8" :max="32" :step="4" show-stops :marks="bitMarks" />
            </el-form-item>
            <el-button type="primary" @click="store.doComputeHash()" :loading="store.loading">
              计算哈希
            </el-button>
          </el-form>
        </el-card>

        <el-card header="生日攻击" style="margin-top: 16px">
          <p style="color: #606266; font-size: 13px; margin-bottom: 12px">
            对 {{ store.hashBits }} 位哈希发起生日攻击，预期约 2^{{ store.hashBits / 2 }} = {{ Math.pow(2, store.hashBits / 2) }} 次尝试找到碰撞。
          </p>
          <el-button type="danger" @click="startAttack" :disabled="attacking">
            {{ attacking ? '搜索中...' : '开始碰撞搜索' }}
          </el-button>

          <div v-if="store.attackProgress" style="margin-top: 12px">
            <el-progress :percentage="progressPct" :format="() => `${store.attackProgress.attempts} 次`" />
            <p style="font-size: 12px; color: #909399; margin-top: 4px">
              已存储 {{ store.attackProgress.hashes_stored }} 个哈希值，耗时 {{ store.attackProgress.elapsed_seconds }}s
            </p>
          </div>

          <div v-if="store.attackResult && store.attackResult.collision" style="margin-top: 12px">
            <el-alert type="success" :closable="false">
              <template #title>找到碰撞!</template>
              <p><strong>输入1:</strong> {{ store.attackResult.collision.input_1 }}</p>
              <p><strong>输入2:</strong> {{ store.attackResult.collision.input_2 }}</p>
              <p><strong>哈希值:</strong> {{ store.attackResult.collision.hash_value }}</p>
              <p><strong>尝试次数:</strong> {{ store.attackResult.collision.attempts_needed }}</p>
              <p style="margin-top: 8px; font-size: 12px; color: #606266">{{ store.attackResult.explanation }}</p>
            </el-alert>
          </div>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-alert v-if="store.error" type="error" :title="store.error" show-icon />

        <div v-if="store.hashResult">
          <el-card>
            <template #header>
              <span>哈希结果: <code>{{ store.hashResult.final_hash }}</code></span>
            </template>

            <p style="margin-bottom: 12px; color: #606266; font-size: 13px">
              {{ store.hashResult.padding_explanation }}
            </p>

            <div v-for="block in store.hashResult.blocks" :key="block.block_index" style="margin-bottom: 16px">
              <h4>块 #{{ block.block_index }}</h4>

              <CompressionCanvas :rounds="block.rounds" :current-round="roundStep" />

              <AnimationControls
                :current-step="roundStep"
                :total-steps="block.rounds.length"
                :is-playing="roundPlaying"
                @play="roundAnim.play()"
                @pause="roundAnim.pause()"
                @next="roundAnim.next()"
                @prev="roundAnim.prev()"
                @reset="roundAnim.reset()"
              />

              <el-tag style="margin-top: 8px">链接值: {{ block.chain_value_after.substring(0, 32) }}...</el-tag>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useHashStore } from '../stores/hash'
import { useAnimation } from '../composables/useAnimation'
import AnimationControls from '../components/common/AnimationControls.vue'
import CompressionCanvas from '../components/hash/CompressionCanvas.vue'

const store = useHashStore()
const attacking = ref(false)
let pollTimer = null

const bitMarks = { 8: '8', 16: '16', 24: '24', 32: '32' }

const roundTotal = computed(() => {
  if (!store.hashResult || !store.hashResult.blocks.length) return 0
  return store.hashResult.blocks[0].rounds.length
})
const roundAnim = useAnimation(roundTotal)
const roundStep = computed(() => roundAnim.currentStep.value)
const roundPlaying = computed(() => roundAnim.isPlaying.value)

const progressPct = computed(() => {
  if (!store.attackProgress) return 0
  const expected = Math.pow(2, store.hashBits / 2)
  return Math.min(100, Math.round((store.attackProgress.attempts / expected) * 100))
})

async function startAttack() {
  attacking.value = true
  await store.doStartAttack()
  pollTimer = setInterval(async () => {
    await store.pollProgress()
    if (store.attackProgress?.status === 'complete' || store.attackProgress?.status === 'error') {
      clearInterval(pollTimer)
      attacking.value = false
    }
  }, 500)
}

watch(() => store.hashResult, () => { roundAnim.reset() })

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>
