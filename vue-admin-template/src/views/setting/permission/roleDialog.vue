<template>
  <div>
    <el-dialog
      :title="showtitle"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="closeDialog"
      :center="center"
    >
      <el-form v-if="inResize === true" ref="form" :rules="rules" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" cy-data="role-name" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-role" @click="closeDialog">取消</el-button>
        <el-button cy-data="save-role" type="primary" @click="onSubmit('form')">保存</el-button>
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
      dialogVisible: true,
      form: {
        name: '',
      },
      rules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ],
      },
      inResize: true,
      showtitle: '',
      center: true
    }
  },
  // 触发生命周期，判断标题
  created() {
    if (this.tid === 0) {
      this.showtitle = '创建角色'
    } else {
      this.showtitle = '编辑角色'
      this.initroledetail(this.rid)
    }
  },
  methods: {
    // 调用父组件 关闭弹窗
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    // 创建、编辑项目
    onSubmit(formname) {
      this.$refs[formname].validate(valid => {
        if (valid) {
          if (this.tid === 0) {
            RoleApi.create(this.form).then(resp => {
              if (resp.data.success === true) {
                Message.success('创建成功')
                this.closeDialog()
              } else {
                Message.error(resp.data.error.msg)
              }
            })
          } else {
            RoleApi.update(this.rid, this.form).then(resp => {
              if (resp.data.success === true) {
                Message.success('编辑成功')
                this.closeDialog()
              } else {
                Message.error(resp.data.error.msg)
              }
            })
          }
        }
      })
    },
    // 获取项目详情
    async initroledetail(id) {
      const resp = await RoleApi.getdetail(id)
      if (resp.data.success === true) {
        this.form = resp.data.result
      } else {
        Message.error(resp.data.error.msg)
      }
    }
  }
}
</script>

  <style scoped>
  .line{
    text-align: center;
  }
  </style>

