<template>
  <div class="app-container" style="height:calc(95vh)">
    <el-card style="width: 100%;height: 100%;">
      <!-- 选择框 -->
      <el-form ref="ruleForm" :model="ruleForm" :inline="true" :rules="rules" class="demo-ruleForm">
        <el-form-item label="项目" prop="projectlabel">
          <el-select v-model="ruleForm.projectlabel" placeholder="请选择项目" @change="changeproject">
            <el-option
              v-for="item in projectoptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="emaillabel">
          <el-select v-model="ruleForm.emaillabel" placeholder="请选择邮箱" @change="changeemail">
            <el-option
              v-for="item in emailoptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <keep-alive>
            <el-button :loading="loading" type="primary" @click="Search('ruleForm')">在线查询</el-button>
          </keep-alive>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
      <!-- 查询记录列表 -->
      <div>
        <h3>查询记录：</h3>
        <el-table
          :data="tableData"
          style="width: 100%"
          :header-cell-style="{textAlign:'center'}"
          :cell-style="{textAlign:'center'}"
          :row-class-name="tableRowClassName"
          :fit="fit"
        >
          <el-table-column prop="project" label="项目" />
          <el-table-column prop="subject" label="标题" />
          <el-table-column prop="sender" label="发送" />
          <el-table-column prop="receive" label="接收" />
          <el-table-column prop="report_time" label="报告时间" />
          <el-table-column prop="update_time" label="更新时间" />
          <!-- <el-table-column prop="create_time" label="创建时间" /> -->
          <el-table-column prop="lastest" label="最新" />
          <el-table-column prop="existfail" label="存在错误" />
          <!-- <el-table-column prop="report_dir" label="详情"></el-table-column> -->
          <el-table-column fixed="right" label="操作" width="100">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="handleClick(scope.row)">查看</el-button>
            <!-- <el-button type="text" size="small">查看</el-button> -->
            </template>
          </el-table-column>
        </el-table>
      </div>
      <!-- 分页 -->
      <div style="text-align:center;position: fixed; left:calc(42vw);bottom: calc(5vh);">
        <el-pagination
          background
          :page-size="req.size"
          :total="total"
          style="margin: 10px"
          cy-data="EmailPagination"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }

  .el-table .error-row {
    background: #ecc7c9;
  }
</style>

<script>
import EmailApi from '@/api/email'
import ProjectApi from '@/api/project'
import ReportApi from '@/api/report'

export default {
  components: {
  },
  data() {
    return {
      fit: true,
      ruleForm: {
        projectlabel: '',
        emaillabel: ''
      },
      rules: {
        projectlabel: [
          { required: true, message: '请选择项目', trigger: 'change' }
        ],
        emaillabel: [
          { required: true, message: '请选择邮箱', trigger: 'change' }
        ]
      },
      projectoptions: [],
      emailoptions: [],
      req: {
        page: 1,
        size: 6
      },
      projectvalue: 1,
      emailvalue: 1,
      tableData: [],
      loading: false,
      total: 0
    }
  },
  created() {
    this.initProjectList()
    this.initEmailList()
    this.initSearchReportLog()
  },
  methods: {
    // 查询报告
    Search(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.loading = true
          const reportdata = { 'project_id': this.projectvalue, 'email_id': this.emailvalue }
          ReportApi.getreport(reportdata).then((resp) => {
            if (resp.data.success === true) {
              this.loading = false
              this.tableData = []
              this.initSearchReportLog()
              this.$message.success('查询成功')
            } else {
              this.loading = false
              this.$message.error(resp.data.error.msg)
            }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 重置
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    // 初始化获取项目列表
    async initProjectList() {
      console.log('获取项目列表')
      const resp = await ProjectApi.getlist(this.req)
      if (resp.data.success === true) {
        this.projectvalue = resp.data.items[0].id
        this.projectlabel = resp.data.items[0].name
        // this.total = resp.data.total
        for (let i = 0; i < resp.data.items.length; i++) {
          this.projectoptions.push({
            // value为id label为内容
            value: resp.data.items[i].id,
            label: resp.data.items[i].name + '—' + resp.data.items[i].keyword
          })
        }
        // this.$message.success("查询成功");
      } else {
        this.$message.error('查询失败!')
      }
    },
    // 初始化获取邮箱列表
    async initEmailList() {
      const resp = await EmailApi.getlist(this.req)
      if (resp.data.success === true) {
        this.emailvalue = resp.data.items[0].id
        this.emaillabel = resp.data.items[0].email
        // this.total = resp.data.total
        for (let i = 0; i < resp.data.items.length; i++) {
          this.emailoptions.push({
            // value为id label为内容
            value: resp.data.items[i].id,
            label: resp.data.items[i].email
          })
        }
        // this.$message.success("查询成功");
      } else {
        this.$message.error('查询失败!')
      }
    },
    // 切换项目
    changeproject(value) {
      this.projectvalue = value
    },
    // 切换邮箱
    changeemail(value) {
      this.emailvalue = value
    },
    // 获取查询记录
    async initSearchReportLog() {
      const resp = await ReportApi.getreportlog(this.req)
      if (resp.data.success === true) {
        for (let i = 0; i < resp.data.items.length; i++) {
          var time = new Date(resp.data.items[i].update_time)
          let lastest = resp.data.items[i].lastest
          let existfail = resp.data.items[i].existfail
          if (lastest === true) {
            lastest = '是'
          } else {
            lastest = '否'
          }
          if (existfail === true) {
            existfail = '是'
          } else {
            existfail = '否'
          }
          this.tableData.push({
            project: resp.data.items[i].project.name + '_' + resp.data.items[i].project.keyword,
            subject: resp.data.items[i].subject,
            sender: resp.data.items[i].sender,
            receive: resp.data.items[i].receive,
            report_time: resp.data.items[i].report_time,
            update_time: time.toLocaleString(),
            // create_time: resp.data.items[i].create_time,
            existfail: existfail,
            lastest: lastest,
            report_dir: resp.data.items[i].report_dir
          })
        }
        this.total = resp.data.total
      } else {
        this.$message.error('查询失败!')
      }
    },
    // 行显示颜色
    tableRowClassName({ row, rowIndex }) {
      console.log(row.lastest)
      if (row.lastest === '否') {
        return 'warning-row'
      } else if (row.existfail === '是') {
        return 'error-row'
      } else if (row.lastest === '是') {
        return 'success-row'
      }
    },
    // 打开测试报告
    handleClick(row) {
      console.log(row.report_dir)
      // window.location.href = report_dir
      window.open(row.report_dir)
    },
    // 跳到第几页
    handleCurrentChange(val) {
      this.req.page = val
      this.initSearchReportLog()
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

