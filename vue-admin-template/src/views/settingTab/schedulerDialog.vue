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
        <el-form-item label="任务描述" prop="describe">
          <el-input v-model="form.describe" cy-data="scheduler-describe" />
        </el-form-item>
        <el-form-item label="执行函数" prop="excutefun">
          <el-input v-model="form.excutefun" cy-data="scheduler-excutefun" />
        </el-form-item>
        <el-form-item label="触发类型" prop="trigger">
          <!-- <el-input v-model="form.triggerType" cy-data="scheduler-triggerType" /> -->
          <el-select v-model="form.trigger" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="触发时间" prop="crontab">
          <el-input v-model="form.crontab" cy-data="scheduler-crontab" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-scheduler" @click="closeDialog">取消</el-button>
        <el-button cy-data="save-scheduler" type="primary" @click="onSubmit('form')">创建</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import SchedulerApi from '@/api/scheduler'
import { Message } from 'element-ui'
export default {
  // props: ['tid', 'pid'],
  props: { tid: { type: Object, default: null }},
  data() {
    return {
      dialogVisible: true,
      options: [{
        value: 'cron',
        label: 'cron'
      }],
      value: '',
      form: {
        describe: '',
        excutefun: '',
        trigger: '',
        crontab: ''
      },
      rules: {
        describe: [
          { required: true, message: '请输入任务描述', trigger: 'blur' }
        ],
        excutefun: [
          { required: true, message: '请输入执行函数', trigger: 'blur' }
        ],
        trigger: [
          { required: true, message: '请选择触发类型', trigger: 'blur' }
        ],
        crontab: [
          { required: true, message: '请输入触发时间', trigger: 'blur' }
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
      this.showtitle = '创建定时任务'
    } else {
      this.showtitle = ''
    }
  },
  methods: {
    // 调用父组件 关闭弹窗
    closeDialog() {
      console.log('closeDialog')
      this.$emit('cancel', {})
    },
    // 创建定时任务
    onSubmit(formname) {
      this.$refs[formname].validate(valid => {
        if (valid) {
          if (this.tid === 0) {
            // this.form.trigger = this.value
            SchedulerApi.create(this.form).then(resp => {
              if (resp.data.success === true) {
                Message.success('创建成功')
                this.closeDialog()
              } else {
                Message.error('创建失败')
              }
            })
          }
        }
      })
    },
    // 获取项目详情
    async initprojectdetail(id) {
      const resp = await ProjectApi.getdetail(id)
    }
  }
}
</script>

<style scoped>
.line{
    text-align: center;
}
</style>

