<template>
  <div class="main-card">
    <!-- 创建角色按钮/添加用户 -->
    <div>
      <el-button type="primary" style="margin:10px 10px;" @click="create">添加角色</el-button>
      <el-button type="primary" style="margin:10px 10px;" @click="register">添加用户</el-button>
    </div>
    <!-- 角色列表 -->
    <div>
      <el-table
        :data="tableData"
        :fit="true"
        style="width: 100%"
      >
        <el-table-column
          label="ID"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="角色"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button-group>
              <el-button type="warning" icon="el-icon-s-promotion" @click="enterRolePermission(scope.$index, scope.row)">接口</el-button>
              <el-button icon="el-icon-menu" style="background-color:azure;" @click="enterMenuPermission(scope.$index, scope.row)">菜单</el-button>
              <el-button type="success" icon="el-icon-user" @click="enterRoleUser(scope.$index, scope.row)">用户</el-button>
              <el-button type="primary" icon="el-icon-edit" @click="Edit(scope.$index, scope.row)" />
              <el-button type="danger" icon="el-icon-delete" @click="Delete(scope.$index, scope.row)" />
            </el-button-group>
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
    <roleDialog v-if="show" :tid="titleid" :rid="rid" @cancel="closeDialog" />
    <roleUserDialog v-if="showRoleDialog" :tid="titleid" :rid="rid" @cancel="closeDialog" />
    <userRegister v-if="showRegister" :tid="titleid" :rid="rid" @cancel="closeDialog" />
  </div>
</template>

<script>

import roleDialog from '@/views/setting/permission/roleDialog.vue'
import roleUserDialog from '@/views/setting/permission/roleUserDialog.vue'
import userRegister from '@/views/setting/permission/userRegister.vue'
import RoleApi from '@/api/role'
import { Message } from 'element-ui'

export default {
  components: {
    roleDialog,
    roleUserDialog,
    userRegister
  },
  data() {
    return {
      show: false,
      showRoleDialog: false,
      showRegister: false,
      titleid: 0,
      rid: 0,
      tableData: [],
      req: {
        page: 1,
        size: 10
      },
      total: 0
    }
  },
  mounted() {
    this.rolelist()
  },
  methods: {
    showDialog() {
      this.show = true
    },
    closeDialog() {
      this.show = false
      this.showRoleDialog = false
      this.showRegister = false
      this.rolelist()
    },
    // 获取角色列表
    async rolelist() {
      const resp = await RoleApi.getlist(this.req)
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
      this.rolelist()
    },
    // 点击编辑角色
    Edit(index, row) {
      this.showDialog()
      this.titleid = 1
      this.rid = row.id
    },
    // 点击创建角色
    create() {
      this.showDialog()
      this.titleid = 0
    },
    // 点击注册用户
    register() {
      this.showRegister = true
      this.titleid = 3
    },
    // 删除角色
    async Delete(index, row) {
      console.log(index, row)
      const resp = await RoleApi.delete({ id: row.id })
      if (resp.data.success === true) {
        Message.success('删除成功')
        this.rolelist()
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    // 跳转角色授权接口页面
    enterRolePermission(index, row) {
      this.$router.push({ path: '/permisssion/role', query: { id: row.id }})
    },
    // 跳转角色授权菜单页面
    enterMenuPermission(index, row) {
      this.$router.push({ path: '/permisssion/menu', query: { id: row.id }})
    },
    // 打开用户授权
    enterRoleUser(index, row) {
      this.showRoleDialog = true
      this.titleid = 2
      this.rid = row.id
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
