<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, required: true },
})

const map = {
  '0': { label: 'Em elaboração', cls: 'border-zinc-300 bg-zinc-50 text-zinc-700' },
  '1': { label: 'Enviado', cls: 'border-amber-300 bg-amber-50 text-amber-800' },
  '2': { label: 'Aprovado', cls: 'border-emerald-300 bg-emerald-50 text-emerald-800' },
  '3': { label: 'Reprovado', cls: 'border-red-300 bg-red-50 text-red-800' },
}

const badge = computed(() => map[props.status] || map['0'])
</script>

<template>
  <span
    class="inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium"
    :class="badge.cls"
  >
    {{ badge.label }}
  </span>
</template>
