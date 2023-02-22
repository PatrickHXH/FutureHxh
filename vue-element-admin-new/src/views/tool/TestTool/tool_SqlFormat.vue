<template>
  <div class="app-container" style="height:calc(85vh)">
    <el-card style="width: 100%;height: 100%;padding: 0px;">
      <p class="fontstyle" href="../css/common.css">SQL格式转换</p>
      <div class="codebefore">
        <codemirror
          ref="myCm"
          :value="code"
          :options="cmOptions"
          @ready="onCmReady"
          @focus="onCmFocus"
          @input="onCmCodeChange"
        />

      </div>
      <i class="el-icon-right" />
      <div class="codeafter">
        <codemirror
          ref="myCm"
          :value="formatcode"
          :options="formatOptions"
          @ready="onCmReady"
          @focus="onCmFocus"
          @input="onCmCodeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import sqlFormatter from 'sql-formatter'
import { codemirror } from 'vue-codemirror'
import 'vue-codemirror/node_modules/codemirror/lib/codemirror.css'
import 'vue-codemirror/node_modules/codemirror/theme/paraiso-light.css'
import 'vue-codemirror/node_modules/codemirror/theme/twilight.css'
import 'vue-codemirror/node_modules/codemirror/mode/sql/sql.js'
import '@/views/tool/css/common.css'
var intervalID
export default {
  components: { codemirror },
  data() {
    return {
      code: '',
      formatcode: '',
      cmOptions: {
        // codemirror options
        tabSize: 4,
        mode: 'sql',
        theme: 'paraiso-light',
        lineNumbers: true,
        line: true,
        autoRefresh: true
        // more codemirror options, 更多 codemirror 的高级配置...
      },
      formatOptions: {
        // codemirror options
        tabSize: 4,
        mode: 'sql',
        theme: 'twilight',
        lineNumbers: true,
        line: true,
        autoRefresh: true
        // more codemirror options, 更多 codemirror 的高级配置...
      }
    }
  },
  mounted() {
    intervalID = setInterval(this.changeformat, 2000)
  },
  beforeDestroy() {
    clearInterval(intervalID)
    console.log('清除定时器')
  },
  methods: {
    changeformat() {
      this.formatcode = sqlFormatter.format(this.formatcode)
      console.log(this.formatcode)
    },
    onCmReady(cm) {
      console.log('the editor is readied!', cm)
    },
    onCmFocus(cm) {
      console.log('the editor is focus!', cm)
      this.changeformat()
    },
    onCmCodeChange(newCode) {
      console.log('this is new code', newCode)
      this.formatcode = newCode
    }
  }

}
</script>

<style>
.CodeMirror{
  height: calc(70vh);
}
.codebefore {
    float: left;
    width: 48%;
}
.codeafter{
    float: right;
    width: 48%;
}
/* p.fontstyle{
  color:hsl(0, 38%, 55%);
  font-family: "微软雅黑";
  font-size: 20px;
  margin: 10px 0;
} */
.el-icon-right{
  font-size: 60px;
  position:fixed;
  bottom:40%
}
</style>
