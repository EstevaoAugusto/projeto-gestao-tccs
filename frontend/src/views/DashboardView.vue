<script setup>
import { ref, onMounted, computed } from 'vue'
import { useApi } from '@/composables/useApi'
import { Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'
import {
  DocumentTextIcon,
  UserGroupIcon,
  AcademicCapIcon,
  BookOpenIcon,
  CheckCircleIcon,
  ClockIcon,
  PaperAirplaneIcon,
  XCircleIcon,
} from '@heroicons/vue/24/outline'

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const api = useApi('tccs')
const stats = ref(null)
const loading = ref(true)

const counts = ref({ tccs: 0, alunos: 0, professores: 0, cursos: 0 })

async function loadData() {
  loading.value = true
  const [estatisticas, tccs, alunos, professores, cursos] = await Promise.all([
    api.custom('estatisticas/'),
    useApi('tccs').list(),
    useApi('alunos').list(),
    useApi('professores').list(),
    useApi('cursos').list(),
  ])
  stats.value = estatisticas
  counts.value = {
    tccs: Array.isArray(tccs) ? tccs.length : 0,
    alunos: Array.isArray(alunos) ? alunos.length : 0,
    professores: Array.isArray(professores) ? professores.length : 0,
    cursos: Array.isArray(cursos) ? cursos.length : 0,
  }
  loading.value = false
}

onMounted(loadData)

const statusColors = ['#a1a1aa', '#f59e0b', '#10b981', '#ef4444']
const statusChart = computed(() => {
  if (!stats.value) return null
  const s = stats.value.por_status
  return {
    data: {
      labels: Object.keys(s),
      datasets: [{
        data: Object.values(s),
        backgroundColor: statusColors,
        borderWidth: 0,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '60%',
      plugins: { legend: { position: 'bottom', labels: { padding: 16, usePointStyle: true, pointStyle: 'circle', font: { size: 12, family: 'Inter' } } } },
    },
  }
})

const tipoChart = computed(() => {
  if (!stats.value) return null
  const t = stats.value.por_tipo
  return {
    data: {
      labels: Object.keys(t),
      datasets: [{
        data: Object.values(t),
        backgroundColor: '#6366f1',
        borderRadius: 4,
        maxBarThickness: 32,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 11, family: 'Inter' } } },
        y: { grid: { display: false }, ticks: { font: { size: 12, family: 'Inter' } } },
      },
    },
  }
})

const semestreChart = computed(() => {
  if (!stats.value) return null
  const s = stats.value.por_semestre
  const sorted = Object.entries(s).sort((a, b) => a[0].localeCompare(b[0]))
  return {
    data: {
      labels: sorted.map(e => e[0]),
      datasets: [{
        data: sorted.map(e => e[1]),
        backgroundColor: '#6366f1',
        borderRadius: 4,
        maxBarThickness: 24,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 11, family: 'Inter' }, maxRotation: 45, minRotation: 45 } },
        y: { grid: { color: '#f4f4f5' }, ticks: { font: { size: 11, family: 'Inter' }, stepSize: 1 }, beginAtZero: true },
      },
    },
  }
})

