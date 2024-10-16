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
