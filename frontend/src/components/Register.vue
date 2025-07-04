<template>
  <div class="container">
    <div class="form-container">
      <h2>Регистрация</h2>
      <form @submit.prevent="register">
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
        <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
        <router-link to="/login" class="btn">Войти</router-link>
      </form>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      success: ''
    }
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://localhost:8000/register', {
          username: this.username,
          password: this.password
        })
        
        this.success = 'Регистрация успешна! Теперь вы можете войти.'
        this.error = ''
        this.username = ''
        this.password = ''
      } catch (error) {
        this.error = 'Ошибка регистрации. Возможно, пользователь уже существует.'
        this.success = ''
        console.error('Register error:', error)
      }
    }
  }
}
</script>
