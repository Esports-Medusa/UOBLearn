<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <select v-model="form.role" required>
        <option disabled value="">Select Role</option>
        <option value="student">Student</option>
        <option value="mentor">Mentor</option>
      </select><br />

      <input v-model="form.username" type="text" placeholder="Username" required /><br />
      <input v-model="form.email" type="email" placeholder="Email" required /><br />
      <input v-model="form.password" type="password" placeholder="Password" required /><br />

      <button type="submit">Register</button>
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
        role: '',
        username: '',
        email: '',
        password: ''
      },
      message: ''
    }
  },
  methods: {
    async handleRegister() {
      try {
        const res = await axios.post('http://127.0.0.1:5000/register', this.form)

        // ✅ 保存登录状态（自动登录）
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('username', res.data.username)
        localStorage.setItem('email', res.data.email)
        localStorage.setItem('is_first_login', res.data.is_first_login)

        // ✅ 跳转主页，App.vue will handle redirection to /preferences if needed
        this.$router.push('/')
      } catch (err) {
        this.message = err.response?.data?.msg || 'Registration failed'
      }
    }
  }
}
</script>

<style scoped>
input,
select {
  margin: 5px 0;
  padding: 8px;
  width: 250px;
}
</style>
