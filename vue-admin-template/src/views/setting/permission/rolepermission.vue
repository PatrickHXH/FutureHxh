<template>
    <div class="app-container" style="height:calc(95vh)">
      <el-card style="width: 100%;height: 100%;padding: 0px;">
        <!-- 返回上一页 -->
        <div>
            <el-page-header @back="returnLastPage" content="授权权限"></el-page-header>
        </div>
        <div style="margin:20px 0"></div>
        <!-- 权限列表 -->
        <div class="per-group" v-infinite-scroll="load" style="overflow:auto">
        <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange" >全选</el-checkbox>
        <div style="margin: 15px 0;"></div>
        <el-checkbox-group v-model="checkedPer" @change="handlecheckedPerChange">
            <div class="per-group-cloumn" v-infinite-scroll="true">
            <el-checkbox  
                class="per-group-item" 
                v-for="per in  perOptions" 
                :label="per.id" 
                :key="per.name">{{per.name}}</el-checkbox>
        </div>
        </el-checkbox-group>
        </div>
        <!-- 保存按钮 -->
        <div style="margin:20px 0">
            <el-button type="primary" style="float:right" @click="saveRolePer()">保存</el-button>
        </div>
      </el-card>
    </div>
  </template>
  
<script>
import { Message } from 'element-ui'
import PermissionApi from '@/api/permission'
// const perOptions = [];
export default {
props: [],
components: { },
data() {
    return {
        perOptions:[],
        Options:[],
        checkAll: false,
        checkedPer: [],
        isIndeterminate: true,
        count: 0
    }
},
created() {
    this.initPermissionList()
},
beforeDestroy(){

},
methods: {
    returnLastPage(){
        this.$router.push({path:"/permisssion/index"})
    },
    handleCheckAllChange(val) {
        console.log(val)
        this.checkedPer = val ? this.Options:[];
        this.isIndeterminate = false;
      },
    handlecheckedPerChange(value) {
        let checkedCount = value.length;
        this.checkAll = checkedCount === this.perOptions.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.perOptions.length;
        this.checkedPer = []
        for(let i=0;i<value.length;i++){
            this.checkedPer.push(value[i])
        }
    },
    async initPermissionList(){
        const resp = await PermissionApi.getroleperlist(this.$route.query.id)
        console.log('列表', resp)
        if (resp.data.success === true) {
            // Message.success("获取列表成功")
            for(let i=0; i < resp.data.result.length;i++){
                this.perOptions.push({
                    name:resp.data.result[i].name,
                    id:resp.data.result[i].id
                })
                this.Options.push(resp.data.result[i].id)
                if(resp.data.result[i].has_per == true){
                    this.checkedPer.push(resp.data.result[i].id)
                }
            }
            console.log(this.perOptions)
        } else {
            Message.error(resp.data.error.msg)
    }
    },
    load(){},
    async saveRolePer(){
        const resp = await PermissionApi.roleperupdate({
            permission_id:this.checkedPer,
            group_id:this.$route.query.id
        })
        if (resp.data.success === true) {
            Message.success("保存成功")
            this.returnLastPage()
        } else {
            Message.error(resp.data.error.msg)
    }
    }
}
}
</script>

<style>
.per-group{
    display: flex;
    height: 75vh;
}
.per-group-cloumn{
    display: flex;
    flex-direction:column;
    margin:0 20px;
    
}
.per-group-item{
    margin: 4px 0;

}
</style>
  
  