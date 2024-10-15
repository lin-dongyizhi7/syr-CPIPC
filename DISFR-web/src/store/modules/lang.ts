import { defineStore } from 'pinia'
interface ILanguage {
  language: string
}

export const useLangStore = defineStore('lang', {
  state: (): ILanguage => {
    return {
      language: sessionStorage.getItem('localeLang') || 'zhCn',
    }
  },
  actions: {
    changeLang(data: 'zhCn' | 'en') {
      this.language = data
    },
  },
  persist: true,
})
