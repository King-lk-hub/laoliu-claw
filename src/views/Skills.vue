<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-title">
        <span class="header-icon">🔧</span>
        <h1>全部技能</h1>
      </div>
      <el-tag type="warning" effect="dark">持续更新中</el-tag>
    </div>

    <!-- 技能分类 -->
    <div class="category-filter">
      <button 
        v-for="cat in categories" 
        :key="cat.value"
        class="category-btn"
        :class="{ active: activeCategory === cat.value }"
        @click="activeCategory = cat.value"
      >
        <span class="category-name">{{ cat.label }}</span>
      </button>
    </div>

    <!-- 技能卡片网格 -->
    <div class="skills-grid">
      <el-card 
        v-for="skill in filteredSkills" 
        :key="skill.id" 
        class="skill-card" 
        shadow="hover"
      >
        <div class="skill-header">
          <div class="skill-icon">{{ skill.icon }}</div>
          <div class="skill-info">
            <h3 class="skill-name">{{ skill.name }}</h3>
            <div class="skill-tags">
              <el-tag 
                v-for="tag in skill.tags" 
                :key="tag" 
                size="small" 
                :type="getTagType(tag)"
                effect="plain"
              >{{ tag }}</el-tag>
            </div>
          </div>
        </div>
        <p class="skill-desc">{{ skill.description }}</p>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Skills',
  setup() {
    const activeCategory = ref('all')

    const categories = [
      { value: 'all', label: '全部' },
      { value: 'info', label: '信息获取' },
      { value: 'content', label: '内容创作' },
      { value: 'tech', label: '技术能力' },
      { value: 'social', label: '社媒运营' },
      { value: 'office', label: '办公效率' }
    ]

    const skills = [
      {
        id: 1,
        name: '网页搜索与分析',
        icon: '🔍',
        description: '实时网络信息搜索，支持多搜索引擎，获取最新资讯和数据。',
        category: 'info',
        tags: ['官方', '必装']
      },
      {
        id: 2,
        name: '今日热榜',
        icon: '🔥',
        description: '一键获取微博、知乎、抖音、百度等全网热点榜单。',
        category: 'info',
        tags: ['官方', '热门']
      },
      {
        id: 3,
        name: '深度研究',
        icon: '🔬',
        description: '多引擎搜索 + 网页提取，生成结构化分析报告。',
        category: 'info',
        tags: ['官方']
      },
      {
        id: 4,
        name: '快讯推送',
        icon: '📰',
        description: '每日自动获取AI、军事、科技等热门资讯，推送给用户。',
        category: 'info',
        tags: ['已实现']
      },
      {
        id: 5,
        name: 'AI 文本人性化',
        icon: '🧑',
        description: '去除AI味，支持小红书、知乎、学术等多种风格转换。',
        category: 'content',
        tags: ['官方', '必装']
      },
      {
        id: 6,
        name: '博客写手',
        icon: '✍️',
        description: '长文写作 + 排版 + 发布，支持多平台格式适配。',
        category: 'content',
        tags: ['官方']
      },
      {
        id: 7,
        name: 'SEO 内容写作',
        icon: '📈',
        description: 'SEO优化的长文写作，关键词策略 + 结构化内容。',
        category: 'content',
        tags: ['官方', '必装']
      },
      {
        id: 8,
        name: '代码助手',
        icon: '💻',
        description: '写代码、改Bug、部署，PTY模式自动应答。',
        category: 'tech',
        tags: ['官方']
      },
      {
        id: 9,
        name: 'GitHub 操作',
        icon: '🐙',
        description: '仓库/Issues/PR/代码搜索/Actions，不开网页管GitHub。',
        category: 'tech',
        tags: ['官方']
      },
      {
        id: 10,
        name: '浏览器控制',
        icon: '🔭',
        description: '无头Chrome截图、网页自动化、视觉调试。',
        category: 'tech',
        tags: ['官方', '必装']
      },
      {
        id: 11,
        name: '英语学习助手',
        icon: '📖',
        description: '每日单词背诵、艾宾浩斯遗忘曲线复习、词汇测试。',
        category: 'content',
        tags: ['已实现']
      },
      {
        id: 12,
        name: '日记系统',
        icon: '📔',
        description: '每天自动生成日记，记录工作与生活，支持图片展示。',
        category: 'content',
        tags: ['已实现']
      }
    ]

    const filteredSkills = computed(() => {
      if (activeCategory.value === 'all') return skills
      return skills.filter(s => s.category === activeCategory.value)
    })

    const getTagType = (tag) => {
      if (tag === '必装' || tag === '热门') return 'danger'
      if (tag === '官方') return 'primary'
      if (tag === '已实现') return 'success'
      return 'info'
    }

    return {
      activeCategory,
      categories,
      skills,
      filteredSkills,
      getTagType
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

/* 分类按钮样式 - 三万风格 */
.category-filter {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.category-btn {
  padding: 10px 24px;
  border: 1px solid #e0e0e0;
  background: #fff;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  transition: all 0.3s ease;
}

.category-btn:hover {
  border-color: #c0c0c0;
  background: #fafafa;
}

.category-btn.active {
  background: #c0392b;
  color: #fff;
  border-color: #c0392b;
}

/* 技能卡片网格布局 */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
}

/* 技能卡片统一样式 - 三万风格 */
.skill-card {
  cursor: default;
  transition: all 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.skill-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border-color: #e0e0e0;
}

.skill-card :deep(.el-card__body) {
  padding: 20px;
}

.skill-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.skill-icon {
  font-size: 32px;
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.skill-info {
  flex: 1;
}

.skill-name {
  margin: 0 0 8px 0;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.skill-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.skill-tags :deep(.el-tag) {
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 12px;
}

.skill-desc {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  padding-left: 52px;
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
    padding: 8px 16px;
    font-size: 13px;
  }
  
  .skills-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .skill-desc {
    padding-left: 0;
    margin-top: 8px;
  }
}
</style>
