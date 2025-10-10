import { describe, it, expect } from 'vitest'
import { formatDate } from '@/utils/format'

describe('formatDate', () => {
  it('formats timestamp to ISO', () => {
    const iso = formatDate(0)
    expect(iso).toContain('1970-01-01')
  })
})