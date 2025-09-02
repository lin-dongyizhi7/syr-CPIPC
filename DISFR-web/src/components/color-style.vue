<!--
 * @Author: lin-dongyizhi7 2985956026@qq.com
 * @Date: 2024-11-15 00:20:21
 * @LastEditors: lin-dongyizhi7 2985956026@qq.com
 * @LastEditTime: 2024-11-19 17:30:11
 * @FilePath: \systemic financial crises\DISFR-web\src\components\color-style.vue
 * @Description: Systemic Financial Crises
-->
<template>
  <div class="color-list">
    <div
      v-for="color in colors"
      class="color"
      :style="`background: ${color}`"
    ></div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  colors: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped lang="less">
.color-list {
    display: flex;
    padding-right: 6px;
}
.color {
    height: 20px;
    width: 10px;
}
</style>
