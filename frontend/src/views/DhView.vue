<template>
  <div class="page-container">
    <h2>Diffie-Hellman 密钥交换 — 交互式演示</h2>
    <el-alert type="info" :closable="false" style="margin-bottom: 16px">
      DH 协议让双方在不安全信道上协商出相同的共享密钥，安全性基于离散对数问题的困难性。
    </el-alert>

    <el-tabs v-model="activeTab">
      <!-- Tab 1: Color Mixing Analogy -->
      <el-tab-pane label="颜色混合类比" name="color">
        <el-row :gutter="24">
          <el-col :span="8">
            <el-card header="颜色参数">
              <el-form label-position="top">
                <el-form-item label="公共颜色">
                  <el-color-picker v-model="store.commonColor" />
                </el-form-item>
                <el-form-item label="Alice 私有颜色">
                  <el-color-picker v-model="store.aliceColor" />
                </el-form-item>
                <el-form-item label="Bob 私有颜色">
                  <el-color-picker v-model="store.bobColor" />
                </el-form-item>
                <el-button type="primary" @click="store.doColorMixing()" :loading="store.loading">
                  执行颜色混合
                </el-button>
              </el-form>
            </el-card>
          </el-col>
          <el-col :span="16">
            <el-card v-if="store.colorResult">
              <ColorMixingCanvas :color-result="store.colorResult" />
              <p style="margin-top: 12px; color: #606266; font-size: 13px">
                {{ store.colorResult.explanation }}
              </p>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <!-- Tab 2: Mathematical DH Exchange -->
      <el-tab-pane label="数学计算" name="math">
        <el-row :gutter="24">
          <el-col :span="8">
            <el-card header="DH 参数">
              <el-form label-position="top">
                <el-form-item label="素数 p">
                  <el-input-number v-model="store.p" :min="3" :max="9999" />
                </el-form-item>
                <el-form-item label="生成元 g">
                  <el-input-number v-model="store.g" :min="2" :max="store.p - 1" />
                </el-form-item>
                <el-form-item label="Alice 私钥 a">
                  <el-input-number v-model="store.aPrivate" :min="1" :max="store.p - 1" />
                </el-form-item>
                <el-form-item label="Bob 私钥 b">
                  <el-input-number v-model="store.bPrivate" :min="1" :max="store.p - 1" />
                </el-form-item>
                <el-button type="primary" @click="store.doExchange()" :loading="store.loading">
                  执行密钥交换
                </el-button>
              </el-form>
            </el-card>
          </el-col>
          <el-col :span="16">
            <el-alert v-if="store.error" type="error" :title="store.error" show-icon />
            <el-card v-if="store.exchangeResult" header="密钥交换过程">
              <AnimationControls
                :current-step="exchStep"
                :total-steps="store.exchangeResult.steps.length"
                :is-playing="exchPlaying"
                @play="exchAnim.play()"
                @pause="exchAnim.pause()"
                @next="exchAnim.next()"
                @prev="exchAnim.prev()"
                @reset="exchAnim.reset()"
              />
              <StepDisplay :steps="store.exchangeResult.steps" :current-step="exchStep" />
              <el-tag type="success" size="large" style="margin-top: 12px">
                共享密钥: {{ store.exchangeResult.shared_secret }}
              </el-tag>
              <p style="margin-top: 8px; color: #606266; font-size: 13px">
                {{ store.exchangeResult.security_note }}
              </p>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <!-- Tab 3: MITM Attack -->
      <el-tab-pane label="中间人攻击" name="mitm">
        <el-row :gutter="24">
          <el-col :span="8">
            <el-card header="MITM 参数">
              <el-form label-position="top">
                <el-form-item label="素数 p">
                  <el-input-number v-model="store.p" :min="3" :max="9999" />
                </el-form-item>
                <el-form-item label="生成元 g">
                  <el-input-number v-model="store.g" :min="2" />
                </el-form-item>
                <el-form-item label="Alice 私钥">
                  <el-input-number v-model="store.aPrivate" :min="1" />
                </el-form-item>
                <el-form-item label="Bob 私钥">
                  <el-input-number v-model="store.bPrivate" :min="1" />
                </el-form-item>
                <el-form-item label="Mallory 私钥">
                  <el-input-number v-model="store.mPrivate" :min="1" />
                </el-form-item>
                <el-button type="danger" @click="store.doMitm()" :loading="store.loading">
                  模拟中间人攻击
                </el-button>
              </el-form>
            </el-card>
          </el-col>
          <el-col :span="16">
            <el-card v-if="store.mitmResult" header="中间人攻击过程">
              <AnimationControls
                :current-step="mitmStep"
                :total-steps="store.mitmResult.steps.length"
                :is-playing="mitmPlaying"
                @play="mitmAnim.play()"
                @pause="mitmAnim.pause()"
                @next="mitmAnim.next()"
                @prev="mitmAnim.prev()"
                @reset="mitmAnim.reset()"
              />
              <StepDisplay :steps="store.mitmResult.steps" :current-step="mitmStep" />
              <el-alert type="error" :closable="false" style="margin-top: 12px">
                {{ store.mitmResult.explanation }}
              </el-alert>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useDhStore } from '../stores/dh'
import { useAnimation } from '../composables/useAnimation'
import StepDisplay from '../components/common/StepDisplay.vue'
import AnimationControls from '../components/common/AnimationControls.vue'
import ColorMixingCanvas from '../components/dh/ColorMixingCanvas.vue'

const store = useDhStore()
const activeTab = ref('color')

const exchTotal = computed(() => store.exchangeResult?.steps?.length || 0)
const exchAnim = useAnimation(exchTotal)
const exchStep = computed(() => exchAnim.currentStep.value)
const exchPlaying = computed(() => exchAnim.isPlaying.value)

const mitmTotal = computed(() => store.mitmResult?.steps?.length || 0)
const mitmAnim = useAnimation(mitmTotal)
const mitmStep = computed(() => mitmAnim.currentStep.value)
const mitmPlaying = computed(() => mitmAnim.isPlaying.value)

watch(() => store.exchangeResult, () => exchAnim.reset())
watch(() => store.mitmResult, () => mitmAnim.reset())
</script>
