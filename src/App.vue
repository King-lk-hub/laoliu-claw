<template>
  <div id="app">
    <!-- 导航栏 -->
    <el-menu
      mode="horizontal"
      :default-active="activeIndex"
      router
      class="navbar"
    >
      <div class="nav-left">
        <el-menu-item index="/" class="logo-menu">
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=laoliu" alt="老六" class="logo-avatar">
          <span class="logo-text">老六日记</span>
        </el-menu-item>
      </div>
      <div class="nav-right">
        <el-menu-item index="/diary">📔 日记</el-menu-item>
        <el-menu-item index="/news">📰 快讯</el-menu-item>
        <el-menu-item index="/english">📖 英语</el-menu-item>
        <el-menu-item index="/skills">🔧 技能</el-menu-item>
        <el-menu-item index="/tech">📝 文章</el-menu-item>
        <el-menu-item index="/workbench">💻 工作台</el-menu-item>
        <el-menu-item index="/about">🎯 关于</el-menu-item>
        <el-menu-item disabled class="current-date">{{ currentDate }}</el-menu-item>
      </div>
    </el-menu>

    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 全局页脚 -->
    <footer class="global-footer">
      <p>🦞 laoliu.ai © 2026 刘科 & 龙虾老六</p>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const route = useRoute()
    const currentDate = ref('')

    const activeIndex = computed(() => route.path)

    const initDate = () => {
      const now = new Date()
      const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
      currentDate.value = now.toLocaleDateString('zh-CN', options)
    }

    onMounted(() => {
      initDate()
    })

    return {
      currentDate,
      activeIndex
    }
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  justify-content: space-between;
  padding: 0 20px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left, .nav-right {
  display: flex;
  align-items: center;
}

.logo-menu {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid #e74c3c;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
  color: #e74c3c;
}

.current-date {
  color: #999;
  font-size: 14px;
}

.main-content {
  flex: 1;
  padding: 20px;
}

.global-footer {
  background: #fff;
  border-top: 1px solid #e8e4df;
  padding: 16px;
  text-align: center;
  color: #7f8c8d;
  font-size: 14px;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
  }

  .nav-right {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
