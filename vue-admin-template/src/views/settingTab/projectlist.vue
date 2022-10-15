<template>
  <div class="main-card">
    <!-- 创建项目按钮 -->
    <div>
      <el-button type="primary" style="margin:10px auto" @click="create">添加项目</el-button>
    </div>
    <!-- 邮箱列表 -->
    <div>
      <el-table
        :data="tableData"
        :fit="true"
        style="width: 100%"
      >
        <el-table-column
          label="项目名称"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="关键词"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.keyword }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="Edit(scope.$index, scope.row)"
            >编辑</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="Delete(scope.$index, scope.row)"
            >删除</el-button>
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
        cy-data="ProjectPagination"
        @current-change="handleCurrentChange"
      />
    </div>
    <!-- 调用子组件 -->
    <projectDialog v-if="show" :tid="titleid" :pid="pid" @cancel="closeDialog" />
  </div>
</template>

<script>

import projectDialog from '@/views/settingTab/projectDialog.vue'
import ProjectApi from '@/api/project'
import { Message } from 'element-ui'

export default {
  components: {
    projectDialog
  },
  data() {
    return {
      show: false,
      titleid: 0,
      pid: 0,
      tableData: [],
      req: {
        page: 1,
        size: 10
      },
      total: 0
    }
  },
  mounted() {
    this.projectlist()
  },
  methods: {
    showDialog() {
      this.show = true
    },
    closeDialog() {
      this.show = false
      this.projectlist()
    },
    // 获取项目列表
    async projectlist() {
      const resp = await ProjectApi.getlist(this.req)
      console.log('列表', resp)
      if (resp.data.success === true) {
        // Message.success("获取列表成功")
        this.tableData = resp.data.items
        this.total = resp.data.total
      } else {
        Message.error('获取列表失败')
      }
    },
    // 跳到第几页
    handleCurrentChange(val) {
    //   console.log(`当前页: ${val}`);
      this.req.page = val
      this.projectlist()
    },
    // 点击编辑项目
    Edit(index, row) {
      console.log(index, row)
      this.showDialog()
      this.titleid = 1
      this.pid = row.id
    },
    // 点击创建项目
    create() {
      this.showDialog()
      this.titleid = 0
    },
    // 删除项目
    async Delete(index, row) {
      console.log(index, row)
      const resp = await ProjectApi.delete(row.id)
      if (resp.data.success === true) {
        Message.success('删除成功')
        this.projectlist()
      } else {
        Message.error('删除失败')
      }
    }
  }
}
</script>

  <style>
  .el-popover.home-popover {
    width: 70px;
    min-width: auto;
  }
  </style>

  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  /* 定义当前组件使用的CSS */
  .filter-line {
    height: 50px;
    text-align: left;
    margin-left: 15px;
  }
  .foot-page {
    margin-top: 20px;
      float: right;
      margin-bottom: 20px;
  }
  .project-card {
    margin-left: 15px;
    margin-right: 15px;
    margin-top: 15px;
    margin-bottom: 15px
  }
  </style>
