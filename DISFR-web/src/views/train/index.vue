<template>
  <page>
    <template #input>
      <el-form
        :model="formModel"
        :rules="formRules"
        ref="formRef"
        label-width="100px"
        label-position="left"
      >
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
        <el-form-item label="基本模型类型">
          <el-select v-model="formModel.baseModel">
            <el-option
              label="未选择模型则自动根据文件大小选择适合的模型进行训练"
              disabled
              size="small"
            ></el-option>
            <el-option
              v-for="model in models"
              :key="model"
              :label="model"
              :value="model"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="是否启用GPU">
          <el-switch v-model="formModel.gpu" size="small"></el-switch>
        </el-form-item>
        <el-form-item label="total_epoch">
          <el-slider
            v-model="formModel.totalEpoch"
            :step="1"
            :min="2"
            :max="100"
            show-input
            size="small"
          />
        </el-form-item>
        <el-form-item label="batch_size">
          <el-slider
            v-model="formModel.batchSize"
            :step="1"
            :min="1"
            :max="64"
            show-input
            size="small"
          />
        </el-form-item>
      </el-form>
    </template>
    <template #process>
      <opt-btn-progress opt-name="训练" @success="success = true"></opt-btn-progress>
    </template>
    <template #output>
      <div v-if="success">训练完成</div>
    </template>
  </page>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { UploadFilled } from "@element-plus/icons-vue";
import type { UploadProps, UploadFile } from "element-plus";
import { ElMessage } from "element-plus";
import Papa from "papaparse";

import Page from "../page.vue";
import OptBtnProgress from "../../components/opt-btn-progress.vue";

const formModel = reactive({
  filePath: "",
  file: null,
  baseModel: "DWT-Informer",
  totalEpoch: 20,
  batchSize: 8,
  gpu: false,
});
const formRef = ref();

const formRules = {
  //   filePath: [{ required: true, message: "未上传文件" }],
};

const models = ["DWT-Informer", "Informer", "LSTM", "GRU"];

const handleBeforeUpload: UploadProps["beforeUpload"] = (rawFile) => {
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
  font-weight: normal;
}

.upload-file {
  width: 100%;
}

:deep(.el-form-item__label) {
  font-size: 12px;
}

:deep(.el-slider--with-input) {
  .el-slider__input {
    width: 100px;
  }
}
</style>
