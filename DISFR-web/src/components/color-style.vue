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
