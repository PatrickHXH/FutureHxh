<template>
  <div class="app-container" style="height:calc(95vh)">
    <el-card style="width: 100%;height: 100%;padding: 0px;overflow:auto">
      <!-- 返回上一页 -->
      <div>
        <el-page-header content="授权接口" @back="returnLastPage" />
      </div>
      <div style="margin:20px 0" />
      <!-- 权限列表 -->
      <el-tree
        :data="data"
        show-checkbox
        default-expand-all
        node-key="id"
        ref="tree"
        highlight-current
        :props="defaultProps"
        @check="handleNodeClick"
        :default-checked-keys="defaultCheckedKeys"
        >
      </el-tree>
      <!-- 保存按钮 -->
      <div style="margin:20px 0">
        <el-button type="primary" style="float:right" @click="saveRolePer()">保存</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Message } from 'element-ui'
import PermissionApi from '@/api/permission'
export default {
  components: { },
  props: [],
  data() {
    return {
      checkedPer: [],
      data: [],
      defaultProps: {
        children: 'group',
        label: 'name'
      },
      defaultCheckedKeys:[]
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
    handleCheckChange(data, checked, indeterminate) {
        console.log(data, checked, indeterminate);
      },
    handleNodeClick(a,b) {
        console.log(a,b);
        this.checkedPer = b.checkedKeys
      },
    async initPermissionList() {
      const resp = await PermissionApi.getroleperlist(this.$route.query.id)
      console.log('列表', resp)
      if (resp.data.success === true) {
        for (let i = 0; i < resp.data.result.length; i++) {
          switch(resp.data.result[i]["content_type"]){
            case 4:
              var name = "用户"
              break
            case 7:
              var name = "邮箱"
              break
            case 8:
              var name = "项目"
              break
            case 9:
              var name = "查询记录"
              break
            case 13:
              var name = "权限"
              break
            case 14:
              var name = "菜单"
              break
            case 10:
              var name = "定时任务"
              break
            default:
              var name = "其他"
              break
          }
          this.data.push({
            name:name,
            group:resp.data.result[i].group
          })
          for(let j=0; j<resp.data.result[i].group.length;j++){
            if(resp.data.result[i].group[j]["has_per"]===true){
              this.defaultCheckedKeys.push(resp.data.result[i].group[j].id)
            }
          }
        }
        this.$nextTick(() => {
          this.$refs.tree.setCheckedKeys(this.defaultCheckedKeys);
        });
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    load() {},
    async saveRolePer() {
      const resp = await PermissionApi.roleperupdate({
        permission_id: this.checkedPer,
        group_id: this.$route.query.id
      })
      if (resp.data.success === true) {
        Message.success('保存成功')
        this.returnLastPage()
      } else {
        Message.error(resp.data.error.msg)
      }
    },
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

