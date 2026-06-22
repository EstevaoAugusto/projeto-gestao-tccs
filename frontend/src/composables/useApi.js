const BASE = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api`

async function request(url, options = {}) {
  const res = await fetch(url, options)
  if (options.method === 'DELETE' && res.status === 204) return null
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const err = new Error(res.statusText)
    err.status = res.status
    err.data = data
    throw err
  }
  return data
}

export function useApi(resource) {
  const url = `${BASE}/${resource}/`

  return {
    list(search = '') {
      const q = search ? `?search=${encodeURIComponent(search)}` : ''
      return request(`${url}${q}`)
    },
    get(id) {
      return request(`${url}${id}/`)
    },
    create(data, isFormData = false) {
      const opts = { method: 'POST', body: isFormData ? data : JSON.stringify(data) }
      if (!isFormData) opts.headers = { 'Content-Type': 'application/json' }
      return request(url, opts)
    },
    update(id, data, isFormData = false) {
      const opts = { method: 'PUT', body: isFormData ? data : JSON.stringify(data) }
      if (!isFormData) opts.headers = { 'Content-Type': 'application/json' }
      return request(`${url}${id}/`, opts)
    },
    patch(id, data) {
      return request(`${url}${id}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
    },
    remove(id) {
      return request(`${url}${id}/`, { method: 'DELETE' })
    },
    custom(path) {
      return request(`${url}${path}`)
    },
  }
}
