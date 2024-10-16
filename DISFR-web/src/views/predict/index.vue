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
          <el-form-item label="" prop="draw">
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

import Page from "../page.vue";
import OptBtnProgress from "../../components/opt-btn-progress.vue";
import ColorStyle from "../../components/color-style.vue";

import { styles } from "../../enum/options";

const formModel = reactive({
  filePath: "",
  file: null,
  drawStyle: 'common'
});
const formRef = ref();

const formRules = {
  //   filePath: [{ required: true, message: "未上传文件" }],
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
