import http from '@/utils/request'

export function listPosts() {
  return http.get('/posts')
}