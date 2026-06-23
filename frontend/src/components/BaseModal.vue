<script setup>
import { XMarkIcon } from '@heroicons/vue/20/solid'

defineProps({
  title: { type: String, required: true },
  wide: { type: Boolean, default: false },
})
const emit = defineEmits(['close'])
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-zinc-900/40 px-4 pt-16 pb-8" @mousedown.self="emit('close')">
    <div
      class="w-full rounded-lg border border-zinc-200 bg-white shadow-sm"
      :class="wide ? 'max-w-2xl' : 'max-w-lg'"
      role="dialog"
      aria-modal="true"
    >
      <header class="flex items-center justify-between border-b border-zinc-200 px-6 py-4">
        <h2 class="text-base font-semibold text-zinc-900">{{ title }}</h2>
        <button
          type="button"
          class="rounded-md p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-600"
          @click="emit('close')"
        >
          <XMarkIcon class="h-5 w-5" />
        </button>
      </header>
      <div class="px-6 py-4">
        <slot />
      </div>
      <footer v-if="$slots.footer" class="flex items-center justify-end gap-3 border-t border-zinc-200 px-6 py-4">
        <slot name="footer" />
      </footer>
    </div>
  </div>
</template>
