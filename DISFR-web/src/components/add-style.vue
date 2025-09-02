<!--
 * @Author: lin-dongyizhi7 2985956026@qq.com
 * @Date: 2024-11-15 00:20:21
 * @LastEditors: lin-dongyizhi7 2985956026@qq.com
 * @LastEditTime: 2024-11-19 17:29:54
 * @FilePath: \systemic financial crises\DISFR-web\src\components\add-style.vue
 * @Description: Systemic Financial Crises
-->
<template>
  <div class="colors-band"></div>
  <el-button @click="cancel">取消</el-button>
  <el-button @click="save" type="primary">保存</el-button>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

const emits = defineEmits(["save", "cancel"]);

onMounted(() => {});

const cancel = () => {
  emits("cancel");
};
const save = () => {
  emits("save");
};
</script>

<style scoped lang="less"></style>
