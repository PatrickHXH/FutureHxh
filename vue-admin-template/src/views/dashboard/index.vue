<template>
  <div class="dashboard-container">
    <div class="dashboard-text">欢迎：{{ user }}</div>
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'
import { getInfo } from '@/api/user'
import TokenKey from '@/utils/auth'
import Cookies from 'js-cookie'
export default {
  data() {
    return {
      user: ''
    }
  },
  created() {
    this.GetInfo()
  },
  methods: {
    async GetInfo() {
      this.token_obj = Cookies.get(TokenKey)
      const resp = await getInfo({ token: this.token_obj.vue_admin_token })
      this.user = resp.data.result.username
    }
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
