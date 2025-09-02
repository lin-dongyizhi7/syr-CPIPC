/*
 * @Author: lin-dongyizhi7 2985956026@qq.com
 * @Date: 2024-11-15 00:20:21
 * @LastEditors: lin-dongyizhi7 2985956026@qq.com
 * @LastEditTime: 2024-11-19 17:32:26
 * @FilePath: \systemic financial crises\DISFR-web\src\api\api.ts
 * @Description: Systemic Financial Crises
 */
import request from "../utils/request.js";

const baseUrl = ''

// 指标构建
export const generateInd = (data: any) => {
  return request({
    url: baseUrl + "/generateInd",
    method: "post",
    data
  });
}
// 开始训练
export const startTrain = (data: any) => {
  return request({
    url: baseUrl + "/train",
    method: "post",
    data
  });
}
// 预测
export const startPredict = (data: any) => {
  return request({
    url: baseUrl + "/predict",
    method: "post",
    data
  });
}

// 获取模型列表
export const getModelsList = () => {
  return request({
    url: baseUrl + '/getModelsList',
    method: "get"
  });
}