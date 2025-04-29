<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="form.email" type="email" placeholder="Email" required /><br>
      <input v-model="form.password" type="password" placeholder="Password" required /><br>
      <button type="submit">Login</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      message: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const res = await axios.post('http://127.0.0.1:5000/login', this.form)
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('username', res.data.username)
        localStorage.setItem('email', res.data.email)
        localStorage.setItem('is_first_login', res.data.is_first_login)
        this.$router.push('/')
      } catch (err) {
        this.message = err.response?.data?.msg || 'Login failed'
      }
    }
  }
}
</script>

<style scoped>
input {
  margin: 5px 0;
  padding: 8px;
  width: 250px;
}
</style>
