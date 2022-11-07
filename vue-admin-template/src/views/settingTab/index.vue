<template>
  <div class="app-container" style="height:calc(95vh)">
    <div class="workbench" style="height: 100%">
      <el-tabs v-model="tabName" type="border-card" style="height: 100%" @tab-click="tabClick">
        <el-tab-pane label="项目管理" name="project">
          <projectlist v-if="showTab == 1" />
        </el-tab-pane>
        <el-tab-pane label="邮件管理" name="email">
          <emailist v-if="showTab == 2" />
        </el-tab-pane>
        <el-tab-pane label="定时任务" name="scheduler">
          <schedulerlist v-if="showTab == 3" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import emailist from '@/views/settingTab/emailist.vue'
import projectlist from '@/views/settingTab/projectlist.vue'
import schedulerlist from '@/views/settingTab/schedulerlist.vue'
export default {
  components: {
    // 组件
    emailist,
    projectlist,
    schedulerlist
  },
  data() {
    return {
    // loading: true,
      tabName: 'project',
      showTab: 1
    }
  },

  mounted() {
    // 初始化方法
  },

  methods: {
    // 切换tab标签页
    tabClick(tab) {
      console.log(tab.name)
      if (tab.name === 'project') {
        this.showTab = 1
      }
      if (tab.name === 'email') {
        this.showTab = 2
      }
      if (tab.name === 'scheduler') {
        this.showTab = 3
      }
    }
  }
}
</script>

<style>
.el-popover.home-popover {
width: 70px;
min-width: auto;
}
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* 定义当前组件使用的CSS */
</style>
