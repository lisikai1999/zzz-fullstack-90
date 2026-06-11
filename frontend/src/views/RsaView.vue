<template>
  <div class="page-container">
    <h2>RSA 加密算法 — 交互式演示</h2>
    <el-alert type="info" :closable="false" style="margin-bottom: 16px">
      RSA 基于大数分解的困难性：知道 n 很难分解回 p 和 q，因此无法从公钥推导私钥。
    </el-alert>

    <el-row :gutter="24">
      <el-col :span="8">
        <el-card header="参数设置">
          <el-form label-position="top">
            <el-form-item label="素数 p">
              <el-input-number v-model="store.p" :min="2" :max="9999" />
            </el-form-item>
            <el-form-item label="素数 q">
              <el-input-number v-model="store.q" :min="2" :max="9999" />
            </el-form-item>
            <el-form-item label="公钥指数 e (可选)">
              <el-input-number v-model="store.e" :min="3" />
            </el-form-item>
            <el-button type="primary" @click="store.doGenerateKeys()" :loading="store.loading">
              生成密钥
            </el-button>
          </el-form>
        </el-card>

        <el-card v-if="store.keyGenResult" header="加密/解密" style="margin-top: 16px">
          <el-form label-position="top">
            <el-form-item label="明文消息 m (数字)">
              <el-input-number v-model="message" :min="0" :max="store.keyGenResult.parameters.n - 1" />
            </el-form-item>
            <el-button type="success" @click="doEncrypt" :loading="store.loading">
              加密 (m^e mod n)
            </el-button>
            <el-button
              v-if="store.encryptResult"
              type="warning"
              @click="doDecrypt"
              :loading="store.loading"
              style="margin-top: 8px"
            >
              解密 (c^d mod n)
            </el-button>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-alert v-if="store.error" type="error" :title="store.error" show-icon />

        <div v-if="store.keyGenResult">
          <el-card header="密钥生成过程">
            <AnimationControls
              :current-step="keyGenStep"
              :total-steps="store.keyGenResult.steps.length"
              :is-playing="keyGenPlaying"
              @play="keyGenAnim.play()"
              @pause="keyGenAnim.pause()"
              @next="keyGenAnim.next()"
              @prev="keyGenAnim.prev()"
              @reset="keyGenAnim.reset()"
            />
            <StepDisplay :steps="store.keyGenResult.steps" :current-step="keyGenStep" />
            <el-descriptions :column="2" border style="margin-top: 16px">
              <el-descriptions-item label="公钥 (e, n)">
                ({{ store.keyGenResult.public_key.e }}, {{ store.keyGenResult.public_key.n }})
              </el-descriptions-item>
              <el-descriptions-item label="私钥 (d, n)">
                ({{ store.keyGenResult.private_key.d }}, {{ store.keyGenResult.private_key.n }})
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>

        <div v-if="store.encryptResult" style="margin-top: 16px">
          <el-card header="加密过程: c = m^e mod n (逐位平方乘法)">
            <ModExpCanvas :steps="store.encryptResult.steps" :current-step="encStep" />
            <AnimationControls
              :current-step="encStep"
              :total-steps="store.encryptResult.steps.length"
              :is-playing="encPlaying"
              @play="encAnim.play()"
              @pause="encAnim.pause()"
              @next="encAnim.next()"
              @prev="encAnim.prev()"
              @reset="encAnim.reset()"
            />
            <StepDisplay :steps="store.encryptResult.steps" :current-step="encStep" />
            <el-tag type="success" size="large" style="margin-top: 12px">
              密文 c = {{ store.encryptResult.result }}
            </el-tag>
          </el-card>
        </div>

        <div v-if="store.decryptResult" style="margin-top: 16px">
          <el-card header="解密过程: m = c^d mod n (逐位平方乘法)">
            <ModExpCanvas :steps="store.decryptResult.steps" :current-step="decStep" />
            <AnimationControls
              :current-step="decStep"
              :total-steps="store.decryptResult.steps.length"
              :is-playing="decPlaying"
              @play="decAnim.play()"
              @pause="decAnim.pause()"
              @next="decAnim.next()"
              @prev="decAnim.prev()"
              @reset="decAnim.reset()"
            />
            <StepDisplay :steps="store.decryptResult.steps" :current-step="decStep" />
            <el-tag type="warning" size="large" style="margin-top: 12px">
              解密后明文 m = {{ store.decryptResult.result }}
            </el-tag>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRsaStore } from '../stores/rsa'
import { useAnimation } from '../composables/useAnimation'
import StepDisplay from '../components/common/StepDisplay.vue'
import AnimationControls from '../components/common/AnimationControls.vue'
import ModExpCanvas from '../components/rsa/ModExpCanvas.vue'

const store = useRsaStore()
const message = ref(65)

const keyGenTotal = computed(() => store.keyGenResult?.steps?.length || 0)
const keyGenAnim = useAnimation(keyGenTotal)
const keyGenStep = computed(() => keyGenAnim.currentStep.value)
const keyGenPlaying = computed(() => keyGenAnim.isPlaying.value)

const encTotal = computed(() => store.encryptResult?.steps?.length || 0)
const encAnim = useAnimation(encTotal)
const encStep = computed(() => encAnim.currentStep.value)
const encPlaying = computed(() => encAnim.isPlaying.value)

const decTotal = computed(() => store.decryptResult?.steps?.length || 0)
const decAnim = useAnimation(decTotal)
const decStep = computed(() => decAnim.currentStep.value)
const decPlaying = computed(() => decAnim.isPlaying.value)

watch(() => store.keyGenResult, () => { keyGenAnim.reset() })
watch(() => store.encryptResult, () => { encAnim.reset() })
watch(() => store.decryptResult, () => { decAnim.reset() })

function doEncrypt() {
  store.doEncrypt(message.value)
}
function doDecrypt() {
  store.doDecrypt(store.encryptResult.result)
}
</script>
