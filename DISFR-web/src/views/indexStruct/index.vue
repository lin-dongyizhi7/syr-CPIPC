<!--
 * @Author: lin-dongyizhi7 2985956026@qq.com
 * @Date: 2024-11-15 00:20:21
 * @LastEditors: lin-dongyizhi7 2985956026@qq.com
 * @LastEditTime: 2024-11-19 17:33:34
 * @FilePath: \systemic financial crises\DISFR-web\src\views\indexStruct\index.vue
 * @Description: Systemic Financial Crises
-->
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
        <div class="info-input">
          <el-form-item label="选取列">
            <el-select v-model="formModel.cols" multiple placeholder="">
              <template #header>
                <el-checkbox
                    v-model="checkAll"
                    :indeterminate="indeterminate"
                    @change="handleCheckAll"
                >
                  All
                </el-checkbox>
              </template>
              <el-option
                  v-for="item in columns"
                  :key="item"
                  :label="item"
                  :value="item"
              >
                <div class="flex items-center">
                  <el-tag type="info" size="small">{{ item }}</el-tag>
                </div>
              </el-option>
              <template #tag>
                <el-tag type="success" v-for="item in formModel.cols" :key="item">{{ item }}</el-tag>
              </template>
            </el-select>
          </el-form-item>
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
                  <color-style :colors="item.colors"></color-style>
                  {{ item.label }}
                </div>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="是否归一化">
            <el-switch v-model="formModel.normal"></el-switch>
          </el-form-item>
        </div>
      </el-form>
    </template>
    <template #process>
      <opt-btn-progress
          opt-name="构造"
          :disbled="!formModel.file && !formModel.filePath"
          :reset="reset"
          @start="startGenerateInd"
          @success="success = true">
      </opt-btn-progress>
    </template>
    <template #output>
      <div v-if="!reset">
        <div v-if="starting">构造中...</div>
      </div>
      <div v-if="!starting && success && finished">构造成功，保存到opt目录下</div>
    </template>
  </page>
  <el-dialog v-model="showAddStyle" title="自定义风格">
    <add-style @save="saveStyle" @cancel="showAddStyle = false"></add-style>
  </el-dialog>
</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import {UploadFilled} from "@element-plus/icons-vue";
import type {UploadProps, UploadFile, UploadRawFile, UploadInstance} from "element-plus";
import {ElMessage, genFileId} from "element-plus";
import Papa from "papaparse";

import Page from "../page.vue";
import OptBtnProgress from "../../components/opt-btn-progress.vue";
import ColorStyle from "../../components/color-style.vue";
import addStyle from "../../components/add-style.vue";

import {styles} from "../../enum/options";

import {generateInd} from "../../api/api.ts";

const formModel = reactive({
  filePath: "",
  file: null,
  cols: [],
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
  // console.log(rawFile);
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

let fileData: any;
let file: any;
const columns = ref([]);
const indeterminate = ref(false);

const handleCheckAll = (val) => {
  indeterminate.value = false
  if (val) {
    formModel.cols = columns.value;
  } else {
    formModel.cols = [];
  }
}

const upload = ref<UploadInstance>()
const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0] as UploadRawFile;
  file.uid = genFileId()
  upload.value!.handleStart(file)
}

const handleOnChange = (uploadFile: UploadFile, uploadFiles: UploadFile[]) => {
  file = uploadFile;
  reset.value = false;
  Papa.parse(uploadFile.raw, {
    header: true,
    dynamicTyping: true,
    complete: function (results: any) {
      // console.log("解析结果:", results.data);
      // 在这里处理解析后的内容
      fileData = results.data;
      columns.value = Object.keys(fileData[0]);
    },
  });
};

const reset = ref(false);
const handleOnRemove = (uploadFile: UploadFile, uploadFiles: UploadFile[]) => {
  if (uploadFiles.length === 0) {
    reset.value = true;
    columns.value = [];
  }
}

const uploadRequest = () => {
};

const startGenerateInd = () => {
  starting.value = true;
  if (formModel.filePath) {
    let paths = formModel.filePath.split('/')
    generateInd({
      name: paths[paths.length - 1].split('.')[0],
      filePath: formModel.filePath,
      cols: formModel.cols,
      draw: formModel.draw,
      drawThreshold: formModel.drawThreshold,
      drawStyle: formModel.drawStyle,
      normal: formModel.normal,
    }).then((results: any) => {
      finished.value = true;
      starting.value = false;
      reset.value = true;
    });
  } else {
    generateInd({
      name: file.name,
      data: fileData,
      cols: formModel.cols,
      draw: formModel.draw,
      drawThreshold: formModel.drawThreshold,
      drawStyle: formModel.drawStyle,
      normal: formModel.normal,
    }).then((results: any) => {
      finished.value = true;
      starting.value = false;
      reset.value = true;
    });
  }
}

const starting = ref(false);
const finished = ref(false);
const success = ref(false);
</script>

<style scoped lang="less">
.info-tip {
  margin-bottom: 8px;
}

.upload-file {
  width: 100%;
}

.info-input {
  height: 200px;
  overflow: scroll;
  scrollbar-width: none;
}
</style>
