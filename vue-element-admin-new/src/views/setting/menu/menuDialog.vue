<template>
  <div>
    <el-dialog
      :title="showtitle"
      :visible.sync="dialogVisible"
      :before-close="closeDialog"
      width="30%"
      center
    >
      <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">
        <el-form-item label="菜单名称" prop="title">
          <el-input v-model="ruleForm.title" />
        </el-form-item>
        <el-form-item label="父级菜单" prop="menuLabel">
          <el-select v-model="ruleForm.menuLabel" placeholder="请选择父级菜单" :disabled="checked===true?true:false">
            <el-option :value="ruleForm.menuValue" :label="ruleForm.menuLabel" style="height:100px;overflow: auto;background-color:#fff;padding: 0;">
              <el-tree :data="menuOptions" :props="defaultProps" @node-click="handleNodeClick" />
            </el-option>
          </el-select>
          <el-checkbox v-model="checked" style="margin-left: 10px;" @change="check">顶级</el-checkbox>
        </el-form-item>
        <el-form-item label="路由地址" prop="path">
          <el-input v-model="ruleForm.path" />
        </el-form-item>
        <el-form-item label="前端组件" prop="cmp">
          <el-input v-model="ruleForm.cmp" />
        </el-form-item>
        <el-form-item label="是否可见">
          <el-switch v-model="ruleForm.hidden" :active-value="false" :inactive-value="true" @change="switchChange" />
        </el-form-item>
        <el-form-item label="图标" prop="icon" style="">
          <div class="server-name-div">
            <el-input v-model="ruleForm.icon" class="server-name-input" />
            <el-popover
              v-model="visible"
              placement="right"
              trigger="click"
              width="800"
            >
              <el-button slot="reference" icon="el-icon-search" class="server-name-button" />
              <icon @cancel="iconEvent()" />
            </el-popover>
          </div>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeDialog">取 消</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import icon from '@/views/icons/index.vue'
import { Message } from 'element-ui'
import MenuApi from '@/api/menu'
export default {
  // props: { tid: { type: Object, default: null }, rid: { type: Object, default: null }},
  components: {
    icon
  },
  props: ['tid', 'rid', 'mid'],
  data() {
    return {
      menuOptions: [],
      dialogVisible: true,
      ruleForm: {
        title: '',
        cmp: '',
        icon: '',
        path: '',
        hidden: false,
        menuLabel: '',
        menuValue: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入菜单名称', trigger: 'blur' }
        ],
        path: [
          { required: true, message: '请输入路由地址', trigger: 'blur' }
        ],
        cmp: [
          { required: true, message: '请输入前端组件', trigger: 'blur' }
        ]
      },
      // 树形对应
      defaultProps: {
        children: 'children',
        label: 'title'
      },
      checked: true,
      parent_id: 0,
      iconShow: false,
      visible: false
    }
  },
  // 触发生命周期，判断标题
  created() {
    this.iconEvent()
    if (this.tid === 0) {
      this.showtitle = '新建菜单'
      this.initMenuList()
      this.check()
    } else {
      this.initMenudetail()
      this.initMenuList()
      this.showtitle = '编辑菜单'
    }
  },
  methods: {
    // 调用父组件 关闭弹窗
    closeDialog() {
      this.$emit('cancel', {})
    },
    // 创建、编辑项目
    submitForm(formname) {
      this.$refs[formname].validate(valid => {
        if (valid) {
          if (this.tid === 0) {
            MenuApi.create({
              path: this.ruleForm.path,
              title: this.ruleForm.title,
              component: this.ruleForm.cmp,
              hidden: this.ruleForm.hidden,
              icon: this.ruleForm.icon,
              parent_id: this.ruleForm.menuValue
            }).then(resp => {
              if (resp.data.success === true) {
                Message.success('创建成功')
                this.closeDialog()
              } else {
                Message.error(resp.data.error.msg)
              }
            })
          } else {
            MenuApi.update(this.mid, {
              path: this.ruleForm.path,
              title: this.ruleForm.title,
              component: this.ruleForm.cmp,
              hidden: this.ruleForm.hidden,
              icon: this.ruleForm.icon,
              parent_id: this.ruleForm.menuValue }).then(resp => {
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
    async initMenudetail() {
      const resp = await MenuApi.menuDetail(this.mid)
      if (resp.data.success === true) {
        this.ruleForm.title = resp.data.result.title
        this.ruleForm.cmp = resp.data.result.component
        this.ruleForm.icon = resp.data.result.icon
        this.ruleForm.path = resp.data.result.path
        this.ruleForm.hidden = resp.data.result.hidden
        if (resp.data.result.parent_id === 0) {
          this.ruleForm.menuLabel = ''
          this.ruleForm.menuValue = 0
          this.checked = true
        } else {
          this.ruleForm.menuLabel = resp.data.result.parent_title
          this.ruleForm.menuValue = resp.data.result.parent_id
          this.checked = false
        }
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    // 获取菜单列表
    async initMenuList() {
      const resp = await MenuApi.menuList()
      if (resp.data.success === true) {
        this.menuOptions = resp.data.result
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    // 选择菜单节点
    handleNodeClick(data) {
      // this.pidTemp.id = data.id
      this.ruleForm.menuValue = data.id
      this.ruleForm.menuLabel = data.title
      // this.pidTemp.title = data.title
    },
    // 展示icon弹窗
    showiconDialog() {
      this.iconShow = true
    },
    // 选择顶级复选框
    check() {
      if (this.checked === true) {
        console.log('change')
        this.ruleForm.menuLabel = ''
        this.ruleForm.menuValue = 0
      }
    },
    // 选择图标是触发
    iconEvent() {
      this.visible = false
      document.addEventListener('copy', () => {
        const text = window.getSelection().toString()
        console.log(text)
        this.ruleForm.icon = text
      })
      // if(window.isSecureContext){
      //   navigator.clipboard.readText().then((cliptext) => this.ruleForm.icon = cliptext)
      // }else{

      // }
    },
    switchChange(check) {
      console.log(check)
      // if(check===true){
      //   this.ruleForm.hidden = false
      // }else{
      //   this.ruleForm.hidden = true
      // }
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
.el-select .el-input {
width: 130px;
}
.input-with-select .el-input-group__prepend {
background-color: #fff;
}
.server-name-div{
  width: 270px;
  display: flex;
}
.server-name-button{

}
.server-name-input {

}
</style>

