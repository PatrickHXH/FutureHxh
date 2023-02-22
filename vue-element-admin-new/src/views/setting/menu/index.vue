<template>
  <div class="app-container" style="height:calc(90vh)">
    <el-card style="width: 100%;height: 100%;">
      <!-- 创建菜单按钮 -->
      <div>
        <el-button type="primary" style="margin:10px auto" @click="create">新建菜单</el-button>
      </div>
      <!-- 菜单列表 -->
      <div>
        <el-table
          :data="tableData"
          style="width: 100%;margin-bottom: 20px;"
          row-key="id"
          border
          :fit="true"
          :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
        >
          <el-table-column
            prop="title"
            label="菜单名称"
          />
          <el-table-column
            prop="component"
            label="组件"
          />
          <el-table-column
            prop="path"
            label="路径"
          />
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button-group>
                <el-button
                  size="medium"
                  type="primary"
                  icon="el-icon-edit"
                  @click="handleEdit(scope.$index, scope.row)"
                />
                <el-button
                  size="medium"
                  type="danger"
                  icon="el-icon-delete"
                  @click="handleDelete(scope.$index, scope.row)"
                />
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>

      </div>
      <!-- 调用子组件 -->
      <menuDialog v-if="show" :tid="tid" :rid="rid" :mid="mid" @cancel="closeDialog" />
    </el-card>
  </div>
</template>

<script>
import MenuApi from '@/api/menu'
import { Message } from 'element-ui'
import menuDialog from './menuDialog.vue'
export default {
  components: {
    menuDialog
  },
  data() {
    return {
      tableData: [],
      tid: 0,
      rid: 0,
      mid: 0,
      show: false
    }
  },
  mounted() {
    this.menuList()
  },
  methods: {
    async menuList() {
      const resp = await MenuApi.menuList()
      if (resp.data.success === true) {
        this.tableData = resp.data.result
      } else {
        Message.error(resp.data.error.msg)
      }
    },
    create() {
      this.showDialog()
      this.tid = 0
    },
    showDialog() {
      this.show = true
    },
    closeDialog() {
      this.show = false
      this.menuList()
    },
    handleEdit(index, row) {
      this.show = true
      this.tid = 1
      this.mid = row.id
    },
    // 删除菜单
    async handleDelete(index, row) {
      const resp = await MenuApi.delete(row.id)
      if (resp.data.success === true) {
        Message.success('删除成功')
        this.menuList()
      } else {
        Message.error(resp.data.error.msg)
      }
    }
  }
}
</script>
