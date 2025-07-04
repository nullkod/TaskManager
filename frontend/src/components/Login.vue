<template>
  <div class="container">
    <div class="form-container">
      <h2>Вход в систему</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Имя пользователя:</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required
          >
        </div>
        <div class="form-group">
          <label for="password">Пароль:</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
          >
        </div>
        <button type="submit" class="btn btn-primary">Войти</button>
        <router-link to="/register" class="btn">Регистрация</router-link>
      </form>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async login() {
      try {
        const formData = new FormData()
        formData.append('username', this.username)
        formData.append('password', this.password)
        
        const response = await axios.post('http://localhost:8000/login', formData)
        
        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/tasks')
      } catch (error) {
        this.error = 'Ошибка входа. Проверьте имя пользователя и пароль.'
        console.error('Ошибка входа:', error)
      }
    }
  }
}
</script>
