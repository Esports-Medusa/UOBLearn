<template>
  <div class="account">
    <h2>My Account</h2>
    <div v-if="isLoggedIn">
      <p><strong>Welcome,</strong> {{ username }}!</p>
      <p><strong>Email:</strong> {{ email }}</p>
    </div>
    <div v-else>
      <p>Please <router-link to="/login">log in</router-link> to view your account.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: localStorage.getItem('username') || '',
      email: localStorage.getItem('email') || '' // 这里email后面补充存一下
    }
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    }
  }
}
</script>

<style scoped>
.account {
  padding: 20px;
  font-family: sans-serif;
}
</style>
