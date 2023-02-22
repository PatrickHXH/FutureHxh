import request from '@/utils/request'

class PermissionApi {
  create(data) {
    return request({
      url: '/api/permission/create/',
      method: 'post',
      data
    })
  }
  update(id, data) {
    return request({
      url: '/api/permission/update/' + id + '/',
      method: 'post',
      data
    })
  }
  roleperupdate(data) {
    return request({
      url: '/api/permission/add/',
      method: 'post',
      data
    })
  }
  delete(data) {
    return request({
      url: '/api/permission/delete/',
      method: 'post',
      data
    })
  }
  getdetail(data) {
    return request({
      url: '/api/permission/detail/',
      method: 'post',
      data
    })
  }
  getroleperlist(id) {
    return request({
      url: '/api/permission/list/' + id + '/',
      method: 'get'
    })
  }
  getperlist(data) {
    return request({
      url: '/api/permission/per_list',
      method: 'get',
      params: data
    })
  }
}

export default new PermissionApi()
