<template>
    <div class="app-container" style="height:calc(95vh)">
  <div class="main-card" style="overflow:auto;">
    <!-- 创建定时任务按钮 -->
    <div>
      <el-button type="primary" style="margin:10px auto" @click="create">添加定时任务</el-button>
    </div>
    <!-- 任务列表 -->
    <div>
      <el-table
        :data="tableData"
        :fit="true"
        style="width: 100%"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="50"
        />
        <el-table-column
          prop="job_id"
          label="任务ID"
          width="300"
        />
        <el-table-column
          prop="describe"
          label="任务描述"
          width="140"
        />
        <el-table-column
          prop="trigger"
          label="触发类型"
          width="140"
        />
        <el-table-column
          prop="crontab"
          label="触发时间"
          width="140"
        />
        <el-table-column
          prop="excutefun"
          label="执行函数"
          width="140"
        />
        <el-table-column
          prop="next_run_time"
          label="下次运行时间"
          width="180"
        />
        <el-table-column
          prop="state"
          label="任务开启"
          width="140"
        >
          <template slot-scope="scope">
            <el-switch v-model="scope.row.state" style="margin-left: 10px" @change="switchJob(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="danger"
              @click="DeleteJob(scope.row)"
            >删除</el-button>
            <el-button
              size="mini"
              type="primary"
              :loading="loadingid===scope.row.id?true:false"
              style="width:73px;height:28px"
              @click="ExcuteJob(scope.row)"
            >执行</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 调用子组件 -->
    <schedulerDialog v-if="show" :tid="titleid" @cancel="closeDialog" />
  </div>
</div>
</template>

<script>

import schedulerDialog from '@/views/setting/settingTab/schedulerDialog.vue'
import SchedulerApi from '@/api/scheduler'
import { Message } from 'element-ui'

export default {
  components: {
    schedulerDialog
  },
  data() {
    return {
      show: false,
      titleid: 0,
      tableData: [],
      req: {
        page: 1,
        size: 6
      },
      total: 0,
      switchValue: '',
      loadingid: ''
    }
  },
  mounted() {
    this.Schedulerlist()
  },
  methods: {
    showDialog() {
      this.show = true
    },
    closeDialog() {
      this.show = false
      this.tableData = []
      this.Schedulerlist()
    },
    // 点击添加任务
    create() {
      this.showDialog()
    },
    // 获取定时任务列表
    async Schedulerlist() {
      const resp = await SchedulerApi.joblist()
      console.log('列表', resp)
      if (resp.data.success === true) {
      // Message.success("获取列表成功")
        for (let i = 0; i < resp.data.items.length; i++) {
          var time = new Date(resp.data.items[i].job.next_run_time)
          var runtime = resp.data.items[i].job.next_run_time === null ? null : time.toLocaleString()
          console.log(time)
          this.tableData.push({
            id: resp.data.items[i].id,
            job_id: resp.data.items[i].job.id,
            describe: resp.data.items[i].describe,
            trigger: resp.data.items[i].trigger,
            crontab: resp.data.items[i].crontab,
            excutefun: resp.data.items[i].excutefun,
            next_run_time: runtime,
            state: resp.data.items[i].state
          })
        }
        this.total = resp.data.total
      } else {
        Message.error('获取列表失败')
      }
    },
    // 重启和暂停任务
    async switchJob(row) {
      if (row.state === false) {
        const resp = await SchedulerApi.pausejob({ id: row.job_id })
        if (resp.data.success === true) {
          Message.info('暂停成功')
          this.tableData = []
          this.Schedulerlist()
        } else {
          Message.error(resp.data.error.msg)
        }
      } else {
        const resp = await SchedulerApi.resumejob({ id: row.job_id })
        if (resp.data.success === true) {
          Message.success('重启成功')
          this.tableData = []
          this.Schedulerlist()
        } else {
          Message.error(resp.data.error.msg)
        }
      }
    },
    // 删除任务
    async DeleteJob(row) {
      const resp = await SchedulerApi.removejob({ id: row.job_id })
      if (resp.data.success === true) {
        Message.success('删除成功')
        this.tableData = []
        this.Schedulerlist()
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    // 执行任务
    async ExcuteJob(row) {
      this.loadingid = row.id
      const resp = await SchedulerApi.excutejob(row.id)
      if (resp.data.success === true) {
        Message.success('执行成功')
        this.loadingid = ''
      } else {
        Message.error(resp.data.error.msg)
        this.loadingid = ''
      }
    }
  }
}
</script>

