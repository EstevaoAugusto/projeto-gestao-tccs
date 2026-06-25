<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useApi } from '@/composables/useApi'
import { useToast } from '@/composables/useToast'
import BaseModal from '@/components/BaseModal.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { PlusIcon, PencilSquareIcon, TrashIcon, MagnifyingGlassIcon } from '@heroicons/vue/20/solid'

const api = useApi('professores')
const toast = useToast()

const items = ref([])
const departamentos = ref([])
const loading = ref(true)
const search = ref('')
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const errors = ref({})
const deleteTarget = ref(null)
const deleting = ref(false)

const form = reactive({ nome: '', departamento: '' })

async function fetchAll() {
  loading.value = true
  const [profList, deptoList] = await Promise.all([
    api.list(search.value),
    useApi('departamentos').list(),
  ])
  items.value = profList
  departamentos.value = deptoList
  loading.value = false
}

onMounted(fetchAll)
let debounce = null
watch(search, () => { clearTimeout(debounce); debounce = setTimeout(fetchAll, 300) })

function deptoName(id) {
  const d = departamentos.value.find(d => d.id === id)
  return d ? `${d.nome} (${d.sigla})` : `#${id}`
}

function openCreate() {
  editing.value = null; errors.value = {}
  Object.assign(form, { nome: '', departamento: '' })
  showModal.value = true
}
function openEdit(item) {
  editing.value = item; errors.value = {}
  Object.assign(form, { nome: item.nome, departamento: item.departamento })
  showModal.value = true
}

async function save() {
  saving.value = true; errors.value = {}
  try {
    if (editing.value) {
      await api.update(editing.value.id, { ...form })
      toast.success('Professor atualizado.')
    } else {
      await api.create({ ...form })
      toast.success('Professor cadastrado.')
    }
    showModal.value = false
    await fetchAll()
  } catch (e) {
    if (e.data) errors.value = e.data
    else toast.error('Falha ao salvar.')
  } finally { saving.value = false }
}

async function confirmDelete() {
  deleting.value = true
  try {
    await api.remove(deleteTarget.value.id)
    toast.success('Professor excluído.')
    deleteTarget.value = null
    await fetchAll()
  } catch { toast.error('Falha ao excluir.') }
  finally { deleting.value = false }
}

function fieldError(n) { const e = errors.value[n]; return Array.isArray(e) ? e[0] : e }
</script>

<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center gap-3">
      <div class="relative flex-1 min-w-[200px] max-w-sm">
        <MagnifyingGlassIcon class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
        <input v-model="search" type="search" placeholder="Buscar por nome..." class="w-full rounded-md border border-zinc-200 bg-white py-2 pl-9 pr-3 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
      </div>
      <button type="button" class="inline-flex items-center gap-1.5 rounded-md bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors duration-150" @click="openCreate">
        <PlusIcon class="h-4 w-4" /> Novo professor
      </button>
    </div>

    <div class="overflow-x-auto rounded-lg border border-zinc-200 bg-white">
      <table class="w-full text-left text-sm">
        <thead>
          <tr class="border-b border-zinc-200 bg-zinc-50">
            <th class="px-4 py-3 font-medium text-zinc-600">Nome</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Departamento</th>
            <th class="px-4 py-3 font-medium text-zinc-600 w-24">Ações</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr v-for="i in 6" :key="i" class="border-b border-zinc-100">
              <td v-for="j in 3" :key="j" class="px-4 py-3"><div class="h-4 w-full animate-pulse rounded bg-zinc-100" /></td>
            </tr>
          </template>
          <tr v-else-if="items.length === 0"><td colspan="3" class="px-4 py-12 text-center text-sm text-zinc-400">Nenhum professor encontrado.</td></tr>
          <tr v-for="item in items" v-else :key="item.id" class="border-b border-zinc-100 hover:bg-zinc-50/60 transition-colors duration-150">
            <td class="px-4 py-3 font-medium text-zinc-900">{{ item.nome }}</td>
            <td class="px-4 py-3 text-zinc-600">{{ deptoName(item.departamento) }}</td>
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

    <BaseModal v-if="showModal" :title="editing ? 'Editar professor' : 'Novo professor'" @close="showModal = false">
      <form class="space-y-4" @submit.prevent="save">
        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Nome</label>
          <input v-model="form.nome" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
          <p v-if="fieldError('nome')" class="mt-1 text-xs text-red-600">{{ fieldError('nome') }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Departamento</label>
          <select v-model="form.departamento" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
            <option value="" disabled>Selecionar</option>
            <option v-for="d in departamentos" :key="d.id" :value="d.id">{{ d.nome }} ({{ d.sigla }})</option>
          </select>
          <p v-if="fieldError('departamento')" class="mt-1 text-xs text-red-600">{{ fieldError('departamento') }}</p>
        </div>
      </form>
      <template #footer>
        <button type="button" class="rounded-md border border-zinc-200 bg-white px-4 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50" @click="showModal = false">Cancelar</button>
        <button type="button" class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700" :disabled="saving" @click="save">{{ saving ? 'Salvando...' : (editing ? 'Atualizar' : 'Cadastrar') }}</button>
      </template>
    </BaseModal>

    <ConfirmDialog v-if="deleteTarget" :message="`Excluir o professor '${deleteTarget.nome}'?`" :loading="deleting" @confirm="confirmDelete" @cancel="deleteTarget = null" />
  </div>
</template>
