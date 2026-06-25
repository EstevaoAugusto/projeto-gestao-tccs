<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { useToast } from '@/composables/useToast'
import BaseModal from '@/components/BaseModal.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { PlusIcon, PencilSquareIcon, TrashIcon } from '@heroicons/vue/20/solid'

const api = useApi('departamentos')
const toast = useToast()

const items = ref([])
const unidades = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const errors = ref({})
const deleteTarget = ref(null)
const deleting = ref(false)

const form = reactive({ nome: '', sigla: '', unidade_academica: '' })

async function fetchAll() {
  loading.value = true
  const [deptoList, unidadeList] = await Promise.all([
    api.list(),
    useApi('unidades-academicas').list(),
  ])
  items.value = deptoList
  unidades.value = unidadeList
  loading.value = false
}
onMounted(fetchAll)

function unidadeName(id) {
  const u = unidades.value.find(u => u.id === id)
  return u ? `${u.nome} (${u.sigla})` : `#${id}`
}

function openCreate() {
  editing.value = null; errors.value = {}
  Object.assign(form, { nome: '', sigla: '', unidade_academica: '' })
  showModal.value = true
}
function openEdit(item) {
  editing.value = item; errors.value = {}
  Object.assign(form, { nome: item.nome, sigla: item.sigla, unidade_academica: item.unidade_academica })
  showModal.value = true
}

async function save() {
  saving.value = true; errors.value = {}
  try {
    if (editing.value) {
      await api.update(editing.value.id, { ...form })
      toast.success('Departamento atualizado.')
    } else {
      await api.create({ ...form })
      toast.success('Departamento cadastrado.')
    }
    showModal.value = false; await fetchAll()
  } catch (e) {
    if (e.data) errors.value = e.data
    else toast.error('Falha ao salvar.')
  } finally { saving.value = false }
}

async function confirmDelete() {
  deleting.value = true
  try {
    await api.remove(deleteTarget.value.id)
    toast.success('Departamento excluído.')
    deleteTarget.value = null; await fetchAll()
  } catch { toast.error('Falha ao excluir.') }
  finally { deleting.value = false }
}

function fieldError(n) { const e = errors.value[n]; return Array.isArray(e) ? e[0] : e }
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-end">
      <button type="button" class="inline-flex items-center gap-1.5 rounded-md bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors duration-150" @click="openCreate">
        <PlusIcon class="h-4 w-4" /> Novo departamento
      </button>
    </div>

    <div class="overflow-x-auto rounded-lg border border-zinc-200 bg-white">
      <table class="w-full text-left text-sm">
        <thead>
          <tr class="border-b border-zinc-200 bg-zinc-50">
            <th class="px-4 py-3 font-medium text-zinc-600">Nome</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Sigla</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Unidade acadêmica</th>
            <th class="px-4 py-3 font-medium text-zinc-600 w-24">Ações</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr v-for="i in 4" :key="i" class="border-b border-zinc-100">
              <td v-for="j in 4" :key="j" class="px-4 py-3"><div class="h-4 w-full animate-pulse rounded bg-zinc-100" /></td>
            </tr>
          </template>
          <tr v-else-if="items.length === 0"><td colspan="4" class="px-4 py-12 text-center text-sm text-zinc-400">Nenhum departamento cadastrado.</td></tr>
          <tr v-for="item in items" v-else :key="item.id" class="border-b border-zinc-100 hover:bg-zinc-50/60 transition-colors duration-150">
            <td class="px-4 py-3 font-medium text-zinc-900">{{ item.nome }}</td>
            <td class="px-4 py-3 text-zinc-600 font-mono text-xs">{{ item.sigla }}</td>
            <td class="px-4 py-3 text-zinc-600">{{ unidadeName(item.unidade_academica) }}</td>
            <td class="px-4 py-3">
              <div class="flex gap-1">
                <button type="button" class="rounded p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 transition-colors duration-150" @click="openEdit(item)"><PencilSquareIcon class="h-4 w-4" /></button>
                <button type="button" class="rounded p-1 text-zinc-400 hover:bg-red-50 hover:text-red-600 transition-colors duration-150" @click="deleteTarget = item"><TrashIcon class="h-4 w-4" /></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="!loading" class="text-xs text-zinc-400">{{ items.length }} registro(s)</p>

    <BaseModal v-if="showModal" :title="editing ? 'Editar departamento' : 'Novo departamento'" @close="showModal = false">
      <form class="space-y-4" @submit.prevent="save">
        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Nome</label>
          <input v-model="form.nome" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
          <p v-if="fieldError('nome')" class="mt-1 text-xs text-red-600">{{ fieldError('nome') }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Sigla</label>
          <input v-model="form.sigla" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
          <p v-if="fieldError('sigla')" class="mt-1 text-xs text-red-600">{{ fieldError('sigla') }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Unidade acadêmica</label>
          <select v-model="form.unidade_academica" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
            <option value="" disabled>Selecionar</option>
            <option v-for="u in unidades" :key="u.id" :value="u.id">{{ u.nome }} ({{ u.sigla }})</option>
          </select>
          <p v-if="fieldError('unidade_academica')" class="mt-1 text-xs text-red-600">{{ fieldError('unidade_academica') }}</p>
        </div>
      </form>
      <template #footer>
        <button type="button" class="rounded-md border border-zinc-200 bg-white px-4 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50" @click="showModal = false">Cancelar</button>
        <button type="button" class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700" :disabled="saving" @click="save">{{ saving ? 'Salvando...' : (editing ? 'Atualizar' : 'Cadastrar') }}</button>
      </template>
    </BaseModal>

    <ConfirmDialog v-if="deleteTarget" :message="`Excluir o departamento '${deleteTarget.nome}'?`" :loading="deleting" @confirm="confirmDelete" @cancel="deleteTarget = null" />
  </div>
</template>
