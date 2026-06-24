<script setup>
import { onMounted, ref } from 'vue'
import { MoonIcon, SunIcon } from '@heroicons/vue/24/outline'

const STORAGE_KEY = 'theme'
const isDark = ref(false)

function applyTheme(value) {
  isDark.value = value
  document.documentElement.classList.toggle('dark', value)
  document.documentElement.style.colorScheme = value ? 'dark' : 'light'
  localStorage.setItem(STORAGE_KEY, value ? 'dark' : 'light')
}

function getInitialTheme() {
  const savedTheme = localStorage.getItem(STORAGE_KEY)
  if (savedTheme) return savedTheme === 'dark'
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function toggleTheme() {
  applyTheme(!isDark.value)
}

onMounted(() => {
  applyTheme(getInitialTheme())
})
</script>

<template>
  <button
    type="button"
    class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-zinc-200 bg-white text-zinc-600 transition-colors duration-150 hover:bg-zinc-100 hover:text-zinc-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white dark:focus:ring-offset-zinc-950"
    :aria-label="isDark ? 'Ativar tema claro' : 'Ativar tema escuro'"
    :title="isDark ? 'Tema claro' : 'Tema escuro'"
    @click="toggleTheme"
  >
    <SunIcon v-if="isDark" class="h-5 w-5" />
    <MoonIcon v-else class="h-5 w-5" />
  </button>
</template>
