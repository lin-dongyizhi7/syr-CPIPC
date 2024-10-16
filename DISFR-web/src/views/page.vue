<template>
  <div class="content-page">
    <div class="input-block">
      <slot name="input"></slot>
    </div>
    <div class="process">
      <slot name="process"></slot>
    </div>
    <div class="result-show">
      <div class="info-tip">输出</div>
      <div class="output-block">
        <slot name="output"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="less">
::-webkit-scrollbar {
  display: none; /* Chrome Safari */
}

.content-page {
  display: flex;
  height: 100%;
  justify-self: space-around;
  width: calc(80vw - 22px);
}

.info-tip {
  margin-bottom: 8px;
}

.input-block {
  flex: 2;
  padding: 0px 10px;
  height: 100% !important;
  max-width: 400px;
  overflow: scroll;
  scrollbar-width: none;
}

.process {
  flex: 1;
  padding: 20px 10px;
  height: calc(100vh - 300px);
}

.result-show {
  flex: 2;
  padding: 0px 10px;
  height: calc(100vh - 300px);
}
.output-block {
  height: calc(100% - 50px);
  border: 1px solid #66666644;
  border-radius: 6px;
  -webkit-border-radius: 6px;
  -moz-border-radius: 6px;
  -ms-border-radius: 6px;
  -o-border-radius: 6px;
  padding: 8px 12px;
}
</style>
