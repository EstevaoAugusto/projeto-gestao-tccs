<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { useToast } from '@/composables/useToast'
import BaseModal from '@/components/BaseModal.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { PlusIcon, PencilSquareIcon, TrashIcon } from '@heroicons/vue/20/solid'

const api = useApi('cursos')
const toast = useToast()

const items = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const errors = ref({})
const deleteTarget = ref(null)
const deleting = ref(false)

const form = reactive({ nome: '', sigla: '', codigo: '' })

async function fetchAll() {
  loading.value = true
  items.value = await api.list()
  loading.value = false
}
onMounted(fetchAll)

function openCreate() {
  editing.value = null; errors.value = {}
  Object.assign(form, { nome: '', sigla: '', codigo: '' })
  showModal.value = true
}
function openEdit(item) {
  editing.value = item; errors.value = {}
  Object.assign(form, { nome: item.nome, sigla: item.sigla, codigo: item.codigo })
  showModal.value = true
}

async function save() {
  saving.value = true; errors.value = {}
  try {
    if (editing.value) {
      await api.update(editing.value.id, { ...form })
      toast.success('Curso atualizado.')
    } else {
      await api.create({ ...form })
      toast.success('Curso cadastrado.')
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
    toast.success('Curso excluído.')
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
        <PlusIcon class="h-4 w-4" /> Novo curso
      </button>
    </div>

    <div class="overflow-x-auto rounded-lg border border-zinc-200 bg-white">
      <table class="w-full text-left text-sm">
        <thead>
          <tr class="border-b border-zinc-200 bg-zinc-50">
            <th class="px-4 py-3 font-medium text-zinc-600">Nome</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Sigla</th>
            <th class="px-4 py-3 font-medium text-zinc-600">Código</th>
            <th class="px-4 py-3 font-medium text-zinc-600 w-24">Ações</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr v-for="i in 4" :key="i" class="border-b border-zinc-100">
              <td v-for="j in 4" :key="j" class="px-4 py-3"><div class="h-4 w-full animate-pulse rounded bg-zinc-100" /></td>
            </tr>
          </template>
          <tr v-else-if="items.length === 0"><td colspan="4" class="px-4 py-12 text-center text-sm text-zinc-400">Nenhum curso cadastrado.</td></tr>
          <tr v-else v-for="item in items" :key="item.id" class="border-b border-zinc-100 hover:bg-zinc-50/60 transition-colors duration-150">
            <td class="px-4 py-3 font-medium text-zinc-900">{{ item.nome }}</td>
            <td class="px-4 py-3 text-zinc-600 font-mono text-xs">{{ item.sigla }}</td>
            <td class="px-4 py-3 text-zinc-600 font-mono text-xs">{{ item.codigo }}</td>
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

    <BaseModal v-if="showModal" :title="editing ? 'Editar curso' : 'Novo curso'" @close="showModal = false">
      <form @submit.prevent="save" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-zinc-700 mb-1">Nome</label>
          <input v-model="form.nome" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
          <p v-if="fieldError('nome')" class="mt-1 text-xs text-red-600">{{ fieldError('nome') }}</p>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Sigla</label>
            <input v-model="form.sigla" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
            <p v-if="fieldError('sigla')" class="mt-1 text-xs text-red-600">{{ fieldError('sigla') }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-zinc-700 mb-1">Código</label>
            <input v-model="form.codigo" type="text" required class="w-full rounded-md border border-zinc-200 px-3 py-2 text-sm text-zinc-900 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
            <p v-if="fieldError('codigo')" class="mt-1 text-xs text-red-600">{{ fieldError('codigo') }}</p>
          </div>
        </div>
      </form>
      <template #footer>
        <button type="button" class="rounded-md border border-zinc-200 bg-white px-4 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50" @click="showModal = false">Cancelar</button>
        <button type="button" class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700" :disabled="saving" @click="save">{{ saving ? 'Salvando...' : (editing ? 'Atualizar' : 'Cadastrar') }}</button>
      </template>
    </BaseModal>

    <ConfirmDialog v-if="deleteTarget" :message="`Excluir o curso '${deleteTarget.nome}'?`" :loading="deleting" @confirm="confirmDelete" @cancel="deleteTarget = null" />
  </div>
</template>
