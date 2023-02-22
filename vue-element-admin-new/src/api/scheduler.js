import request from '@/utils/request'

class SchedulerApi {
  create(data) {
    return request({
      url: '/api/scheduled/create/',
      method: 'post',
      data
    })
  }
  removejob(data) {
    return request({
      url: '/api/scheduled/removejob/',
      method: 'post',
      data
    })
  }
  pausejob(data) {
    return request({
      url: '/api/scheduled/pausejob/',
      method: 'post',
      data
    })
  }
  resumejob(data) {
    return request({
      url: '/api/scheduled/resumejob/',
      method: 'post',
      data
    })
  }
  joblist() {
    return request({
      url: '/api/scheduled/joblist/',
      method: 'get'
    })
  }
  jobdetail(id) {
    return request({
      url: '/api/scheduled/jobdetail/' + id + '/',
      method: 'get'
    })
  }
  excutejob(id) {
    return request({
      url: '/api/scheduled/excutejob/' + id,
      method: 'post'
    })
  }
}

export default new SchedulerApi()
