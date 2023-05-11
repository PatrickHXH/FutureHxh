<template>
  <div>
    <el-dialog
      :title="showtitle"
      :visible.sync="dialogVisible"
      width="300px"
      :before-close="closeDialog"
      :center="center"
    >
      <div style="text-align: center;overflow: auto">
        <el-tree
          :data="data"
          show-checkbox
          ref="tree"
          highlight-current
          node-key="id"
          :props="defaultProps"
          @check="handleNodeClick"
          :default-checked-keys="defaultCheckedKeys"
          >
        </el-tree>
      </div>
      <div slot="footer" class="dialog-footer" style="text-align: center;">
        <el-button cy-data="cancel-role" @click="closeDialog">取消</el-button>
        <el-button cy-data="save-role" type="primary" @click="addRoleUser()">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import RoleApi from '@/api/role'
import { Message } from 'element-ui'
export default {
  props: ['tid', 'rid'],
  // props: { tid: { type: Object, default: null }, rid: { type: Object, default: null }},
  data() {
    return {
      form: {
        group_id: '',
        user_id: []
      },
      dialogVisible: true,
      showtitle: '',
      center: true,
      data: [],
      defaultProps: {
        children: 'children',
        label: 'username'
      },
      defaultCheckedKeys:[]
    }
  },
  // 触发生命周期，判断标题
  created() {
    if (this.tid === 2) {
      this.showtitle = '授权用户'
      this.initUserlist(this.rid)
    }
  },
  methods: {
    // 调用父组件 关闭弹窗
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    // 新增用户授权
    async addRoleUser() {
      this.form.group_id = this.rid
      const resp = await RoleApi.addRoleUser(this.form)
      if (resp.data.success === true) {
        this.closeDialog()
        Message.success('授权成功')
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    // 获取用户列表
    async initUserlist(id) {
      const resp = await RoleApi.getuserlist(id)
      if (resp.data.success === true) {
        for (let i = 0; i < resp.data.result.length; i++) {
          this.data.push({
            id:resp.data.result[i].id,
            username:resp.data.result[i].username,
          })
          if(resp.data.result[i].is_current_group === true){
            this.defaultCheckedKeys.push(resp.data.result[i].id)
            this.form.user_id.push(resp.data.result[i].id)
          }
        }
        console.log("ceshi",this.defaultCheckedKeys)
        this.$nextTick(() => {
          this.$refs.tree.setCheckedKeys(this.defaultCheckedKeys);
        });
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    //选择节点
    handleNodeClick(a,b) {
        console.log(a,b);
        this.form.user_id = b.checkedKeys
      },
    // 清空授权列表
    clear() {
      this.value = []
    }
  }
}
</script>

  <style scoped>
  .line{
    text-align: center;
  }
  .transfer-footer {
    margin-left: 20px;
    padding: 6px 5px;
  }
  </style>

