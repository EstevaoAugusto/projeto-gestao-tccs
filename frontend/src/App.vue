<script setup>
import { computed, onMounted, ref } from 'vue'

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const healthEndpoint = `${apiUrl}/api/health/`

const loading = ref(true)
const errorMessage = ref('')
const backendStatus = ref('checking')
const databaseStatus = ref('checking')
const backendMessage = ref('Aguardando resposta da API Django.')
const databaseMessage = ref('Aguardando consulta ao PostgreSQL.')
const lastCheckedAt = ref('')

const allHealthy = computed(
  () => backendStatus.value === 'healthy' && databaseStatus.value === 'healthy',
)

async function checkHealth() {
  loading.value = true
  errorMessage.value = ''
  backendStatus.value = 'checking'
  databaseStatus.value = 'checking'

  try {
    const response = await fetch(healthEndpoint)
    const data = await response.json()

    backendStatus.value = data.services?.backend?.status || 'unhealthy'
    databaseStatus.value = data.services?.database?.status || 'unhealthy'
    backendMessage.value = data.services?.backend?.message || 'Backend sem mensagem.'
    databaseMessage.value = data.services?.database?.message || 'Banco sem mensagem.'

    if (!response.ok) {
      errorMessage.value = 'A API respondeu, mas algum servico ainda nao esta saudavel.'
    }
  } catch (error) {
    backendStatus.value = 'unhealthy'
    databaseStatus.value = 'unknown'
    backendMessage.value = 'Nao foi possivel conectar ao backend.'
    databaseMessage.value = 'Sem resposta do backend para validar o banco.'
    errorMessage.value = error instanceof Error ? error.message : 'Erro desconhecido.'
  } finally {
    loading.value = false
    lastCheckedAt.value = new Date().toLocaleString('pt-BR')
  }
}

onMounted(checkHealth)
</script>

<template>
  <main class="status-page">
    <section class="hero">
      <p class="eyebrow">Ambiente Docker em execucao</p>
      <h1>Projeto Gestao de TCCs</h1>
      <p class="summary">
        Esta pagina confirma se o frontend Vue.js, o backend Django REST Framework
        e o banco PostgreSQL estao respondendo corretamente apos subir os containers.
      </p>

      <div class="banner" :class="{ healthy: allHealthy, warning: !allHealthy }">
        <span class="banner-dot"></span>
        <div>
          <strong>{{ allHealthy ? 'Tudo funcionando corretamente' : 'Verificando servicos' }}</strong>
          <p>
            {{
              allHealthy
                ? 'Frontend, backend e banco de dados estao saudaveis.'
                : 'Confira abaixo qual servico ainda precisa responder.'
            }}
          </p>
        </div>
      </div>
    </section>

    <section class="status-grid" aria-label="Status dos servicos">
      <article class="status-card healthy">
        <span class="status-label">Frontend</span>
        <h2>Vue.js</h2>
        <p>Aplicacao carregada pelo Vite na porta 5173.</p>
        <strong>healthy</strong>
      </article>

      <article class="status-card" :class="backendStatus">
        <span class="status-label">Backend</span>
        <h2>Django REST Framework</h2>
        <p>{{ backendMessage }}</p>
        <strong>{{ backendStatus }}</strong>
      </article>

      <article class="status-card" :class="databaseStatus">
        <span class="status-label">Banco de dados</span>
        <h2>PostgreSQL</h2>
        <p>{{ databaseMessage }}</p>
        <strong>{{ databaseStatus }}</strong>
      </article>
    </section>

    <section class="actions">
      <button type="button" :disabled="loading" @click="checkHealth">
        {{ loading ? 'Verificando...' : 'Verificar novamente' }}
      </button>
      <p v-if="lastCheckedAt">Ultima verificacao: {{ lastCheckedAt }}</p>
      <p v-if="errorMessage" class="error">Detalhe: {{ errorMessage }}</p>
    </section>
  </main>
</template>
