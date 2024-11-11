import request from "../utils/request.js";

const baseUrl = ''

// 指标构建
export const generateInd = (params) => {
  return request({
    url: baseUrl + "/generateInd",
    method: "get",
  });
}
// 开始训练
export const startTrain = (params) => {
  return request({
    url: baseUrl + "/train",
    method: "post",
    data
  });
}
// 预测
export const startPredict = (params) => {
  return request({
    url: baseUrl + "/predict",
    method: "post",
    data
  });
}