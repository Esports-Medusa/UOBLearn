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
        this.message = res.data.msg
      } catch (err) {
        this.message = err.response?.data?.msg || 'Login failed'
      }
    }
  }
}
</script>
