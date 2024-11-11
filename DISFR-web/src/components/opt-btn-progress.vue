<template>
  <div v-if="!processing" class="start">
    <el-button @click="startProcess">{{ optName }}</el-button>
  </div>
  <div v-else class="py-progress">
    <el-progress :percentage="percentage" :show-text="false" striped></el-progress>
  </div>
</template>

<script setup lang="ts">
import {computed, ref, watch} from "vue";

const props = defineProps({
  optName: {
    type: String,
  },
  reset: {
    type: Boolean,
  }
});

const emits = defineEmits(['start', 'success']);

// const blank = computed(()=>props.reset);
const processing = ref(false);
const percentage = ref(0);

const startProcess = () => {
  processing.value = true;
  emits('start');
  load();
};

const load = () => {
  let n = 0;
  let timer;
  timer = setInterval(function () {
    n = (n + Math.random() * 10) | 0;
    if (n > 100) {
      n = 100;
      clearInterval(timer);
      emits('success');
    }
    percentage.value = n;
  }, 100 + Math.random() * 300);
};

watch(props, (val) => {
  if (val) {
    processing.value = false;
  }
}, {deep: true});
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

  font-size: 18px;
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
