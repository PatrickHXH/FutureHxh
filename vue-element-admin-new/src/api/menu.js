import request from '@/utils/request'

class MenuApi {
  // 新建菜单
  create(data) {
    return request({
      url: '/api/menu/create/',
      method: 'post',
      data
    })
  }
  // 编辑菜单
  update(id, data) {
    return request({
      url: '/api/menu/update/' + id + '/',
      method: 'post',
      data
    })
  }
  // 删除菜单
  delete(id) {
    return request({
      url: '/api/menu/delete/' + id + '/',
      method: 'post'
    })
  }
  // 菜单详情
  menuDetail(id) {
    return request({
      url: '/api/menu/detail/' + id + '/',
      method: 'get'
    })
  }
  // 菜单列表
  menuList() {
    return request({
      url: '/api/menu/list/',
      method: 'get'
    })
  }
  // 角色授权菜单
  menuRoleUpdate(data) {
    return request({
      url: '/api/menu/role/update/',
      method: 'post',
      data
    })
  }
  // 获取角色菜单列表
  menuRoleList(id) {
    return request({
      url: '/api/menu/rolelist/' + id + '/',
      method: 'get'
    })
  }
}

export default new MenuApi()
