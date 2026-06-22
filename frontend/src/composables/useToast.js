import { ref } from 'vue'

const toasts = ref([])
let uid = 0

export function useToast() {
  function show(message, type = 'success', duration = 3500) {
    const id = ++uid
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, duration)
  }

  function success(msg) { show(msg, 'success') }
  function error(msg) { show(msg, 'error', 5000) }

  return { toasts, show, success, error }
}
