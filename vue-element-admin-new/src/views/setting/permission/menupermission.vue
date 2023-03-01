<template>
  <div class="app-container" style="height:calc(95vh)">
    <el-card style="width: 100%;height: 100%;padding: 0px;overflow:auto;">
      <!-- 返回上一页 -->
      <div>
        <el-page-header content="授权菜单" @back="returnLastPage" />
      </div>
      <div style="margin:20px 0" />
      <!-- 菜单列表 -->
      <div v-infinite-scroll="load" class="per-group" style="overflow:auto">
        <el-tree
          ref="tree"
          :data="data"
          show-checkbox
          node-key="id"
          :default-expand-all="true"
          :default-checked-keys="defaultCheckedKeys"
          :props="defaultProps"
          @check="handleCheckChange"
        />
      </div>
      <!-- 保存按钮 -->
      <div style="margin:20px 0">
        <el-button type="primary" style="float:right" @click="saveMenuPer()">保存</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Message } from 'element-ui'
import MenuApi from '@/api/menu'
// const perOptions = [];
export default {
  components: { },
  props: [],
  data() {
    return {
      data: [],
      perOptions: [],
      Options: [],
      checkAll: false,
      checkedPer: [],
      isIndeterminate: true,
      count: 0,
      defaultProps: {
        children: 'children',
        label: 'title'
      },
      defaultCheckedKeys: [],
      checked_list: []
    }
  },
  created() {
    this.initPermissionList()
  },
  beforeDestroy() {

  },
  methods: {
    returnLastPage() {
      this.$router.push({ path: '/permisssion/index' })
    },
    // 读取每个树形节点返回数组
    readNodes(nodes = [], arr = []) {
      for (const item of nodes) {
        arr.push({
          id: item.id,
          has_per: item.has_per
        })
        if (item.children && item.children.length) { this.readNodes(item.children, arr) }
      }
      return arr
    },
    handleCheckChange() {
      this.checked_list = this.$refs.tree.getCheckedKeys()
      console.log(this.checked_list)
    },
    async initPermissionList() {
      const resp = await MenuApi.menuRoleList(this.$route.query.id)
      if (resp.data.success === true) {
        this.data = resp.data.result
        const arr = this.readNodes(this.data, arr)
        for (let i = 0; i < arr.length; i++) {
          if (arr[i].has_per === true) {
            this.defaultCheckedKeys.push(arr[i].id)
          }
        }
        console.log(this.defaultCheckedKeys)
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    load() {},
    async saveMenuPer() {
      const resp = await MenuApi.menuRoleUpdate({
        menu_list: this.checked_list,
        role_id: this.$route.query.id
      })
      if (resp.data.success === true) {
        Message.success('保存成功')
        this.returnLastPage()
      } else {
        Message.error(resp.data.error.msg)
      }
    }
  }
}
</script>

  <style>
  .per-group{
      display: flex;
      height: 75vh;
  }
  .per-group-cloumn{
      display: flex;
      flex-direction:column;
      margin:0 20px;

  }
  .per-group-item{
      margin: 4px 0;

  }
  </style>

