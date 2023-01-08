<template>
  <div>
    <el-dialog
      :title="showtitle"
      :visible.sync="dialogVisible"
      width="50%"
      :before-close="closeDialog"
      :center="center"
    >
      <div style="text-align: center">
        <el-transfer
          style="text-align: left; display: inline-block"
          v-model="value"
          filterable
          :right-default-checked="value"
          :titles="['用户','授权']"
          :button-texts="['']"
          :format="{
            noChecked: '${total}',
            hasChecked: '${checked}/${total}'
          }"
          @change="handleChange"
          :data="userData">
          <span slot-scope="{ option }">{{ option.key }} - {{ option.label }}</span>
          <el-button class="transfer-footer" slot="right-footer" size="small" @click="clear()">清空</el-button>
          <!-- <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button> -->
        </el-transfer>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-role" @click="closeDialog">取消</el-button>
        <el-button cy-data="save-role" type="primary" @click="addRoleUser()">保存</el-button>
      </span>
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
      form:{
        group_id:"",
        user_id:[]
      },
      dialogVisible: true,
      userData:[],
      showtitle: '',
      center: true,
      value: [],
      };
  },
  // 触发生命周期，判断标题
  created(){
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
    handleChange(value, direction, movedKeys) {
        console.log("你好",value, direction, movedKeys);
     },
    // 新增用户授权
    async addRoleUser() {
      this.form.group_id = this.rid
      this.form.user_id = this.value
      const resp = await RoleApi.addRoleUser(this.form)
      if(resp.data.success === true){
        this.closeDialog()
        Message.success("授权成功")
      }else{
        Message.error(resp.data.error.msg)
      }
    },
    // 获取用户列表
    async initUserlist(id) {
      const resp = await RoleApi.getuserlist(id)
      if (resp.data.success === true) {
        for(let i=0;i<resp.data.result.length;i++){
          if(resp.data.result[i].is_current_group == true){
            this.value.push(resp.data.result[i].id)
          }
          this.userData.push({
            key:resp.data.result[i].id,
            label:resp.data.result[i].username,
            disabled:false
          })
        }
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    //清空授权列表
    clear(){
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

