<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useApi } from '@/composables/useApi'
import { useToast } from '@/composables/useToast'
import BaseModal from '@/components/BaseModal.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import {
  PlusIcon,
  PencilSquareIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  ArrowDownTrayIcon,
  EyeIcon,
  XMarkIcon,
} from '@heroicons/vue/20/solid'

const api = useApi('tccs')
const toast = useToast()
const apiOrigin = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const items = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const errors = ref({})
const deleteTarget = ref(null)
const deleting = ref(false)
const deletingArquivo = ref(false)
const fileInputKey = ref(0)

const alunos = ref([])
const professores = ref([])

const tipoOptions = [
  { value: 'MONOGRAFIA', label: 'Monografia' },
  { value: 'RELATORIO_ESTAGIO', label: 'Relatório de estágio' },
  { value: 'RELATORIO_TECNICO', label: 'Relatório técnico' },
  { value: 'ARTIGO', label: 'Artigo' },
]

const idiomaOptions = [
  { value: 'PT', label: 'Português' },
  { value: 'EN', label: 'Inglês' },
]

const statusOptions = [
  { value: '0', label: 'Em elaboração' },
  { value: '1', label: 'Enviado' },
  { value: '2', label: 'Aprovado' },
  { value: '3', label: 'Reprovado' },
]

const semestreOptions = [
  '2020/1','2020/2','2021/1','2021/2','2022/1','2022/2',
  '2023/1','2023/2','2024/1','2024/2','2025/1','2025/2','2026/1',
]

const blankForm = () => ({
  titulo: '', resumo: '', palavras_chave: '', tipo: 'MONOGRAFIA', idioma: 'PT',
  aluno: '', orientador: '', coorientador: '', presidente: '',
  primeiro_membro: '', segundo_membro: '', semestre_letivo_defesa: '', status: '0', arquivo: null,
})
const form = reactive(blankForm())

async function fetchAll() {
  loading.value = true
  const [tccList, alunoList, profList] = await Promise.all([
    api.list(search.value),
    useApi('alunos').list(),
    useApi('professores').list(),
  ])
  items.value = tccList
  alunos.value = alunoList
  professores.value = profList
  loading.value = false
}

onMounted(fetchAll)

let debounce = null
watch(search, () => {
  clearTimeout(debounce)
  debounce = setTimeout(fetchAll, 300)
})

function alunoName(id) {
  const a = alunos.value.find(a => a.id === id)
  return a ? `${a.nome} (${a.matricula})` : `#${id}`
}
function profName(id) {
  if (!id) return '—'
  const p = professores.value.find(p => p.id === id)
  return p ? p.nome : `#${id}`
}

function openCreate() {
  editing.value = null
  errors.value = {}
  Object.assign(form, blankForm())
  showModal.value = true
}
function openEdit(item) {
  editing.value = item
  errors.value = {}
  Object.assign(form, {
    titulo: item.titulo,
    resumo: item.resumo,
    palavras_chave: item.palavras_chave,
    tipo: item.tipo,
    idioma: item.idioma,
    aluno: item.aluno,
    orientador: item.orientador,
    coorientador: item.coorientador || '',
    presidente: item.presidente,
    primeiro_membro: item.primeiro_membro,
    segundo_membro: item.segundo_membro,
    semestre_letivo_defesa: item.semestre_letivo_defesa || '',
    status: item.status,
    arquivo: null,
  })
  showModal.value = true
}

async function save() {
  saving.value = true
  errors.value = {}
  try {
    const hasFile = form.arquivo instanceof File
    let payload
    if (hasFile) {
      payload = new FormData()
      for (const [k, v] of Object.entries(form)) {
        if (k === 'arquivo') { if (v) payload.append(k, v) }
        else if (v !== '' && v !== null) payload.append(k, v)
      }
    } else {
      payload = {}
      for (const [k, v] of Object.entries(form)) {
        if (k === 'arquivo') continue
        if (v !== '' && v !== null) payload[k] = v
      }
    }
    if (editing.value) {
      await api.update(editing.value.id, payload, hasFile)
      toast.success('TCC atualizado.')
    } else {
      await api.create(payload, hasFile)
      toast.success('TCC cadastrado.')
    }
    showModal.value = false
    await fetchAll()
  } catch (e) {
    if (e.data) errors.value = e.data
    else toast.error('Falha ao salvar o TCC.')
  } finally {
    saving.value = false
  }
}

