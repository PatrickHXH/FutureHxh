<template>
  <div class="app-container" style="height:calc(85vh)">
    <el-card style="width: 100%;height: 100%;padding: 0px;">
      <!-- 标题 -->
      <p class="fontstyle" href="../css/common.css">时间转化器</p>

      <!-- 时间转为时间戳选择器 -->
      <div style="height:8vh;">
        <div class="block" style="float:left;margin-right: 10px;display:flex;">
          <div style="float:left;margin-right: auto;align-self:center;">时间：</div>
          <el-date-picker
            v-model="value1"
            type="datetime"
            placeholder="选择日期"
          />
        </div>
        <!-- 转换按钮 -->
        <el-button type="primary" style="float:left;width: 70px;margin-right: 10px;" @click="changetimestamp">转换</el-button>
        <!-- 输出框 -->
        <el-input v-model="input" placeholder="时间戳" style="float:left;width: 160px;margin-right: 10px;" />
        <!-- 选择框秒/毫秒框 -->
        <el-select v-model="value" filterable placeholder="请选择" style="float:left;width: 85px;margin-right: 10px;">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <!-- 时间戳转为时间 -->
      <div style="height:8vh;">
        <!-- 输出框 -->
        <div style="float:left;margin-right: 10px; display: flex;">
          <div style="float:left;margin-right: auto;align-self:center;">时间戳：</div>
          <el-input v-model="input" placeholder="时间戳" style="float:left;width: 160px;margin-right: 10px;" />
        </div>
        <!-- 选择框秒/毫秒框 -->
        <el-select v-model="value" filterable placeholder="请选择" style="float:left;width: 85px;margin-right: 10px;">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <!-- 转换按钮 -->
        <el-button type="primary" style="float:left;width: 70px;margin-right: 10px;" @click="changetime">转换</el-button>
        <!-- 转为时间 -->
        <div class="block" style="float:left;margin-right: 10px;">
          <el-date-picker
            v-model="value2"
            type="datetime"
            placeholder="选择日期"
          />
        </div>
      </div>
      <!-- 介绍 -->
      <div>
        <h3>时间戳</h3>
        <span>Unix 时间戳是从1970年1月1日（UTC/GMT的午夜）开始所经过的秒数，不考虑闰秒。</span>
      </div>
    </el-card>
  </div>
</template>

<script>

export default {
  data() {
    return {
      chosetime: '',
      timestamp: '',
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        }
      },
      value1: '',
      value2: '',
      input: '',
      options: [{
        value: '1',
        label: '秒'
      }, {
        value: '2',
        label: '毫秒'
      }],
      value: ''
    }
  },
  created() {
    var time = new Date()
    this.value1 = time.toLocaleString()
    this.value = this.options[0].value
  },
  methods: {
    changetimestamp() {
      var time = new Date(this.value1)
      if (this.value === '1') {
        this.input = Math.round(time / 1000)
      } else if (this.value === '2') {
        this.input = time.getTime()
      }
    },
    changetime() {
      this.value2 = this.timestampToTime(this.input)
    },
    timestampToTime(timestamp) {
      if (this.value === '1') {
        timestamp = timestamp * 1000
      }
      var time = new Date(timestamp)
      var Y = time.getFullYear() + '-'
      var M = (time.getMonth() + 1 < 10 ? '0' + (time.getMonth() + 1) : time.getMonth() + 1) + '-'
      var D = time.getDate() + ' '
      var h = time.getHours() + ':'
      var m = time.getMinutes() + ':'
      var s = time.getSeconds()
      return Y + M + D + h + m + s
    }

  }
}
</script>

<style>

</style>

