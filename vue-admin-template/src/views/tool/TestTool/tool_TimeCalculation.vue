<template>
    <div class="app-container" style="height:calc(85vh)">
      <el-card style="width: 100%;height: 100%;padding: 0px;">
        <p class="fontstyle" href="../css/common.css">日期计算器</p>
        <div class="block" >
            <span class="demonstration">请选择开始时间：</span>
            <el-date-picker
            v-model="value1"
            type="datetime"
            placeholder="选择日期"
            >
            </el-date-picker>
        </div>
        <div class="block">
            <span class="demonstration">请选择结束时间：</span>
            <el-date-picker
            v-model="value2"
            type="datetime"
            placeholder="选择日期"
            >
            </el-date-picker>
        </div>
        <el-button type="primary" style="width: 100px;margin: 10px 0;" @click="CalcTime()">结果计算</el-button>
        <el-button type="primary" style="width: 80px;margin: 10px 10px;" @click="deltime()">重置</el-button>
        <p v-if="time==''?false:true">结果：{{time}}</p>
      </el-card>
    </div>
  </template>
  
  <script>
import { Message } from 'element-ui'
  
  export default {
    data() {
      return {
        time:"",
        value1: '',
        value2:'',
      }
    },
    created() {
        
    },
    methods: {
        init(){
            this.time =''
        },
        CalcTime(){
            if(this.value1 == '' || this.value2 == ''){
                Message.info("请选择开始时间和结束时间")
            }else{
                var stime = new Date(this.value1).getTime()
                var etime = new Date(this.value2).getTime()
                console.log(stime)
                console.log(etime)
                var usedTime = etime - stime
                var days =Math.floor(usedTime/(24*3600*1000))  //计算出天数
                console.log(days)
                var leave1 = usedTime%(24*3600*1000)  //计算天数后剩余的毫秒数
                console.log(leave1)
                var hours=Math.floor(leave1/(3600*1000)); //计算小时数
                var leave2 = leave1%(3600*1000) //计算小时后剩余的毫秒数
                var minutes = Math.floor(leave2/(60 * 1000))   //计算分钟
                this.time = days + "天"+hours+"时"+minutes+"分";
            }
        }, 
        deltime(){
            this.value1 = ''
            this.value2 = ''
            this.init()
        }
    }
  }
  </script>
  
  <style>
  .block{
    margin: 10px 0;
  }
  </style>
  
  