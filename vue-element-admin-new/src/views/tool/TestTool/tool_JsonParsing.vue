<template>
  <div class="app-container" style="height:calc(85vh)">
    <el-card style="width: 100%;height: 100%;padding: 0px;">
      <p class="fontstyle" href="../css/common.css">在线JSON校验格式化工具</p>
      <vue-json-editor
        v-model="resultInfo"
        :show-btns="false"
        :mode="'code'"
        lang="zh"
        @json-change="onJsonChange"
        @json-save="onJsonSave"
      />
    </el-card>
  </div>
</template>

  <!-- {"employees":[{"firstName":"Bill","lastName":"Gates"},{"firstName":"George","lastName":"Bush"},{"firstName":"Thomas","lastName":"Carter"}]} -->
<script>
import vueJsonEditor from 'vue-json-editor'

export default {
  components: { vueJsonEditor },
  data() {
    return {
      resultInfo: {},
      desc: ''
    }
  },
  created() {

  },
  methods: {
    // json编辑器内容变化
    onJsonChange(value) {
      console.log('value:', value)
    },
    // json编辑器内容保存
    onJsonSave(value) {
      console.log('value:', value)
    }
  }
}
</script>

<style>
.jsoneditor-vue{
  height: 70vh;
}
div.jsoneditor-menu{
  background-color: #5a5e66;
}
div.jsoneditor-menu a.jsoneditor-poweredBy{
  font-size: 0;
}
</style>
