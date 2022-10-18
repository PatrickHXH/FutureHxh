<template>
  <div class="dashboard-container">
    <div class="dashboard-text">欢迎：{{ user }}</div>
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'
import {UserKey} from '@/utils/auth'
import Cookies from 'js-cookie'
export default {
  data() {
    return {
      user: ''
    }
  },
  created() {
    this.user =Cookies.get(UserKey).username
  },
  methods: {
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
