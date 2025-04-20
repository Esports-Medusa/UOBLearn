<template>
  <div>
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/">Main</router-link> |
        <router-link to="/mentor">Meet with your mentor</router-link> |
        <router-link to="/account">My account</router-link>
      </div>
      <div class="nav-right">
        <router-link to="/register">Register</router-link> |
        <router-link to="/login">Login</router-link>
      </div>
    </nav>

    <router-view />
  </div>
</template>

<script setup>
// 无需引入其他组件
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

.nav-right {
  white-space: nowrap;
}
</style>
