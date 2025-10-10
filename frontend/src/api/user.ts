import http from '@/utils/request'

export function login(email: string, password: string) {
  return http.post('/users/login', { email, password })
}