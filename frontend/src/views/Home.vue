<template>
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
</template>

<script>
import axios from 'axios'
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const token = ref(localStorage.getItem('token'))
    const courses = ref([])

    const fetchCourses = async () => {
      token.value = localStorage.getItem('token')  // 🧠 每次调用都刷新 token

      if (!token.value) {
        courses.value = []
        return
      }

      try {
        const res = await axios.get('http://127.0.0.1:5000/recommend', {
          headers: {
            Authorization: `Bearer ${token.value}`
          }
        })
        courses.value = res.data
      } catch (err) {
        console.error('❌ Failed to load courses:', err)
        courses.value = []
      }
    }

    onMounted(fetchCourses)

    // 💡 关键：每次路由变化，重新获取 token + 刷新课程
    watch(() => route.fullPath, () => {
      fetchCourses()
    })

    return {token, courses}
  }
}
</script>

<style scoped>
.main-content {
  padding: 20px;
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

.platform {
  font-size: 14px;
  color: #666;
}
</style>
