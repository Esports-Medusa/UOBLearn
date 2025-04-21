<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <select v-model="form.role" required>
        <option disabled value="">Select Role</option>
        <option value="student">Student</option>
        <option value="mentor">Mentor</option>
      </select><br>

      <input v-model="form.username" type="text" placeholder="Username" required /><br>
      <input v-model="form.email" type="email" placeholder="Email" required /><br>
      <input v-model="form.password" type="password" placeholder="Password" required /><br>

      <button type="submit">Register</button>
    </form>
    <p v-if="message">{{ message }}</p>

    <!-- ✅ Preference settings modal -->
    <div v-if="showPreferences" class="modal-overlay">
      <div class="modal-content">
        <h3>Select Your Preferences</h3>
        <div class="tags">
          <label v-for="tag in allTags" :key="tag">
            <input type="checkbox" :value="tag" v-model="preferences" />
            {{ tag }}
          </label>
        </div>
        <div class="modal-buttons">
          <button @click="savePreferences">Save</button>
          <button @click="skipPreferences">Skip</button>
        </div>
      </div>
    </div>
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
      message: '',
      showPreferences: false,
      preferences: [],
      allTags: ['AI', 'machine learning', 'web dev', 'data science', 'algorithms']
    }
  },
  methods: {
    async handleRegister() {
      try {
        const res = await axios.post('http://127.0.0.1:5000/register', this.form)
        this.message = res.data.msg

        // ✅ Display preference settings modal.
        this.showPreferences = true
      } catch (err) {
        console.error(err)
        this.message = err.response?.data?.msg || err.message || 'Registration failed'
      }
    },
    async savePreferences() {
      try {
        await axios.post('http://127.0.0.1:5000/preferences', {
          email: this.form.email,
          preferences: this.preferences
        })
      } catch (err) {
        console.error('Failed to save preferences')
      } finally {
        this.showPreferences = false
        this.$router.push('/')
      }
    },
    skipPreferences() {
      this.showPreferences = false
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
input, select {
  margin: 5px 0;
  padding: 8px;
  width: 250px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
}

.tags label {
  display: block;
  margin: 5px 0;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}
</style>
