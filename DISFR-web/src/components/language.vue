<template>
  <el-dropdown @command="handleCommand" class="lang-warp">
    <span class="el-dropdown-link">
      {{ langType[store.language] }}
      <el-icon>
        <arrow-down />
      </el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="zhCn">中文</el-dropdown-item>
        <el-dropdown-item command="en">English</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { langType } from "../enum/options";
import { useLangStore } from "../store/modules/lang";

import { getCurrentInstance } from "vue";
import { ElMessage } from "element-plus";

const store = useLangStore();
const { proxy } = getCurrentInstance() as any;
const handleCommand = (value: "zhCn" | "en") => {
  if (store.language === value) return;
  proxy.$i18n.locale = value;
  store.changeLang(value);
  ElMessage.closeAll();
  ElMessage.success(`${value === "en" ? "英文" : "中文"}切换成功！`);
};
</script>

<style scoped lang="scss">
.lang-warp {
  margin: 0 20px;
}
</style>
