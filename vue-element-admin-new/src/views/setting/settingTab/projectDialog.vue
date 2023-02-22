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
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" cy-data="project-name" />
        </el-form-item>
        <el-form-item label="关键词" prop="keyword">
          <el-input v-model="form.keyword" cy-data="project-keyword" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-project" @click="closeDialog">取消</el-button>
        <el-button cy-data="save-project" type="primary" @click="onSubmit('form')">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import ProjectApi from '@/api/project'
import { Message } from 'element-ui'
export default {
  // props: ['tid', 'pid'],
  props: { tid: { type: Object, default: null }, pid: { type: Object, default: null }},
  data() {
    return {
      dialogVisible: true,
      form: {
        name: '',
        code: '',
        server: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ],
        keyword: [
          { required: true, message: '请输入关键词', trigger: 'blur' }
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
      this.showtitle = '创建项目'
    } else {
      this.showtitle = '编辑项目'
      this.initprojectdetail(this.pid)
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
            ProjectApi.create(this.form).then(resp => {
              if (resp.data.success === true) {
                Message.success('创建成功')
                this.closeDialog()
              } else {
                Message.error(resp.data.error.msg)
              }
            })
          } else {
            ProjectApi.update(this.pid, this.form).then(resp => {
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
    async initprojectdetail(id) {
      const resp = await ProjectApi.getdetail(id)
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

