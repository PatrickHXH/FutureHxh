import request from '@/utils/request'

class ProjectApi {
  create(data) {
    return request({
      url: '/api/projects/create/',
      method: 'post',
      data
    })
  }
  update(id, data) {
    return request({
      url: '/api/projects/update/' + id + '/',
      method: 'post',
      data
    })
  }
  delete(id) {
    return request({
      url: '/api/projects/delete/' + id + '/',
      method: 'post'
    })
  }
  getdetail(id) {
    return request({
      url: '/api/projects/detail/' + id + '/',
      method: 'get'
    })
  }
  getlist(data) {
    return request({
      url: '/api/projects/list/',
      method: 'get',
      params: data
    })
  }
}

export default new ProjectApi()
