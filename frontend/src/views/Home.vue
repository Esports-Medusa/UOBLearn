<template>
  <div>
    <main class="main-content">
      <h2>📚 Recommended Courses</h2>

      <div v-if="!token">
        <p>Please <router-link to="/login">log in</router-link> to see your recommendations.</p>
      </div>

      <div v-else-if="courses.length === 0">
        <p>No recommendations available yet.</p>
      </div>

      <div v-else class="course-list">
        <div class="course-card" v-for="course in courses" :key="course.title">
          <h3>
            <a :href="course.url" target="_blank" rel="noopener noreferrer">
              {{ course.title }}
            </a>
            <span class="platform">({{ course.platform }})</span>
          </h3>
          <p>{{ course.description }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      token: localStorage.getItem('token'),
      courses: []
    }
  },
  async mounted() {
    if (!this.token) return

    try {
      const res = await axios.get('http://127.0.0.1:5000/recommend', {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      })
      this.courses = res.data
    } catch (err) {
      console.error('❌ Failed to load courses:', err)
    }
  }
}
</script>

<style scoped>
.main-content {
  padding: 20px;
  font-family: sans-serif;
}

.course-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.course-card {
  border: 1px solid #ddd;
  padding: 16px;
  border-radius: 6px;
  background-color: #fafafa;
}

.course-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.course-card a {
  color: #2c3e50;
  text-decoration: none;
}

.course-card a:hover {
  text-decoration: underline;
}

.platform {
  font-size: 14px;
  color: #666;
}
</style>
