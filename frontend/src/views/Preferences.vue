<template>
  <div class="prefs">
    <h2>Select your interests (or skip)</h2>
    <div class="tags">
      <label v-for="tag in allTags" :key="tag">
        <input type="checkbox" :value="tag" v-model="selectedTags" />
        {{ tag }}
      </label>
    </div>
    <button @click="save">Save Preferences</button>
    <button @click="$router.push('/')">Skip</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      allTags: ['machine learning', 'web dev', 'data science', 'AI', 'algorithms'],
      selectedTags: []
    }
  },
  methods: {
    async save() {
      const token = localStorage.getItem('token')
      await axios.post('http://127.0.0.1:5000/preferences', {
        preferences: this.selectedTags
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.$router.push('/')
    }
  }
}
</script>
