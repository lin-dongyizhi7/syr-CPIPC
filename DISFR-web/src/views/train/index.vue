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
                ref="upload"
                class="upload-file"
                drag
                :limit="1"
                :http-request="uploadRequest"
                :before-upload="handleBeforeUpload"
                :on-change="handleOnChange"
                :on-remove="handleOnRemove"
                :on-exceed="handleExceed"
            >
              <el-icon class="el-icon--upload">
                <upload-filled/>
              </el-icon>
              <div class="el-upload__text">拖拽文件到此处 或者 <em>点击此处</em></div>
              <div class="el-upload__tip">小于10MB的csv/xlsx/xls文件</div>
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
      <opt-btn-progress
          opt-name="训练"
          :disbled="!formModel.file && !formModel.filePath"
          :reset="reset"
          @start="startTrainModel"
          @success="success = true">
      </opt-btn-progress>
    </template>
    <template #output>
      <div v-if="!reset">
        <div v-if="starting">训练中...</div>
        <div v-if="!starting && success && finished">训练完成</div>
      </div>
    </template>
  </page>
</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import {UploadFilled} from "@element-plus/icons-vue";
import type {UploadProps, UploadFile} from "element-plus";
import {ElMessage} from "element-plus";
import Papa from "papaparse";

import Page from "../page.vue";
import OptBtnProgress from "../../components/opt-btn-progress.vue";

import {startTrain} from "../../api/api.ts";

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
  } else if (rawFile.size / 1024 / 1024 > 10) {
    ElMessage.error("文件大小超出限制!");
    return false;
  }
  return true;
};

let fileData;
let file;

const upload = ref<UploadInstance>()
const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0]
  file.uid = genFileId()
  upload.value!.handleStart(file)
}

const handleOnChange = (uploadFile: UploadFile) => {
  file = uploadFile;
  reset.value = false;
  Papa.parse(uploadFile.raw, {
    header: true,
    dynamicTyping: true,
    complete: function (results: any) {
      console.log("解析结果:", results.data);
      // 在这里处理解析后的内容
      fileData = results.data;
    },
  });
};

const reset = ref(false);
const handleOnRemove = (uploadFile: UploadFile, uploadFiles: UploadFiles) => {
  if (uploadFiles.length === 0) {
    reset.value = true;
  }
}

const uploadRequest = () => {
};

const startTrainModel = () => {
  starting.value = true;
  const config = {
    baseModel: formModel.baseModel,
    totalEpoch: formModel.totalEpoch,
    batchSize: formModel.batchSize,
    gpu: formModel.gpu,
  }
  if (formModel.filePath) {
    let paths = filePath.split('/');
    let name = paths.split('.')[0];
    startTrain({
      type: 'path',
      name: name,
      filePath: formModel.filePath,
      ...config
    }).then((results: any) => {
      finished.value = true;
      starting.value = false;
    });
  } else {
    startTrain({
      type: 'file',
      name: file.name.split('.')[0],
      data: fileData,
      ...config
    }).then((results: any) => {
      finished.value = true;
      starting.value = false;
    });
  }
};

const starting = ref(false);
const finished = ref(false);
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
