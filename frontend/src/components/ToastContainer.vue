<script setup>
import { useToast } from '@/composables/useToast'
import { CheckCircleIcon, ExclamationCircleIcon, XMarkIcon } from '@heroicons/vue/20/solid'

const { toasts } = useToast()

function dismiss(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}
</script>

<template>
  <div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2" aria-live="polite">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="flex items-center gap-2 rounded-md border px-4 py-3 text-sm font-medium shadow-sm transition-all duration-150"
      :class="toast.type === 'error'
        ? 'border-red-200 bg-red-50 text-red-800'
        : 'border-emerald-200 bg-emerald-50 text-emerald-800'"
    >
      <CheckCircleIcon v-if="toast.type === 'success'" class="h-4 w-4 shrink-0 text-emerald-600" />
      <ExclamationCircleIcon v-else class="h-4 w-4 shrink-0 text-red-600" />
      <span>{{ toast.message }}</span>
      <button
        type="button"
        class="ml-2 rounded p-0.5 hover:bg-black/5"
        @click="dismiss(toast.id)"
      >
        <XMarkIcon class="h-3.5 w-3.5" />
      </button>
    </div>
  </div>
</template>
