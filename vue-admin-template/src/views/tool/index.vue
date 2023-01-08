<template>
  <div>
    <el-menu
      :default-active="activeIndex2"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-submenu index="1">
        <template slot="title">在线工具</template>
        <el-menu-item index="1-1">JSON解析</el-menu-item>
        <el-menu-item index="1-2">SQL格式化</el-menu-item>
        <el-submenu index="1-3">
          <template slot="title">加密/解密</template>
          <el-menu-item index="1-3-1">RSA加密（开发中）</el-menu-item>
        </el-submenu>
        <el-submenu index="1-4">
          <template slot="title">计算器</template>
          <el-menu-item index="1-4-1">日期计算器</el-menu-item>
          <el-menu-item index="1-4-2">转换时间戳</el-menu-item>
        </el-submenu>
        <el-menu-item index="1-5">测试</el-menu-item>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title">文档教程</template>
        <el-menu-item index="2-1">速查表</el-menu-item>
      </el-submenu>
    </el-menu>
    <el-main style="width: 100%; height: 100%">
      <tooljsonpasrsing v-if="show == '1-1'" :key="1-1" />
      <toolsqlformat v-if="show == '1-2'" :key="1-2" />
      <toolTimeCalculationVue v-if="show == '1-4-1'" />
      <toolstamp v-if="show == '1-4-2'" />
      <toolTest v-if="show == '1-5'" />
      <toolQuickCheck v-if="show =='2-1'" />
    </el-main>

  </div>
</template>
<script>

import toolstamp from '@/views/tool/TestTool/tool_timestamp.vue'
import tooljsonpasrsing from '@/views/tool/TestTool/tool_JsonParsing.vue'
import toolsqlformat from '@/views/tool/TestTool/tool_SqlFormat.vue'
import toolTimeCalculationVue from './TestTool/tool_TimeCalculation.vue'
import toolQuickCheck from '@/views/tool/TestTool/tool_QuickCheck.vue'
import toolTest from '@/views/tool/TestTool/tool_Test.vue'
export default {
  components: {
    toolstamp,
    tooljsonpasrsing,
    toolsqlformat,
    toolTimeCalculationVue,
    toolQuickCheck,
    toolTest
  },
  data() {
    return {
      show: '',
      activeIndex2: '1-1'
      // isCollapse: true
    }
  },
  mounted() {
    this.show = '1-1'
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(typeof (key))
      this.show = key
    }
  }
}
</script>

<style>
.el-menu-demo{
  padding: 0;
}
</style>
