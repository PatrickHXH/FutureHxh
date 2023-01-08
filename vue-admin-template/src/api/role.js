import request from '@/utils/request'

class RoleApi {
  create(data) {
    return request({
      url: '/api/rolepermission/createrole/',
      method: 'post',
      data
    })
  }
  update(id, data) {
    return request({
      url: '/api/rolepermission/roleupdate/' + id + '/',
      method: 'post',
      data
    })
  }
  delete(data) {
    return request({
      url: '/api/rolepermission/roledelete/',
      method: 'post',
      data
    })
  }
  getdetail(id) {
    return request({
      url: '/api/rolepermission/roledetail/' + id + '/',
      method: 'get'
    })
  }
  getlist(data) {
    return request({
      url: '/api/rolepermission/rolelist/',
      method: 'get',
      params: data
    })
  }
  getuserlist(id){
    return request({
      url: '/api/rolepermission/userlist/'+id+"/",
      method: 'get',
    })
  }
  addRoleUser(data){
    return request({
      url: '/api/rolepermission/addrole/',
      method: 'post',
      data
    })
  }
}

export default new RoleApi()