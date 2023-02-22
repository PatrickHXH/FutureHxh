<template>
  <div>
    <el-dialog
      :title="showtitle"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="closeDialog"
      :center="center"
    >
      <el-form v-if="inResize === true" ref="form" :rules="rules" :model="form" label-width="120px">
        <el-form-item label="名称：" prop="name">
          <el-input v-model="form.name" cy-data="permissino-name" />
        </el-form-item>
        <el-form-item label="接口路径：" prop="api_path">
          <el-input v-model="form.api_path" cy-data="permissino-apipath" />
        </el-form-item>
        <el-form-item label="项目代号：" prop="content_type_id">
          <el-select v-model="form.content_type_id" placeholder="请选择项目代号" @change="changeproject">
            <el-option
              v-for="item in projectoptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="权限编码：" prop="codename">
          <el-input v-model="form.codename" cy-data="permission-codename" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-permission" @click="closeDialog">取消</el-button>
        <el-button cy-data="save-permission" type="primary" @click="onSubmit('form')">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import PermissionApi from '@/api/permission'
import { Message } from 'element-ui'
export default {
  props: ['tid', 'pid', 'per_id', 'api_id'],
  // props: { tid: { type: Object, default: null }, rid: { type: Object, default: null }},
  data() {
    return {
      dialogVisible: true,
      form: {
        name: '',
        api_path: '',
        codename: '',
        content_type_id: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入描述', trigger: 'blur' }
        ],
        api_path: [
          { required: true, message: '请输入接口路径', trigger: 'blur' }
        ],
        content_type_id: [
          { required: true, message: '请选择项目代号', trigger: 'change' }
        ],
        codename: [
          { required: true, message: '请输入codename', trigger: 'blur' }
        ]
      },
      projectoptions: [{
        label: '接口',
        value: 13
      }],
      inResize: true,
      showtitle: '',
      center: true
    }
  },
  // 触发生命周期，判断标题
  created() {
    if (this.tid === 0) {
      this.showtitle = '新建权限'
      this.changeproject(this.projectoptions[0].value)
    } else {
      this.showtitle = '编辑权限'
      this.changeproject(this.projectoptions[0].value)
      this.initpermissiondetail({ permission_id: this.per_id })
    }
  },
  methods: {
    // 调用父组件 关闭弹窗
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    // 创建、编辑权限
    onSubmit(formname) {
      this.$refs[formname].validate(valid => {
        if (valid) {
          if (this.tid === 0) {
            PermissionApi.create(this.form).then(resp => {
              if (resp.data.success === true) {
                Message.success('创建成功')
                this.closeDialog()
              } else {
                Message.error(resp.data.error.msg)
              }
            })
          } else {
            PermissionApi.update(this.api_id, this.form).then(resp => {
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
    async initpermissiondetail(id) {
      const resp = await PermissionApi.getdetail(id)
      if (resp.data.success === true) {
        this.form.name = resp.data.result.name
        this.form.api_path = resp.data.result.api_path
        this.form.codename = resp.data.result.codename
        this.form.content_type_id = resp.data.result.content_type
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    // 切换项目
    changeproject(value) {
      console.log(value)
      this.form.content_type_id = value
    }
  }
}
</script>

  <style scoped>
  .line{
    text-align: center;
  }
  </style>