async function confirmDelete() {
  deleting.value = true
  try {
    await api.remove(deleteTarget.value.id)
    toast.success('TCC excluído.')
    deleteTarget.value = null
    await fetchAll()
  } catch {
    toast.error('Falha ao excluir.')
  } finally {
    deleting.value = false
  }
}

function onFileChange(e) {
  form.arquivo = e.target.files[0] || null
}

function arquivoUrl(arquivo) {
  if (!arquivo) return ''
  if (/^https?:\/\//.test(arquivo)) return arquivo
  return `${apiOrigin}${arquivo}`
}

function arquivoName(arquivo) {
  if (!arquivo) return ''
  return decodeURIComponent(arquivo.split('/').pop() || 'arquivo.pdf')
}

function visualizarArquivo(arquivo) {
  window.open(arquivoUrl(arquivo), '_blank', 'noopener')
}

function baixarArquivo(arquivo) {
  const a = document.createElement('a')
  a.href = arquivoUrl(arquivo)
  a.download = arquivoName(arquivo)
  a.click()
}

async function apagarArquivo() {
  if (!editing.value?.arquivo) return

  deletingArquivo.value = true
  try {
    const updated = await api.patch(editing.value.id, { arquivo: null })
    editing.value = updated
    const index = items.value.findIndex(item => item.id === updated.id)
    if (index !== -1) items.value[index] = updated
    form.arquivo = null
    fileInputKey.value += 1
    toast.success('Arquivo removido.')
  } catch {
    toast.error('Falha ao remover o arquivo.')
  } finally {
    deletingArquivo.value = false
  }
}

function exportCsv() {
  const header = ['Título', 'Aluno', 'Orientador', 'Tipo', 'Idioma', 'Status', 'Semestre']
  const rows = items.value.map(t => [
    t.titulo, alunoName(t.aluno), profName(t.orientador),
    t.tipo_display, t.idioma_display, t.status_display, t.semestre_letivo_defesa || '',
  ])
  const csv = [header, ...rows].map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'tccs.csv'
  a.click()
  URL.revokeObjectURL(a.href)
}

function fieldError(name) {
  const e = errors.value[name]
  return Array.isArray(e) ? e[0] : e
}
</script>

<template>
  <div class="space-y-4">
    <!-- Toolbar -->
    <div class="flex flex-wrap items-center gap-3">
      <div class="relative flex-1 min-w-[200px] max-w-sm">
        <MagnifyingGlassIcon class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
        <input
          v-model="search"
          type="search"
          placeholder="Buscar por título ou resumo..."
          class="w-full rounded-md border border-zinc-200 bg-white py-2 pl-9 pr-3 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-colors duration-150"
        />
      </div>
      <button
        type="button"
        class="inline-flex items-center gap-1.5 rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50 transition-colors duration-150"
        @click="exportCsv"
      >
        <ArrowDownTrayIcon class="h-4 w-4" />
        Exportar CSV
      </button>
      <button
        type="button"
        class="inline-flex items-center gap-1.5 rounded-md bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors duration-150"
        @click="openCreate"
      >
        <PlusIcon class="h-4 w-4" />
        Novo TCC
      </button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto rounded-lg border border-zinc-200 bg-white">
      <table class="w-full text-left text-sm">
        <thead>
          <tr class="border-b border-zinc-200 bg-zinc-50">
            <th class="px-4 py-3 font-medium text-zinc-600">Título</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Aluno</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Orientador</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Tipo</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Semestre</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Status</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Arquivo</th>
            <th class="px-4 py-3 font-medium text-zinc-600 w-24">Ações</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr v-for="i in 6" :key="i" class="border-b border-zinc-100">
              <td v-for="j in 8" :key="j" class="px-4 py-3">
                <div class="h-4 w-full animate-pulse rounded bg-zinc-100" />
              </td>
            </tr>
          </template>
          <tr v-else-if="items.length === 0">
            <td colspan="8" class="px-4 py-12 text-center text-sm text-zinc-400">
              Nenhum TCC encontrado.
            </td>
          </tr>
          <tr
            v-for="item in items"
            v-else
            :key="item.id"
            class="border-b border-zinc-100 hover:bg-zinc-50/60 transition-colors duration-150"
          >
            <td class="max-w-xs truncate px-4 py-3 font-medium text-zinc-900">{{ item.titulo }}</td>
            <td class="px-4 py-3 text-zinc-600 whitespace-nowrap">{{ alunoName(item.aluno) }}</td>
            <td class="px-4 py-3 text-zinc-600 whitespace-nowrap">{{ profName(item.orientador) }}</td>
            <td class="px-4 py-3 text-zinc-600 whitespace-nowrap">{{ item.tipo_display }}</td>
            <td class="px-4 py-3 text-zinc-600">{{ item.semestre_letivo_defesa || '—' }}</td>
            <td class="px-4 py-3"><StatusBadge :status="item.status" /></td>
            <td class="px-4 py-3">
              <div v-if="item.arquivo" class="flex gap-1">
                <button
                  type="button"
                  class="rounded p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 transition-colors duration-150"
                  :title="`Visualizar ${arquivoName(item.arquivo)}`"
                  @click="visualizarArquivo(item.arquivo)"
                >
                  <EyeIcon class="h-4 w-4" />
                </button>
                <button
                  type="button"
                  class="rounded p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 transition-colors duration-150"
                  :title="`Baixar ${arquivoName(item.arquivo)}`"
                  @click="baixarArquivo(item.arquivo)"
                >
                  <ArrowDownTrayIcon class="h-4 w-4" />
                </button>
              </div>
              <span v-else class="text-zinc-400">—</span>
            </td>
            <td class="px-4 py-3">
              <div class="flex gap-1">
                <button type="button" class="rounded p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 transition-colors duration-150" @click="openEdit(item)">
                  <PencilSquareIcon class="h-4 w-4" />
                </button>
                <button type="button" class="rounded p-1 text-zinc-400 hover:bg-red-50 hover:text-red-600 transition-colors duration-150" @click="deleteTarget = item">
                  <TrashIcon class="h-4 w-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="!loading" class="text-xs text-zinc-400">{{ items.length }} registro(s)</p>

    <!-- Modal -->
    <BaseModal
      v-if="showModal"
      :title="editing ? 'Editar TCC' : 'Novo TCC'"
      wide
      @close="showModal = false"
    >
      <form class="space-y-4" @submit.prevent="save">
        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Título</label>
          <input v-model="form.titulo" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
          <p v-if="fieldError('titulo')" class="mt-1 text-xs text-red-600">{{ fieldError('titulo') }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Resumo</label>
          <textarea v-model="form.resumo" rows="3" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
          <p v-if="fieldError('resumo')" class="mt-1 text-xs text-red-600">{{ fieldError('resumo') }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Palavras-chave</label>
          <input v-model="form.palavras_chave" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Tipo</label>
            <select v-model="form.tipo" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option v-for="o in tipoOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Idioma</label>
            <select v-model="form.idioma" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option v-for="o in idiomaOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Aluno</label>
            <select v-model="form.aluno" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="" disabled>Selecionar</option>
              <option v-for="a in alunos" :key="a.id" :value="a.id">{{ a.nome }} ({{ a.matricula }})</option>
            </select>
            <p v-if="fieldError('aluno')" class="mt-1 text-xs text-red-600">{{ fieldError('aluno') }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Status</label>
            <select v-model="form.status" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option v-for="o in statusOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Orientador</label>
            <select v-model="form.orientador" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="" disabled>Selecionar</option>
              <option v-for="p in professores" :key="p.id" :value="p.id">{{ p.nome }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Coorientador <span class="text-zinc-400 font-normal">(opcional)</span></label>
            <select v-model="form.coorientador" class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="">Nenhum</option>
              <option v-for="p in professores" :key="p.id" :value="p.id">{{ p.nome }}</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Presidente da banca</label>
            <select v-model="form.presidente" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="" disabled>Selecionar</option>
              <option v-for="p in professores" :key="p.id" :value="p.id">{{ p.nome }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">1º membro</label>
            <select v-model="form.primeiro_membro" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="" disabled>Selecionar</option>
              <option v-for="p in professores" :key="p.id" :value="p.id">{{ p.nome }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">2º membro</label>
            <select v-model="form.segundo_membro" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="" disabled>Selecionar</option>
              <option v-for="p in professores" :key="p.id" :value="p.id">{{ p.nome }}</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Semestre letivo da defesa</label>
            <select v-model="form.semestre_letivo_defesa" class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="">Não definido</option>
              <option v-for="s in semestreOptions" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Arquivo <span class="text-zinc-400 font-normal">(PDF)</span></label>
            <div v-if="editing?.arquivo" class="mb-2 flex items-center justify-between gap-3 rounded-md border border-zinc-200 bg-zinc-50 px-3 py-2">
              <span class="min-w-0 truncate text-sm text-zinc-700">{{ arquivoName(editing.arquivo) }}</span>
              <div class="flex shrink-0 gap-1">
                <button
                  type="button"
                  class="rounded p-1 text-zinc-500 hover:bg-white hover:text-zinc-900 transition-colors duration-150"
                  :title="`Visualizar ${arquivoName(editing.arquivo)}`"
                  @click="visualizarArquivo(editing.arquivo)"
                >
                  <EyeIcon class="h-4 w-4" />
                </button>
                <button
                  type="button"
                  class="rounded p-1 text-zinc-500 hover:bg-white hover:text-zinc-900 transition-colors duration-150"
                  :title="`Baixar ${arquivoName(editing.arquivo)}`"
                  @click="baixarArquivo(editing.arquivo)"
                >
                  <ArrowDownTrayIcon class="h-4 w-4" />
                </button>
                <button
                  type="button"
                  class="rounded p-1 text-zinc-500 hover:bg-red-50 hover:text-red-600 disabled:opacity-50 transition-colors duration-150"
                  :disabled="deletingArquivo"
                  :title="`Remover ${arquivoName(editing.arquivo)}`"
                  @click="apagarArquivo"
                >
                  <XMarkIcon class="h-4 w-4" />
                </button>
              </div>
            </div>
            <input :key="fileInputKey" type="file" accept="application/pdf,.pdf" class="w-full rounded-md border border-zinc-200 px-3 py-1.5 text-sm text-zinc-900 file:mr-3 file:rounded file:border-0 file:bg-zinc-100 file:px-2 file:py-1 file:text-xs file:font-medium file:text-zinc-700 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" @change="onFileChange" />
            <p v-if="fieldError('arquivo')" class="mt-1 text-xs text-red-600">{{ fieldError('arquivo') }}</p>
          </div>
        </div>
      </form>

      <template #footer>
        <button
          type="button"
          class="rounded-md border border-zinc-200 bg-white px-4 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50 transition-colors duration-150"
          @click="showModal = false"
        >
          Cancelar
        </button>
        <button
          type="button"
          class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors duration-150"
          :disabled="saving"
          @click="save"
        >
          {{ saving ? 'Salvando...' : (editing ? 'Atualizar' : 'Cadastrar') }}
        </button>
      </template>
    </BaseModal>

    <ConfirmDialog
      v-if="deleteTarget"
      :message="`Excluir o TCC '${deleteTarget.titulo}'?`"
      :loading="deleting"
      @confirm="confirmDelete"
      @cancel="deleteTarget = null"
    />
  </div>
</template>
