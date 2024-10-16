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
              :http-request="uploadRequest"
              :before-upload="handleBeforeUpload"
              :on-change="handleOnChange"
              multiple
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">拖拽文件到此处 或者 <em>点击此处</em></div>
              <div class="el-upload__tip">小于100mb的csv/xlsx/xls文件</div>
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
            default-first-option
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
      <opt-btn-progress opt-name="构造" @success="success = true"></opt-btn-progress>
    </template>
    <template #output>
      <div v-if="success">构造成功</div>
    </template>
  </page>
  <el-dialog v-model="showAddStyle" title="自定义风格">
    <add-style @save="saveStyle" @cancel="showAddStyle = false"></add-style>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { UploadFilled } from "@element-plus/icons-vue";
import type { UploadProps, UploadFile } from "element-plus";
import { ElMessage } from "element-plus";
import Papa from "papaparse";

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

const handleBeforeUpload: UploadProps["beforeUpload"] = (rawFile) => {
  console.log(rawFile);
  if (
    rawFile.type.endsWith("csv") &&
    rawFile.type.endsWith("xlsx") &&
    rawFile.type.endsWith("xls")
  ) {
    ElMessage.error("文件必须是csv/xlsx/xls格式!");
    return false;
  } else if (rawFile.size / 1024 / 1024 > 100) {
    ElMessage.error("文件大小超出限制!");
    return false;
  }
  return true;
};

const handleOnChange = (uploadFile: UploadFile) => {
  console.log(uploadFile);
  Papa.parse(uploadFile.raw, {
    header: true,
    dynamicTyping: true,
    complete: function (results: any) {
      console.log("解析结果:", results.data);
      // 在这里处理解析后的内容
    },
  });
};

const uploadRequest = () => {};

const success = ref(false);
</script>

<style scoped lang="less">
.info-tip {
  margin-bottom: 8px;
}

.upload-file {
  width: 100%;
}
</style>
