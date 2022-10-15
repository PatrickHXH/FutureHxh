<template>
  <div class="dashboard-container">
    <div class="dashboard-text">欢迎：{{ user }}</div>
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      user: ''
    }
  },
  created() {
    this.user = sessionStorage.getItem('user')
  },
  methods: {
    // logout() {
    //   console.log("退出登录");
    //   sessionStorage.token = "";
    //   sessionStorage.user = "";
    //   this.$router.push({
    //     path: "/login",
    //   });
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
