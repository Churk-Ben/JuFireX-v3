import { ref } from 'vue'

export function usePagination(initialPage = 1, pageSize = 10) {
	const page = ref(initialPage)
	const size = ref(pageSize)
	const total = ref(0)
	const setTotal = (t: number) => (total.value = t)
	const next = () => (page.value += 1)
	const prev = () => (page.value = Math.max(1, page.value - 1))
	return { page, size, total, setTotal, next, prev }
}