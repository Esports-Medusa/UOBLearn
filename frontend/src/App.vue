<template>
  <div>
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/">Main</router-link> |
        <router-link to="/mentor">Meet with your mentor</router-link>
      </div>
      <div class="nav-right">
        <template v-if="isLoggedIn">
          <router-link to="/account">{{ username }}</router-link> |
          <button @click="logout" class="logout-btn">Exit</button>
        </template>
        <template v-else>
          <router-link to="/register">Register</router-link> |
          <router-link to="/login">Login</router-link>
        </template>
      </div>
    </nav>

    <router-view />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const isLoggedIn = ref(false)
    const username = ref('')

    const syncLoginStatus = () => {
      const token = localStorage.getItem('token')
      const name = localStorage.getItem('username')
      isLoggedIn.value = !!token
      username.value = name || ''
    }

    const logout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('email')
      syncLoginStatus()
      router.push('/')
    }

    const router = useRouter()

    onMounted(() => {
      syncLoginStatus()
      // Automatically update status of login
      router.afterEach(() => {
        syncLoginStatus()

        const isFirstLogin = localStorage.getItem('is_first_login')
        if (isFirstLogin === 'true') {
          localStorage.setItem('is_first_login', false)
          router.push('/preferences')
        }
      })
    })

    return {
      isLoggedIn,
      username,
      logout
    }
  }
}
</script>


<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: #f4f4f4;
  border-bottom: 1px solid #ccc;
  font-family: sans-serif;
}

.nav-left a,
.nav-right a {
  margin-right: 15px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.logout-btn {
  background: none;
  border: none;
  color: #333;
  font-weight: bold;
  cursor: pointer;
}

.logout-btn:hover {
  text-decoration: underline;
}
</style>
