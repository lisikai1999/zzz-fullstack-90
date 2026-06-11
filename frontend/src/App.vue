<template>
  <el-container>
    <el-header>
      <el-menu mode="horizontal" :router="true" :default-active="$route.path">
        <el-menu-item index="/" class="logo-item">
          <strong>密码学交互式教学</strong>
        </el-menu-item>
        <el-menu-item index="/rsa">RSA 加密</el-menu-item>
        <el-menu-item index="/hash">哈希函数</el-menu-item>
        <el-menu-item index="/dh">Diffie-Hellman</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
</script>

<style scoped>
.el-header {
  padding: 0;
}
.logo-item {
  font-size: 16px;
}
</style>
