import request from "../utils/request.js";

const baseUrl = ''

// 指标构建
export const generateInd = (data) => {
  return request({
    url: baseUrl + "/generateInd",
    method: "post",
    data
  });
}
// 开始训练
export const startTrain = (data) => {
  return request({
    url: baseUrl + "/train",
    method: "post",
    data
  });
}
// 预测
export const startPredict = (data) => {
  return request({
    url: baseUrl + "/predict",
    method: "post",
    data
  });
}