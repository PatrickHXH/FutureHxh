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
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" cy-data="email-name" />
        </el-form-item>
        <el-form-item label="授权码" prop="code">
          <el-input v-model="form.code" cy-data="email-code" />
        </el-form-item>
        <el-form-item label="服务器" prop="server">
          <el-input v-model="form.server" cy-data="email-server" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-email" @click="closeDialog">取消</el-button>
        <el-button cy-data="save-email" type="primary" @click="onSubmit('form')">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import EmailApi from '@/api/email'
import { Message } from 'element-ui'
export default {
  // props: ['tid', 'eid'],
  props: { tid: { type: Object, default: null }, eid: { type: Object, default: null }},
  data() {
    return {
      dialogVisible: true,
      form: {
        name: '',
        code: '',
        server: ''
      },
      rules: {
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请输入授权码', trigger: 'blur' }
        ],
        server: [
          { required: true, message: '请输入服务器地址', trigger: 'blur' }
        ]
      },
      inResize: true,
      showtitle: '',
      center: true
    }
  },
  // 触发生命周期，判断标题
  created() {
    if (this.tid === 0) {
      this.showtitle = '添加邮箱'
    } else {
      this.showtitle = '编辑邮箱'
      this.initemaildetail(this.eid)
    }
  },
  methods: {
    // 调用父组件 关闭弹窗
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    // 创建、编辑邮箱
    onSubmit(formname) {
      this.$refs[formname].validate(valid => {
        if (valid) {
          if (this.tid === 0) {
            EmailApi.create(this.form).then(resp => {
              if (resp.data.success === true) {
                Message.success('创建成功')
                this.closeDialog()
              } else {
                Message.error(resp.data.error.msg)
              }
            })
          } else {
            EmailApi.update(this.eid, this.form).then(resp => {
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
    // 获取邮箱详情
    async initemaildetail(id) {
      const resp = await EmailApi.getdetail(id)
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

