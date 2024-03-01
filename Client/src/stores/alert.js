// alert.js
import { reactive } from 'vue'

export const alertStore = reactive({
  display: false,
  text: 'This is a test message.',
  type: 'warning',
  title: 'Test',
  overRide: false,
  showError(text, title = 'Error', overRide = false) {
    this.text = text
    this.type = 'error'
    this.title = title
    this.overRide = overRide
    this.display = true
  },
  showWarning(text, title = 'Warning', overRide = false) {
    this.text = text
    this.type = 'warning'
    this.title = title
    this.overRide = overRide
    this.display = true
  },
  showInfo(text, title = 'Info', overRide = false) {
    this.text = text
    this.type = 'info'
    this.title = title
    this.overRide = overRide
    this.display = true
  },
  showSuccess(text, title = 'Success', overRide = false) {
    this.text = text
    this.type = 'success'
    this.title = title
    this.overRide = overRide
    this.display = true
  },
  hideAlert() {
    this.display = false
  }
})
