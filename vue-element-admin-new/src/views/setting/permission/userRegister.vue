<template>
  <div>
    <el-dialog
      :title="showtitle"
      :visible.sync="dialogVisible"
      width="20%"
      :before-close="closeDialog"
      :center="center"
    >
      <el-form v-if="inResize === true" ref="form" :rules="rules" :model="form" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" cy-data="register-username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" cy-data="register-password" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="form.confirm_password" cy-data="register_confirm_password" />
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
import { register } from '@/api/user'
import { Message } from 'element-ui'
export default {
  props: ['tid', 'rid'],
  // props: { tid: { type: Object, default: null }, rid: { type: Object, default: null }},
  data() {
    return {
      dialogVisible: true,
      form: {
        username: '',
        password: '',
        confirm_password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        confirm_password: [
          { required: true, message: '请确认密码', trigger: 'blur' }
        ]
      },
      inResize: true,
      showtitle: '',
      center: true
    }
  },
  // 触发生命周期，判断标题
  created() {
    if (this.tid === 3) {
      this.showtitle = '添加用户'
    }
  },
  methods: {
    // 调用父组件 关闭弹窗
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    // 创建用户
    onSubmit(formname) {
      this.$refs[formname].validate(valid => {
        if (valid) {
          if (this.tid === 3) {
            register(this.form).then(resp => {
              if (resp.data.success === true) {
                Message.success('添加成功')
                this.closeDialog()
              } else {
                Message.error(resp.data.error.msg)
              }
            })
          }
        }
      })
    }
  }
}
</script>

  <style scoped>
  .line{
    text-align: center;
  }
  </style>

