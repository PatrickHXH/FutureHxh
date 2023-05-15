<template>
  <div class="main-card" style="overflow: auto;">
    <!-- 创建权限按钮 -->
    <div>
      <el-button type="primary" style="margin:10px auto" @click="create">添加权限</el-button>
    </div>
    <!-- 权限列表 -->
    <div>
      <el-table
        :data="tableData"
        :fit="true"
        style="width: 100%"
      >
        <el-table-column
          label="名称"
          width="180"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.permission.name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="接口路径"
          width="240"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.api_path }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="分类"
          width="220"
        >
          <template slot-scope="scope">
            <!-- <span style="margin-left: 10px">{{ content_type_name }}</span> -->
            <span style="margin-left: 10px" v-if="scope.row.permission.content_type_id==4">{{ scope.row.permission.content_type_id==4?"用户":""}}</span>
            <span style="margin-left: 10px" v-if="scope.row.permission.content_type_id==7">{{ scope.row.permission.content_type_id==7?"邮箱":""}}</span>
            <span style="margin-left: 10px" v-if="scope.row.permission.content_type_id==8">{{ scope.row.permission.content_type_id==8?"项目":""}}</span>
            <span style="margin-left: 10px" v-if="scope.row.permission.content_type_id==9">{{ scope.row.permission.content_type_id==9?"查询记录":""}}</span>
            <span style="margin-left: 10px" v-if="scope.row.permission.content_type_id==10">{{ scope.row.permission.content_type_id==10?"定时器":""}}</span>
            <span style="margin-left: 10px" v-if="scope.row.permission.content_type_id==13">{{ scope.row.permission.content_type_id==13?"权限":""}}</span>
            <span style="margin-left: 10px" v-if="scope.row.permission.content_type_id==14">{{ scope.row.permission.content_type_id==14?"菜单":""}}</span>
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
    <div style="text-align:center;position: fixed; left:calc(42vw);bottom: calc(2vh);">
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
    <permissionDialog v-if="show" :tid="titleid" :pid="pid" :per_id="per_id" :api_id="api_id" @cancel="closeDialog" />
  </div>
</template>

<script>

import permissionDialog from '@/views/setting/permission/permissionDialog.vue'
import PermissionApi from '@/api/permission'
import { Message } from 'element-ui'

export default {
  components: {
    permissionDialog
  },
  data() {
    return {
      show: false,
      titleid: 0,
      pid: 0,
      per_id: 0,
      api_id: 0,
      tableData: [],
      req: {
        page: 1,
        size: 10
      },
      total: 0,
      content_type_name:""
    }
  },
  mounted() {
    this.perlist()
  },
  methods: {
    showDialog() {
      this.show = true
    },
    closeDialog() {
      this.show = false
      this.perlist()
    },
    // 获取权限列表
    async perlist() {
      const resp = await PermissionApi.getperlist(this.req)
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
      this.perlist()
    },
    // 点击编辑项目
    Edit(index, row) {
      console.log(index, row)
      this.showDialog()
      this.titleid = 1
      this.pid = row.id
      this.per_id = row.permission.id
      this.api_id = row.id
    },
    // 点击创建项目
    create() {
      this.showDialog()
      this.titleid = 0
    },
    // 删除项目
    async Delete(index, row) {
      console.log(index, row)
      const resp = await PermissionApi.delete({ permission_id: row.permission.id })
      if (resp.data.success === true) {
        Message.success('删除成功')
        this.perlist()
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
