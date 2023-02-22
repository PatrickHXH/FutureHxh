import request from '@/utils/request'

class ReportApi {
  getreport(data) {
    return request({
      url: '/api/reports/search/',
      method: 'post',
      data
    })
  }
  getreportlog(data) {
    return request({
      url: '/api/reports/list/',
      method: 'get',
      params: data
    })
  }
}

export default new ReportApi()
