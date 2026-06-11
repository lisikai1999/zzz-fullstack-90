<template>
  <div class="page-container">
    <el-row :gutter="24">
      <el-col :span="8" v-for="mod in modules" :key="mod.path">
        <el-card shadow="hover" class="module-card" @click="$router.push(mod.path)">
          <template #header>
            <span class="module-title">{{ mod.title }}</span>
          </template>
          <p>{{ mod.description }}</p>
          <ul>
            <li v-for="feat in mod.features" :key="feat">{{ feat }}</li>
          </ul>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
const modules = [
  {
    title: 'RSA 加密算法',
    path: '/rsa',
    description: '理解公钥加密的数学基础',
    features: [
      '密钥生成全过程展示',
      '模幂运算逐步计算',
      '加密/解密可视化',
    ],
  },
  {
    title: '哈希函数',
    path: '/hash',
    description: '看见哈希压缩的内部过程',
    features: [
      '简化 SHA 分块压缩展示',
      '每轮内部状态变化',
      '生日攻击实际碰撞演示',
    ],
  },
  {
    title: 'Diffie-Hellman 密钥交换',
    path: '/dh',
    description: '颜色混合比喻理解密钥协商',
    features: [
      '颜色混合动画类比',
      '数学步骤逐步展示',
      '中间人攻击演示',
    ],
  },
]
</script>

<style scoped>
.module-card {
  cursor: pointer;
  height: 100%;
  transition: transform 0.2s;
}
.module-card:hover {
  transform: translateY(-4px);
}
.module-title {
  font-size: 18px;
  font-weight: bold;
}
ul {
  padding-left: 20px;
  margin-top: 12px;
}
li {
  margin-bottom: 6px;
  color: #606266;
}
</style>
