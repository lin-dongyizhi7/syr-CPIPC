import { defineStore } from "pinia";
type langType = "zhCn" | 'en'
interface ILanguage {
  language: langType;
}

export const useLangStore = defineStore("lang", {
  state: (): ILanguage => {
    return {
      language: sessionStorage.getItem("localeLang") as langType || "zhCn",
    };
  },
  getters: {},
  actions: {
    changeLang(data: "zhCn" | "en") {
      this.language = data;
    },
  },
});
