<template>
  <div v-if="!processing" class="start">
    <el-button @click="startProcess">{{ optName }}</el-button>
  </div>
  <div v-else class="py-progress">
    <el-progress :percentage="percentage" :text-inside="true" striped></el-progress>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps({
  optName: {
    type: String,
  },
});

const processing = ref(false);
const percentage = ref(0);

const startProcess = () => {
  processing.value = true;
  load();
};

const load = () => {
  let n = 0;
  var timer = setInterval(function () {
    n = (n + Math.random() * 10) | 0;
    if (n > 100) {
      n = 100;
      clearInterval(timer);
    }
    percentage.value = n;
  }, 100 + Math.random() * 1000);
};
</script>

<style scoped lang="less">
.start {
  height: 100%;
}

.py-progress {
  height: 100%;
}

:deep(.el-button) {
  width: 100%;
  height: 100%;
  background-color: #16b77788;
  border-radius: 12px;
}

:deep(.el-progress) {
  height: 100%;
  .el-progress-bar {
    height: 100%;
  }
  .el-progress-bar__outer {
    height: 100% !important;
    border-radius: 12px;
  }
  .el-progress-bar__inner {
    border-radius: 12px;
    background-color: #16b77788;
  }
  .el-progress-bar__innerText {
    position: relative;
    left: -50%;
    transform: translateX(50%);
  }
}
</style>
