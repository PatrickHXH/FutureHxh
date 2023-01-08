<template>
  <div class="main-card">
    <!-- 创建邮箱按钮 -->
    <div>
      <el-button type="primary" style="margin:10px auto" @click="create">添加邮箱</el-button>
    </div>
    <!-- 邮箱列表 -->
    <div>
      <el-table
        :data="tableData"
        :fit="true"
        style="width: 100%"
      >
        <el-table-column
          label="邮箱"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.email }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="授权码"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.code }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="服务器地址"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.server }}</span>
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
        cy-data="EmailPagination"
        @current-change="handleCurrentChange"
      />
    </div>
    <!-- 调用子组件 -->
    <emailDialog v-if="show" :tid="titleid" :eid="eid" @cancel="closeDialog" />
  </div>
</template>

<script>

import emailDialog from '@/views/setting/settingTab/emailDialog.vue'
import EmailApi from '@/api/email'
import { Message } from 'element-ui'

export default {
  components: {
    emailDialog
  },
  data() {
    return {
      show: false,
      titleid: 0,
      eid: 0,
      tableData: [],
      req: {
        page: 1,
        size: 10
      },
      total: 0
    }
  },
  mounted() {
    this.emailist()
  },
  methods: {
    showDialog() {
      this.show = true
    },
    closeDialog() {
      this.show = false
      this.emailist()
    },
    // 获取邮箱列表
    async emailist() {
      const resp = await EmailApi.getlist(this.req)
      console.log('列表', resp)
      if (resp.data.success === true) {
        // Message.success("获取列表成功")
        this.tableData = resp.data.items
        this.total = resp.data.total
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    // 跳到第几页
    handleCurrentChange(val) {
    //   console.log(`当前页: ${val}`);
      this.req.page = val
      this.emailist()
    },
    // 点击编辑邮箱
    Edit(index, row) {
      console.log(index, row)
      this.showDialog()
      this.titleid = 1
      this.eid = row.id
    },
    // 点击创建邮箱
    create() {
      this.showDialog()
      this.titleid = 0
    },
    // 删除邮箱
    async Delete(index, row) {
      console.log(index, row)
      const resp = await EmailApi.delete(row.id)
      if (resp.data.success === true) {
        Message.success('删除成功')
        this.emailist()
      } else {
        Message.error(resp.data.error.msg)
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
