<template>
  <div class="app-welcome" v-if="!enter">
    <div class="title">
      <img style="height: 40px" src="../public/logo.png" />
      <!-- <img src="../public/logo-text.png" /> -->
      <div style="font-size: 60px; color: #c7ecee">系统性金融风险预测</div>
    </div>
    <div style="display: flex; width: 100% ; justify-content: center">
      <el-button style="font-size: 32px; margin-top: 50px; color: #16b77788" link @click="enter = true">进入</el-button>
    </div>
  </div>
  <Home v-else />
</template>

<script setup lang="ts">
import Home from "./views/home.vue";

import { ref } from 'vue';

const enter = ref(false);
</script>

<style scoped lang="less">
.app-welcome {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  padding-top: 15%;
  background-image: url('../public/image.png');
  background-size: cover;
}

.title {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
  img {
    height: 100px;
  }
}
</style>
