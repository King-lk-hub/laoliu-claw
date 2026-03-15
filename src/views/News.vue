<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-title">
        <span class="header-icon">📰</span>
        <h1>每日快讯</h1>
      </div>
      <el-tag type="info" effect="plain" class="update-time">更新时间：{{ newsUpdateTime }}</el-tag>
    </div>

    <!-- 分类筛选 -->
    <div class="category-filter">
      <button 
        v-for="cat in categories" 
        :key="cat.value"
        class="category-btn"
        :class="{ active: newsCategory === cat.value, [cat.value]: true }"
        @click="newsCategory = cat.value"
      >
        <span class="category-icon">{{ cat.icon }}</span>
        <span class="category-name">{{ cat.label }}</span>
      </button>
    </div>

    <div class="news-stats">
      <span>共 <strong>{{ filteredNews.length }}</strong> 条新闻</span>
    </div>

    <!-- 使用CSS Grid确保卡片宽度一致 -->
    <div class="news-grid">
      <el-card 
        v-for="newsItem in filteredNews" 
        :key="newsItem.id" 
        class="news-card" 
        :class="newsItem.category" 
        shadow="hover" 
        @click="openNews(newsItem)"
      >
        <!-- 图片显示 -->
        <div v-if="newsItem.image" class="news-image">
          <img :src="newsItem.image" :alt="newsItem.title" />
        </div>
        <div class="news-card-header">
          <el-tag :type="getCategoryType(newsItem.category)" effect="dark" size="small" class="category-tag">
            {{ newsItem.categoryName }}
          </el-tag>
          <span class="news-time">{{ newsItem.time }}</span>
        </div>
        <h3 class="news-title">{{ newsItem.title }}</h3>
        <p class="news-summary">{{ newsItem.summary }}</p>
        <div class="news-source">
          <span>📰 {{ newsItem.source }}</span>
        </div>
      </el-card>
    </div>

    <!-- 快讯详情弹窗 -->
    <el-dialog v-model="newsDialogVisible" :title="currentNews?.title" width="60%" class="news-dialog" top="5vh">
      <div class="news-detail">
        <div class="news-info">
          <el-tag :type="getCategoryType(currentNews?.category)" effect="dark">{{ currentNews?.categoryName }}</el-tag>
          <span class="news-meta-time">{{ currentNews?.time }}</span>
          <span class="news-meta-source">{{ currentNews?.source }}</span>
        </div>
        <div class="news-content" v-html="currentNews?.content"></div>
      </div>
      <template #footer>
        <el-button @click="newsDialogVisible = false" type="primary">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'News',
  setup() {
    const newsCategory = ref('all')
    const newsUpdateTime = ref('--')
    const news = ref([])
    const newsDialogVisible = ref(false)
    const currentNews = ref(null)

    const categories = [
      { value: 'all', label: '全部', icon: '📋' },
      { value: 'ai', label: 'AI', icon: '🤖' },
      { value: 'military', label: '军事', icon: '🎖️' },
      { value: 'tech', label: '科技', icon: '💻' },
      { value: 'international', label: '国际', icon: '🌍' },
      { value: 'life', label: '生活', icon: '🏠' }
    ]

    const categoryMap = {
      ai: 'purple',
      military: 'warning',
      tech: 'primary',
      life: 'success',
      international: 'info'
    }

    const getCategoryType = (category) => {
      return categoryMap[category] || ''
    }

    const filteredNews = computed(() => {
      if (newsCategory.value === 'all') return news.value
      return news.value.filter(n => n.category === newsCategory.value)
    })

    const loadNews = async () => {
      try {
        const response = await fetch('news-data.json?t=' + Date.now())
        const data = await response.json()
        if (data && data.news) {
          news.value = data.news
          newsUpdateTime.value = data.updateTime || '--'
        }
      } catch (e) {
        ElMessage.error('加载快讯失败')
      }
    }

    const openNews = (newsItem) => {
      currentNews.value = newsItem
      newsDialogVisible.value = true
    }

    onMounted(() => {
      loadNews()
    })

    return {
      newsCategory,
      categories,
      filteredNews,
      newsUpdateTime,
      newsDialogVisible,
      currentNews,
      getCategoryType,
      openNews
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 统一页面头部样式 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 32px;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
  color: var(--text-primary);
  font-weight: 700;
}

.update-time {
  font-size: 13px;
  padding: 6px 14px;
  border-radius: 16px;
}

/* 分类按钮统一样式 */
.category-filter {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.category-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 2px solid #e0e0e0;
  background: #fff;
  border-radius: 24px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  transition: all 0.3s ease;
}

.category-btn:hover {
  border-color: #ccc;
  background: #f9f9f9;
  transform: translateY(-2px);
}

.category-btn.active {
  color: #fff;
  border-color: transparent;
}

.category-btn.active.all {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.category-btn.active.ai {
  background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
}

.category-btn.active.military {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
}

.category-btn.active.tech {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
}

.category-btn.active.international {
  background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);
}

.category-btn.active.life {
  background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
}

.category-icon {
  font-size: 16px;
}

.category-name {
  font-weight: 600;
}

/* 统计信息 */
.news-stats {
  margin-bottom: 20px;
  color: #888;
  font-size: 14px;
}

.news-stats strong {
  color: var(--primary-color);
  font-size: 18px;
}

/* 新闻卡片网格布局 - 统一宽度，开片更大 */
.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 28px;
}

/* 新闻卡片统一样式 - 开片更大 */
.news-card {
  height: auto;
  min-height: 300px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border-left: 4px solid transparent;
}

.news-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.news-card.ai { border-left-color: #9b59b6; }

/* 图片样式 */
.news-image {
  width: 100%;
  height: 140px;
  overflow: hidden;
  margin: -20px -20px 12px -20px;
  background: #f5f5f5;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.news-card:hover .news-image img {
  transform: scale(1.05);
}
.news-card.military { border-left-color: #f39c12; }
.news-card.tech { border-left-color: #3498db; }
.news-card.life { border-left-color: #27ae60; }

.news-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 24px;
}

.news-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.category-tag {
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 10px;
}

.news-time {
  color: #aaa;
  font-size: 12px;
}

.news-title {
  margin: 0 0 12px 0;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 48px;
}

.news-summary {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-source {
  font-size: 13px;
  color: #999;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

/* 弹窗样式 */
.news-dialog :deep(.el-dialog__header) {
  border-bottom: 1px solid #f0f0f0;
  padding: 20px 24px;
  margin-right: 0;
}

.news-dialog :deep(.el-dialog__title) {
  font-size: 20px;
  font-weight: 600;
}

.news-dialog :deep(.el-dialog__body) {
  max-height: 70vh;
  overflow-y: auto;
}

.news-detail {
  padding: 10px;
}

.news-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.news-meta-time, .news-meta-source {
  color: #888;
  font-size: 14px;
}

.news-content {
  line-height: 1.8;
  font-size: 15px;
}

.news-content :deep(p) {
  margin-bottom: 12px;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .page-header h1 {
    font-size: 24px;
  }
  
  .category-filter {
    gap: 8px;
  }
  
  .category-btn {
    padding: 8px 14px;
    font-size: 13px;
  }
  
  .news-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .news-card {
    height: auto;
    min-height: 220px;
  }
}
</style>
