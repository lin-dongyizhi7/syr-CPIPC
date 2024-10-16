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
          <el-form-item label="画图风格">
            <el-select v-model="formModel.drawStyle">
              <el-option v-for="item in styles" :label="item.label" :value="item.value">
                <div style="display: flex; align-items: center">
                  <color-style :colors="item.colors"></color-style> {{ item.label }}
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </div>
      </el-form>
    </template>
    <template #process>
      <opt-btn-progress opt-name="预测"></opt-btn-progress>
    </template>
    <template #output></template>
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
import ColorStyle from "../../components/color-style.vue";

import { styles } from "../../enum/options";

const formModel = reactive({
  filePath: "",
  file: null,
  drawStyle: "common",
});
const formRef = ref();

const formRules = {
  //   filePath: [{ required: true, message: "未上传文件" }],
};

const handleBeforeUpload: UploadProps["beforeUpload"] = (rawFile) => {
  if (rawFile.type !== "csv" && rawFile.type !== "xlsx" && rawFile.type !== "xls") {
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
</script>

<style scoped lang="less">
.info-tip {
  margin-bottom: 8px;
}

.upload-file {
  width: 100%;
}
</style>
