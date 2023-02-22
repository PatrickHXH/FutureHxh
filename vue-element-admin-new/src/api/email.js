import request from '@/utils/request'

class EmailApi {
  create(data) {
    return request({
      url: '/api/emails/create/',
      method: 'post',
      data
    })
  }
  update(id, data) {
    return request({
      url: '/api/emails/update/' + id + '/',
      method: 'post',
      data
    })
  }
  delete(id) {
    return request({
      url: '/api/emails/delete/' + id + '/',
      method: 'post'
    })
  }
  getdetail(id) {
    return request({
      url: '/api/emails/detail/' + id + '/',
      method: 'get'
    })
  }
  getlist(data) {
    return request({
      url: '/api/emails/list/',
      method: 'get',
      params: data
    })
  }
}

export default new EmailApi()