const cursoChart = computed(() => {
  if (!stats.value) return null
  const c = stats.value.por_curso
  return {
    data: {
      labels: Object.keys(c),
      datasets: [{
        data: Object.values(c),
        backgroundColor: ['#6366f1', '#a1a1aa', '#10b981', '#f59e0b'],
        borderWidth: 0,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '60%',
      plugins: { legend: { position: 'bottom', labels: { padding: 16, usePointStyle: true, pointStyle: 'circle', font: { size: 12, family: 'Inter' } } } },
    },
  }
})

const summaryCards = computed(() => [
  { label: 'Total de TCCs', value: counts.value.tccs, icon: DocumentTextIcon, accent: 'text-indigo-600 bg-indigo-50' },
  { label: 'Alunos cadastrados', value: counts.value.alunos, icon: UserGroupIcon, accent: 'text-emerald-600 bg-emerald-50' },
  { label: 'Professores', value: counts.value.professores, icon: AcademicCapIcon, accent: 'text-amber-600 bg-amber-50' },
  { label: 'Cursos', value: counts.value.cursos, icon: BookOpenIcon, accent: 'text-sky-600 bg-sky-50' },
])

const statusCards = computed(() => {
  if (!stats.value) return []
  const s = stats.value.por_status
  return [
    { label: 'Em elaboração', value: s['Em Elaboração'] || 0, icon: ClockIcon, cls: 'text-zinc-600 bg-zinc-100' },
    { label: 'Enviados', value: s['Enviado'] || 0, icon: PaperAirplaneIcon, cls: 'text-amber-600 bg-amber-50' },
    { label: 'Aprovados', value: s['Aprovado'] || 0, icon: CheckCircleIcon, cls: 'text-emerald-600 bg-emerald-50' },
    { label: 'Reprovados', value: s['Reprovado'] || 0, icon: XCircleIcon, cls: 'text-red-600 bg-red-50' },
  ]
})
</script>

<template>
  <div class="space-y-6">
    <section>
      <h2 class="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-3">Resumo geral</h2>
      <div class="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <template v-if="loading">
          <div v-for="i in 4" :key="i" class="h-24 animate-pulse rounded-lg border border-zinc-200 bg-white" />
        </template>
        <article
          v-for="card in summaryCards"
          v-else
          :key="card.label"
          class="flex items-center gap-4 rounded-lg border border-zinc-200 bg-white px-4 py-4"
        >
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-md" :class="card.accent">
            <component :is="card.icon" class="h-5 w-5" />
          </div>
          <div>
            <p class="text-2xl font-semibold tracking-tight text-zinc-900">{{ card.value }}</p>
            <p class="text-xs text-zinc-500">{{ card.label }}</p>
          </div>
        </article>
      </div>
    </section>

    <section v-if="!loading && stats">
      <h2 class="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-3">Por status</h2>
      <div class="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <article
          v-for="card in statusCards"
          :key="card.label"
          class="flex items-center gap-4 rounded-lg border border-zinc-200 bg-white px-4 py-4"
        >
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-md" :class="card.cls">
            <component :is="card.icon" class="h-5 w-5" />
          </div>
          <div>
            <p class="text-2xl font-semibold tracking-tight text-zinc-900">{{ card.value }}</p>
            <p class="text-xs text-zinc-500">{{ card.label }}</p>
          </div>
        </article>
      </div>
    </section>

    <section v-if="!loading && stats" class="grid gap-6 lg:grid-cols-2">
      <article class="rounded-lg border border-zinc-200 bg-white p-6">
        <h3 class="mb-4 text-sm font-semibold text-zinc-700">Distribuição por status</h3>
        <div class="h-56">
          <Doughnut v-if="statusChart" :data="statusChart.data" :options="statusChart.options" />
        </div>
      </article>

      <article class="rounded-lg border border-zinc-200 bg-white p-6">
        <h3 class="mb-4 text-sm font-semibold text-zinc-700">TCCs por tipo</h3>
        <div class="h-56">
          <Bar v-if="tipoChart" :data="tipoChart.data" :options="tipoChart.options" />
        </div>
      </article>

      <article class="rounded-lg border border-zinc-200 bg-white p-6">
        <h3 class="mb-4 text-sm font-semibold text-zinc-700">TCCs por semestre letivo</h3>
        <div class="h-56">
          <Bar v-if="semestreChart" :data="semestreChart.data" :options="semestreChart.options" />
        </div>
      </article>

      <article class="rounded-lg border border-zinc-200 bg-white p-6">
        <h3 class="mb-4 text-sm font-semibold text-zinc-700">Distribuição por curso</h3>
        <div class="h-56">
          <Doughnut v-if="cursoChart" :data="cursoChart.data" :options="cursoChart.options" />
        </div>
      </article>
    </section>
  </div>
</template>
