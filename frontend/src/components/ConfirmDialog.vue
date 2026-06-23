<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

defineProps({
  message: { type: String, default: 'Tem certeza que deseja excluir este registro?' },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['confirm', 'cancel'])
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-zinc-900/40 px-4" @mousedown.self="emit('cancel')">
    <div class="w-full max-w-sm rounded-lg border border-zinc-200 bg-white p-6 shadow-sm" role="alertdialog">
      <div class="flex gap-4">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-red-50">
          <ExclamationTriangleIcon class="h-5 w-5 text-red-600" />
        </div>
        <div>
          <h3 class="text-sm font-semibold text-zinc-900">Confirmar exclusão</h3>
          <p class="mt-1 text-sm text-zinc-600">{{ message }}</p>
        </div>
      </div>
      <div class="mt-6 flex justify-end gap-3">
        <button
          type="button"
          class="rounded-md border border-zinc-200 bg-white px-3 py-1.5 text-sm font-medium text-zinc-700 hover:bg-zinc-50 transition-colors duration-150"
          :disabled="loading"
          @click="emit('cancel')"
        >
          Cancelar
        </button>
        <button
          type="button"
          class="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 transition-colors duration-150"
          :disabled="loading"
          @click="emit('confirm')"
        >
          {{ loading ? 'Excluindo...' : 'Excluir' }}
        </button>
      </div>
    </div>
  </div>
</template>
