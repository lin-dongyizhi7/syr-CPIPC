<template>
  <div class="home-page">
    <div class="title">
      <h2>系统性金融风险预测</h2>
    </div>
    <el-tabs type="border-card" @tab-change="handleChange">
      <el-tab-pane label="指标构建">
        <index-struct></index-struct>
      </el-tab-pane>
      <el-tab-pane label="模型训练">
        <train-page v-if="activeTab === '1'"></train-page>
      </el-tab-pane>
      <el-tab-pane label="风险预测">
        <predict-page v-if="activeTab === '2'"></predict-page>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import IndexStruct from "./indexStruct/index.vue";
import TrainPage from "./train/index.vue";
import PredictPage from "./predict/index.vue";

import { ref } from "vue";

import i18n from "../i18n/index";
// const t = i18n()

const activeTab = ref(0);

const handleChange = (name) => {
  activeTab.value = name;
};
</script>

<style scoped lang="less">
.home-page {
  position: absolute;
  top: 0;
  left: 0;
  width: 80%;
  height: 100%;
  padding: 0 10%;

  .title {
    margin: 20px 10px 30px;
  }
}

:deep(.el-tabs__content) {
    height: calc(100vh - 240px);
}
</style>
