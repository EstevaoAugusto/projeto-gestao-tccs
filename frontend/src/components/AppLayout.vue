<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import {
  ChartBarIcon,
  DocumentTextIcon,
  UserGroupIcon,
  AcademicCapIcon,
  BookOpenIcon,
  BuildingOfficeIcon,
  BuildingLibraryIcon,
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/vue/24/outline'
import ToastContainer from './ToastContainer.vue'
import ThemeToggle from './ThemeToggle.vue'

const route = useRoute()
const sidebarOpen = ref(false)

const nav = [
  { to: '/', label: 'Painel geral', icon: ChartBarIcon },
  { to: '/tccs', label: 'TCCs', icon: DocumentTextIcon },
  { to: '/alunos', label: 'Alunos', icon: UserGroupIcon },
  { to: '/professores', label: 'Professores', icon: AcademicCapIcon },
  { to: '/cursos', label: 'Cursos', icon: BookOpenIcon },
  { to: '/departamentos', label: 'Departamentos', icon: BuildingOfficeIcon },
  { to: '/unidades', label: 'Unidades acadêmicas', icon: BuildingLibraryIcon },
]

function isActive(to) {
  if (to === '/') return route.path === '/'
  return route.path.startsWith(to)
}
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-zinc-50 text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-30 bg-zinc-900/30 lg:hidden dark:bg-zinc-950/60"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-zinc-200 bg-white transition-transform duration-150 ease-in-out dark:border-zinc-800 dark:bg-zinc-900 lg:static lg:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="flex h-14 items-center gap-3 border-b border-zinc-200 px-6 dark:border-zinc-800">
        <DocumentTextIcon class="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
        <span class="text-sm font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">Gestão de TCCs</span>
      </div>

      <nav class="flex-1 overflow-y-auto px-3 py-4">
        <ul class="space-y-0.5">
          <li v-for="item in nav" :key="item.to">
            <RouterLink
              :to="item.to"
              class="group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors duration-150"
              :class="isActive(item.to)
                ? 'bg-indigo-50 text-indigo-700 border-l-2 border-indigo-600 -ml-px dark:bg-indigo-500/10 dark:text-indigo-300 dark:border-indigo-400'
                : 'text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white'"
              @click="sidebarOpen = false"
            >
              <component :is="item.icon" class="h-[18px] w-[18px] shrink-0" />
              {{ item.label }}
            </RouterLink>
          </li>
        </ul>
      </nav>

      <div class="border-t border-zinc-200 px-6 py-3 dark:border-zinc-800">
        <p class="text-xs text-zinc-400 dark:text-zinc-500">UFLA — GAC116</p>
      </div>
    </aside>

    <!-- Main -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <header class="flex h-14 items-center gap-4 border-b border-zinc-200 bg-white px-4 dark:border-zinc-800 dark:bg-zinc-900 lg:px-8">
        <button
          type="button"
          class="rounded-md p-1.5 text-zinc-500 hover:bg-zinc-100 hover:text-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white lg:hidden"
          @click="sidebarOpen = true"
        >
          <Bars3Icon class="h-5 w-5" />
        </button>
        <h1 class="min-w-0 flex-1 text-sm font-semibold text-zinc-900 dark:text-zinc-100">
          {{ nav.find(n => isActive(n.to))?.label || 'Painel geral' }}
        </h1>
        <ThemeToggle />
      </header>

      <main class="flex-1 overflow-y-auto p-4 dark:bg-zinc-950 lg:p-8">
        <slot />
      </main>
    </div>

    <ToastContainer />
  </div>
</template>
