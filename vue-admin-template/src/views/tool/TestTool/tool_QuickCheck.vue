<template>
  <div class="app-container" style="height:calc(85vh)">
    <el-card style="width: 100%;height: 100%;padding: 0px;">
      <el-divider direction="vertical" class="titleline" />
      <p href="../css/common.css" class="fontstyle">速查表</p>
      <el-row>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/git.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-git.png" class="image">
                  <span class="top-title">GIT</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">Git是一个免费的开源分布式版本控制系统，旨在快速高效地处理从小型到大型项目的所有内容。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/cron.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/CronTab.svg" class="image">
                  <span class="top-title">Cron</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">Cron 最适合安排重复性任务。 可以使用关联的 at 实用程序来完成一次性任务的调度</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/javascript.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/JavaScript.svg" class="image" style="width:30px">
                  <span class="top-title">JavaScript</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">包含最重要概念、函数、方法等的 JavaScript 备忘单。 初学者的完整快速参考。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/mysql.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-mysql.png" class="image">
                  <span class="top-title">MySql</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">MySQL是一个关系型数据库管理系统，由瑞典MySQL AB
                公司开发，属于 Oracle 旗下产品。MySQL
                是最流行的关系型数据库管理系统之一，在 WEB
                应用方面，MySQL是最好的 RDBMS (Relational Database Management
                System，关系数据库管理系统) 应用软件之一。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/nginx.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-nginx.png" class="image" style="width:28px">
                  <span class="top-title">Nginx</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">Nginx是一款轻量级的HTTP服务器，采用事件驱动的异步非阻塞处理方式框架，这让其具有极好的IO性能，时常用于服务端的反向代理和负载均衡。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/python.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-python.png" class="image">
                  <span class="top-title">Python</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">Nginx是一款轻量级的HTTP服务器，采用事件驱动的异步非阻塞处理方式框架，这让其具有极好的IO性能，时常用于服务端的反向代理和负载均衡。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="http://redisdoc.com/" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-redis.png" class="image" style="width:27px;height:24px">
                  <span class="top-title">Redis</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">Redis是一个开源的使用ANSI
                C语言编写、遵守BSD协议、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/regex.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-reg.png" class="image" style="width:49px;height:32px">
                  <span class="top-title">正则表达式</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">正则表达式(regular expression)描述了一种字符串匹配的模式（pattern），可以用来检查一个串是否含有某种子串、将匹配的子串替换或者从某个串中取出符合某个条件的子串等。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/bash.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-shell.png" class="image" style="height:24px">
                  <span class="top-title">Shell</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">Shell 是一个应用程序，它连接了用户和 Linux
                内核，让用户能够更加高效、安全、低成本地使用 Linux
                内核，这就是 Shell 的本质。Shell
                也是一种编程语言，它的编译器（解释器）是 Shell
                这个程序。我们平时所说的
                Shell，有时候是指连接用户和内核的这个程序，有时候又是指 Shell
                编程。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/vim.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-vim.png" class="image">
                  <span class="top-title">Vim</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">Vim是从 vi
                发展出来的一个文本编辑器。代码补完、编译及错误跳转等方便编程的功能特别丰富，在程序员中被广泛使用。和Emacs并列成为类Unix系统用户最喜欢的编辑器。</span>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card :body-style="{ padding: '0px' }" class="listcard" shadow="hover">
            <div style="padding: 10px;">
              <a href="https://quickref.cn/docs/css.html" target="__blank">
                <div class="classify-descItem-top">
                  <img src="../icon/ic-css-order.png" class="image" style="width:28px;height:32px">
                  <span class="top-title">CSS</span>
                </div>
              </a>
              <div class="classify-descItemLine" />
              <span class="item-desc">一份关于 CSS 优点的快速参考备忘单，列出了选择器语法、属性、单位和其他有用的信息</span>
            </div>
          </el-card>
        </el-col>

      </el-row>
    </el-card>
  </div>
</template>

<script>

export default {

  data() {
    return {

    }
  },
  created() {

  },
  methods: {

  }
}
</script>

<style>
.time {
font-size: 13px;
color: #999;
}

.bottom {
margin-top: 13px;
line-height: 12px;
}

.button {
padding: 0;
float: right;
}

.image {
width: 32px;
height: 32px;
display: block;
}

.top-title{
    margin: 0 10px;
}
.classify-descItem-top {
    width: 100%;
    height: px;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.item-desc {
    font-size: 12px;
    color: #5d5d5d;
    margin-left: 15px;
    margin-right: 15px;
    margin-top: 10px;
    text-overflow: ellipsis;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
.classify-descItemLine {
    width: 200px;
    margin: 10px 10px;
    height: 0;
    border-top: 1px solid #dcdcdc;
    background-color: "#dcdcdc";
}
.listcard{
    height:110px;
    margin-right: 15px;
    margin-top: 15px;
}
.titleline{
    width: 8px;
    height: 22px;
    float: left;
    background-color: hsl(0, 38%, 55%);
}
</style>

