<template>
  <page>
    <template #input>
      <el-form :model="formModel" :rules="formRules" ref="formRef">
        <div class="file-receive">
          <div class="info-tip">下面两种方式二选一即可</div>
          <el-form-item label="输入待处理文件夹路径" label-position="top" prop="filePath">
            <el-input
              v-model="formModel.filePath"
              placeholder="C:\Users\Desktop\my-files"
            ></el-input>
          </el-form-item>
          <el-form-item label="" label-position="top">
            <el-upload
              class="upload-file"
              drag
              action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
              multiple
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                Drop file here or <em>click to upload</em>
              </div>
              <div class="el-upload__tip">
                csv/xlsx/xls file with a size less than 10mb
              </div>
            </el-upload>
          </el-form-item>
        </div>
        <el-form-item label="是否画图">
          <el-switch v-model="formModel.draw"></el-switch>
        </el-form-item>
        <el-form-item v-if="formModel.draw" label="风险阈值">
          <el-select
            filterable
            allow-create
            placeholder="自定义输入"
            v-model="formModel.drawThreshold"
          >
            <el-option label="默认" value="default"></el-option>
            <el-option label="不设置阈值" value="none"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="formModel.draw" label="画图风格">
          <el-select filterable allow-create v-model="formModel.drawStyle">
            <template #header>
              <el-button link @click="showAddStyle = true">自定义</el-button>
            </template>
            <el-option v-for="item in styles" :label="item.label" :value="item.value">
              <div style="display: flex; align-items: center">
                <color-style :colors="item.colors"></color-style> {{ item.label }}
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否归一化">
          <el-switch v-model="formModel.normal"></el-switch>
        </el-form-item>
      </el-form>
    </template>
    <template #process>
      <opt-btn-progress opt-name="构造"></opt-btn-progress>
    </template>
    <template #output></template>
  </page>
  <el-dialog v-model="showAddStyle" title="自定义风格">
    <add-style @save="saveStyle" @cancel="showAddStyle = false"></add-style>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { UploadFilled } from "@element-plus/icons-vue";

import Page from "../page.vue";
import OptBtnProgress from "../../components/opt-btn-progress.vue";
import ColorStyle from "../../components/color-style.vue";
import addStyle from "../../components/add-style.vue";

import { styles } from "../../enum/options";

const formModel = reactive({
  filePath: "",
  file: null,
  draw: false,
  drawThreshold: null,
  drawStyle: "common",
  normal: true,
});
const formRef = ref();

const formRules = {
  //   filePath: [{ required: true, message: "未上传文件" }],
};

const showAddStyle = ref(false);
const saveStyle = () => {
  showAddStyle.value = false;
};
</script>

<style scoped lang="less">
.info-tip {
  margin-bottom: 8px;
}

.upload-file {
  width: 100%;
}
</style>
