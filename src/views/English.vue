<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-title">
        <span class="header-icon">📖</span>
        <h1>英语词汇</h1>
      </div>
      <el-tag type="success" effect="dark" class="day-badge">第 {{ currentDay }} 天</el-tag>
    </div>

    <!-- 三天切换 -->
    <div class="day-tabs">
      <button 
        v-for="tab in dayTabs" 
        :key="tab.value"
        class="day-tab"
        :class="{ active: activeTab === tab.value }"
        @click="activeTab = tab.value"
      >
        <span class="tab-label">{{ tab.label }}</span>
        <span class="tab-date">{{ tab.date }}</span>
      </button>
    </div>

    <!-- 单词列表 -->
    <el-card class="words-card" shadow="hover">
      <div class="words-header">
        <span class="words-count">共 {{ currentWords.length }} 个单词</span>
        <el-button type="primary" size="small" @click="refreshWords" :loading="loading">
          🔄 刷新单词
        </el-button>
      </div>
      <el-table 
        :data="currentWords" 
        stripe 
        style="width: 100%"
        class="words-table"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600' }"
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="word" label="单词" width="150">
          <template #default="scope">
            <span class="word-text">{{ scope.row.word }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="phonetic" label="音标" width="180">
          <template #default="scope">
            <span class="phonetic-text">{{ scope.row.phonetic }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="meaning" label="释义" min-width="200">
          <template #default="scope">
            <span class="meaning-text">{{ scope.row.meaning }}</span>
          </template>
        </el-table-column>
        <el-table-column label="例句" min-width="350">
          <template #default="scope">
            <span class="example-text">{{ scope.row.example }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'English',
  setup() {
    const currentDay = ref(1)
    const activeTab = ref('today')
    const loading = ref(false)
    
    // 三天的单词数据
    const wordsData = ref({
      yesterday: [],
      today: [],
      tomorrow: []
    })

    // 计算三天日期
    const dayTabs = computed(() => {
      const today = new Date()
      const yesterday = new Date(today)
      yesterday.setDate(yesterday.getDate() - 1)
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      
      return [
        { value: 'yesterday', label: '昨天', date: formatDate(yesterday) },
        { value: 'today', label: '今天', date: formatDate(today) },
        { value: 'tomorrow', label: '明天', date: formatDate(tomorrow) }
      ]
    })

    const formatDate = (date) => {
      return `${date.getMonth() + 1}/${date.getDate()}`
    }

    // 当前显示的单词
    const currentWords = computed(() => {
      return wordsData.value[activeTab.value] || []
    })

    // 从API获取单词（模拟）
    const fetchWords = async (day) => {
      // 这里应该是从网站爬取专升本词汇
      // 现在使用模拟数据
      const baseWords = [
        { word: 'abandon', phonetic: '/əˈbændən/', meaning: 'v. 放弃，遗弃', example: 'He abandoned his car in the snow.' },
        { word: 'ability', phonetic: '/əˈbɪləti/', meaning: 'n. 能力，才能', example: 'She has the ability to speak four languages.' },
        { word: 'abroad', phonetic: '/əˈbrɔːd/', meaning: 'adv. 在国外，到国外', example: 'He studied abroad for three years.' },
        { word: 'absence', phonetic: '/ˈæbsəns/', meaning: 'n. 缺席，缺乏', example: 'His absence from school was noticed.' },
        { word: 'absolute', phonetic: '/ˈæbsəluːt/', meaning: 'adj. 绝对的，完全的', example: 'I have absolute confidence in you.' },
        { word: 'absorb', phonetic: '/əbˈsɔːb/', meaning: 'v. 吸收，吸引', example: 'Plants absorb water from the soil.' },
        { word: 'abstract', phonetic: '/ˈæbstrækt/', meaning: 'adj. 抽象的 n. 摘要', example: 'This is an abstract concept.' },
        { word: 'abundant', phonetic: '/əˈbʌndənt/', meaning: 'adj. 丰富的，充裕的', example: 'The region has abundant natural resources.' },
        { word: 'academic', phonetic: '/ˌækəˈdemɪk/', meaning: 'adj. 学术的，学院的', example: 'She has an academic background.' },
        { word: 'accelerate', phonetic: '/əkˈseləreɪt/', meaning: 'v. 加速，促进', example: 'The car began to accelerate.' }
      ]
      
      // 生成50个单词（实际应该从网站爬取）
      const words = []
      for (let i = 0; i < 50; i++) {
        const base = baseWords[i % baseWords.length]
        words.push({
          ...base,
          word: base.word + (i > 9 ? i : ''),
          id: i + 1
        })
      }
      
      return words
    }

    const loadWords = async () => {
      try {
        // 尝试从本地文件加载
        const response = await fetch('english-words-data.json?t=' + Date.now())
        const data = await response.json()
        if (data) {
          currentDay.value = data.day || 1
          // 将单词分配到三天
          const allWords = data.words || []
          wordsData.value.yesterday = allWords.slice(0, 50)
          wordsData.value.today = allWords.slice(50, 100)
          wordsData.value.tomorrow = allWords.slice(100, 150)
        }
      } catch (e) {
        // 如果加载失败，使用模拟数据
        wordsData.value.yesterday = await fetchWords('yesterday')
        wordsData.value.today = await fetchWords('today')
        wordsData.value.tomorrow = await fetchWords('tomorrow')
      }
    }

    const refreshWords = async () => {
      loading.value = true
      try {
        // 模拟从网站爬取50个单词
        const newWords = await fetchWords('today')
        wordsData.value[activeTab.value] = newWords
        ElMessage.success('单词已更新！')
      } catch (e) {
        ElMessage.error('更新失败')
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadWords()
    })

    return {
      currentDay,
      activeTab,
      dayTabs,
      currentWords,
      loading,
      refreshWords
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
  margin-bottom: 24px;
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

.day-badge {
  font-size: 14px;
  padding: 6px 16px;
  border-radius: 20px;
}

/* 三天切换标签 */
.day-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.day-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 32px;
  border: 2px solid #e0e0e0;
  background: #fff;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
}

.day-tab:hover {
  border-color: #27ae60;
  background: #f0f9f4;
}

.day-tab.active {
  background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
  color: #fff;
  border-color: transparent;
}

.tab-label {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.tab-date {
  font-size: 12px;
  opacity: 0.8;
}

/* 单词卡片样式 */
.words-card {
  border-radius: 16px;
  overflow: hidden;
}

.words-card :deep(.el-card__body) {
  padding: 0;
}

.words-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.words-count {
  color: #666;
  font-size: 14px;
}

.words-table {
  font-size: 14px;
}

.words-table :deep(.el-table__cell) {
  padding: 14px 20px;
}

.word-text {
  font-weight: 700;
  color: #e74c3c;
  font-size: 16px;
}

.phonetic-text {
  color: #7f8c8d;
  font-style: italic;
  font-family: 'Times New Roman', serif;
}

.meaning-text {
  color: #2c3e50;
  font-weight: 500;
  line-height: 1.5;
}

.example-text {
  color: #666;
  font-size: 13px;
  line-height: 1.6;
  font-style: italic;
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
  
  .day-tabs {
    gap: 8px;
  }
  
  .day-tab {
    padding: 10px 20px;
    min-width: 80px;
  }
  
  .tab-label {
    font-size: 14px;
  }
  
  .words-table :deep(.el-table__cell) {
    padding: 12px;
  }
}
</style>
