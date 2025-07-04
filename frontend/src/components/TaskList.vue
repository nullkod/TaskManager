<template>
  <div class="container">
    <div class="header">
      <h1>Список задач</h1>
      <button @click="logout" class="btn btn-danger">Выйти</button>
    </div>

    <!-- Форма добавления задачи -->
    <div class="form-container">
      <h3>Добавить новую задачу</h3>
      <form @submit.prevent="addTask">
        <div class="form-group">
          <label for="title">Заголовок:</label>
          <input 
            type="text" 
            id="title" 
            v-model="newTask.title" 
            required
          >
        </div>
        <div class="form-group">
          <label for="description">Описание:</label>
          <textarea 
            id="description" 
            v-model="newTask.description" 
            rows="3"
          ></textarea>
        </div>
        <button type="submit" class="btn btn-success">Добавить задачу</button>
      </form>
    </div>

    <div class="filters">
        <select v-model="statusFilter" class="form-control">
            <option value="all">Все задачи</option>
            <option value="completed">Выполненные</option>
            <option value="not_completed">Не выполненные</option>
        </select>
        <select v-model="sortBy" class="form-control">
            <option value="created_at">По дате создания</option>
            <option value="status">По статусу</option>
            <option value="title">По названию</option>
        </select>
    </div>

    <!-- Список задач -->
    <div class="tasks-container">
      <div 
        v-for="task in filteredAndSortedTasks" 
        :key="task.id" 
        class="task-item"
        :class="{ completed: task.status }"
      >
        <div class="task-header">
          <h4>{{ task.title }}</h4>
          <div class="task-actions">
            <button 
              @click="toggleTask(task)" 
              class="btn"
              :class="task.status ? 'btn-success' : 'btn-primary'"
            >
              {{ task.status ? 'Выполнено' : 'Не выполнено' }}
            </button>
            <button @click="editTask(task)" class="btn btn-primary">Изменить</button>
            <button @click="deleteTask(task.id)" class="btn btn-danger">Удалить</button>
          </div>
        </div>
        <p v-if="task.description">{{ task.description }}</p>
        <small>Создано: {{ formatDate(task.created_at) }}</small>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div v-if="editingTask" class="modal">
      <div class="modal-content">
        <h3>Редактировать задачу</h3>
        <form @submit.prevent="saveTask">
          <div class="form-group">
            <label>Заголовок:</label>
            <input type="text" v-model="editingTask.title" required>
          </div>
          <div class="form-group">
            <label>Описание:</label>
            <textarea v-model="editingTask.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>
              <input type="checkbox" v-model="editingTask.status">
              Выполнено
            </label>
          </div>
          <button type="submit" class="btn btn-success">Сохранить</button>
          <button type="button" @click="cancelEdit" class="btn">Отмена</button>
        </form>
      </div>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TaskList',
  data() {
    return {
      tasks: [],
      newTask: {
        title: '',
        description: ''
      },
      editingTask: null,
      showCompleted: true,
      sortBy: 'created_at',
      error: '',
      statusFilter: 'all',
    }
  },
  computed: {

    filteredAndSortedTasks() {
    let filtered = this.tasks

    if (this.statusFilter === 'completed') {
      filtered = filtered.filter(task => task.status)
    } else if (this.statusFilter === 'not_completed') {
      filtered = filtered.filter(task => !task.status)
    }

    return filtered.sort((a, b) => {
      if (this.sortBy === 'created_at') {
        return new Date(b.created_at) - new Date(a.created_at)
      } else if (this.sortBy === 'status') {
        return a.status - b.status
      } else if (this.sortBy === 'title') {
        return a.title.localeCompare(b.title)
      }
      return 0
    })
  }

    // filteredAndSortedTasks() {
    //   let filtered = this.tasks
      
    //   if (!this.showCompleted) {
    //     filtered = filtered.filter(task => !task.status)
    //   }
      
    //   return filtered.sort((a, b) => {
    //     if (this.sortBy === 'created_at') {
    //       return new Date(b.created_at) - new Date(a.created_at)
    //     } else if (this.sortBy === 'status') {
    //       return a.status - b.status
    //     } else if (this.sortBy === 'title') {
    //       return a.title.localeCompare(b.title)
    //     }
    //     return 0
    //   })
    // }
  },
  async mounted() {
    await this.loadTasks()
  },
  methods: {
    async loadTasks() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://localhost:8000/tasks', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.tasks = response.data
      } catch (error) {
        this.error = 'Ошибка загрузки задач'
        console.error('Load tasks error:', error)
      }
    },
    
    async addTask() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.post('http://localhost:8000/tasks', this.newTask, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.tasks.push(response.data)
        this.newTask = { title: '', description: '' }
      } catch (error) {
        this.error = 'Ошибка добавления задачи'
        console.error('Add task error:', error)
      }
    },
    
    async toggleTask(task) {
      try {
        const token = localStorage.getItem('token')
        await axios.put(`http://localhost:8000/tasks/${task.id}`, {
          status: !task.status,
          title: task.title,
          description: task.description
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        task.status = !task.status
      } catch (error) {
        this.error = 'Ошибка обновления задачи'
        console.error('Toggle task error:', error)
      }
    },
    
    editTask(task) {
      this.editingTask = { ...task }
    },
    
    async saveTask() {
      try {
        const token = localStorage.getItem('token')
        await axios.put(`http://localhost:8000/tasks/${this.editingTask.id}`, this.editingTask, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        const index = this.tasks.findIndex(t => t.id === this.editingTask.id)
        if (index !== -1) {
          this.tasks[index] = { ...this.editingTask }
        }
        
        this.editingTask = null
      } catch (error) {
        this.error = 'Ошибка сохранения задачи'
        console.error('Save task error:', error)
      }
    },
    
    cancelEdit() {
      this.editingTask = null
    },
    
    async deleteTask(taskId) {
      if (!confirm('Вы уверены, что хотите удалить эту задачу?')) return
      
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`http://localhost:8000/tasks/${taskId}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.tasks = this.tasks.filter(task => task.id !== taskId)
      } catch (error) {
        this.error = 'Ошибка удаления задачи'
        console.error('Delete task error:', error)
      }
    },
    
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('ru-RU')
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters {
  margin: 20px 0;
  display: flex;
  gap: 20px;
  align-items: center;
}

.form-control {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.task-item {
  background: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.task-item.completed {
  opacity: 0.7;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.task-actions {
  display: flex;
  gap: 10px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  min-width: 400px;
}
</style>
