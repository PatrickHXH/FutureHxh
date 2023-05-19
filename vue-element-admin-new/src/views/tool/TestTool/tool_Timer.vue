<template>
    <div class="app-container" style="height:calc(85vh)">
      <el-card style="width: 100%;height: 100%;padding: 0px;">
        <div class="timer_contain">
        <div class="time" v-if="rptType" @click="reset" >{{str}}</div>
        <div class="receipt" :class="rptType?'jdz':'jiedan'" @click="receipt">计时</div>
        </div>

      </el-card>
    </div>

  </template>
  
<script>
import screenfull from 'screenfull';
  export default {
    components: {  },
    data() {
      return{
        rptType: false,//状态
        h:0,//定义时，分，秒，毫秒并初始化为0；
        m:0,
        ms:0,
        s:0,
        time:0,
        str:'',
        screenState: false // 屏幕的状态
        }
    },
    created() {
      
    },
    mounted:function(){
        this.$nextTick(function(){//整个视图都渲染完毕
    })
    },
    methods:{
        getTask: function(e){
            this.taskType = e;
        },
        //开始
        receipt: function() {
            this.rptType = !this.rptType;
            if(this.rptType){
            this.time=setInterval(this.timer,50);
            }else{
            this.reset()
            }
        },
        timer: function(){   //定义计时函数
            this.ms=this.ms+50;         //毫秒
            if(this.ms>=1000){
            this.ms=0;
            this.s=this.s+1;         //秒
            }
            if(this.s>=60){
            this.s=0;
            this.m=this.m+1;        //分钟
            }
            if(this.m>=60){
            this.m=0;
            this.h=this.h+1;        //小时
            }
            this.str =this.toDub(this.h)+":"+this.toDub(this.m)+":"+this.toDub(this.s)+":"+this.toDub(this.ms)/*+this.toDubms(this.ms)+"毫秒"*/;
            // document.getElementById('mytime').innerHTML=h+"时"+m+"分"+s+"秒"+ms+"毫秒";
        },
        toDub: function(n){  //补0操作
            if(n<10){
            return "0"+n;
            }
            else {
            return ""+n;
            }
        },
        reset: function(){  //重置
            clearInterval(this.time);
            this.h=0;
            this.m=0;
            this.ms=0;
            this.s=0;
            this.str="00:00:00:000";
            this.rptType =false
        },

    }

  }
</script>
  
<style>
.time{
    font-size: 13.5vw;
    color: red;
    height: 80vh;
    /* width: 100%; */
    display: flex;
	align-items: center;
    vertical-align: middle
}
.receipt{
    font-size: 15vw;
    font-family: "宋体";
    color: black;
    height: 80vh;
    display: flex;
	align-items: center;
    vertical-align: middle;
    text-align:center
}
</style>