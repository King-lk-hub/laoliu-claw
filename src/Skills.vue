<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-title">
        <span class="header-icon">🔧</span>
        <h1>老六技能商店</h1>
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
        <span class="category-icon">{{ cat.icon }}</span>
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
        <div class="skill-icon">{{ skill.icon }}</div>
        <h3 class="skill-name">{{ skill.name }}</h3>
        <p class="skill-desc">{{ skill.description }}</p>
        <div class="skill-tags">
          <el-tag 
            v-for="tag in skill.tags" 
            :key="tag" 
            size="small" 
            :type="getTagType(tag)"
          >{{ tag }}</el-tag>
        </div>
        <div class="skill-scenes" v-if="skill.scenes && skill.scenes.length">
          <h4>使用场景：</h4>
          <ul>
            <li v-for="scene in skill.scenes" :key="scene">{{ scene }}</li>
          </ul>
        </div>
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
      { value: 'all', label: '全部技能', icon: '📋' },
      { value: 'info', label: '信息获取', icon: '🌐' },
      { value: 'content', label: '内容创作', icon: '📝' },
      { value: 'tech', label: '技术能力', icon: '💻' }
    ]

    const skills = [
      {
        id: 1,
        name: '网页搜索与分析',
        icon: '🔍',
        description: '实时网络信息搜索，支持多搜索引擎，获取最新资讯和数据。',
        category: 'info',
        tags: ['官方', '必装'],
        scenes: [
          '新闻监控 - 实时追踪行业新闻',
          '事实核查 - 验证信息找原始来源',
          '信息采集 - 批量获取整理数据'
        ]
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
        tags: ['官方', '已实现']
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

/* 分类按钮样式 */
.category-filter {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
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
  border-color: #f39c12;
  background: #fffbf0;
  transform: translateY(-2px);
}

.category-btn.active {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  color: #fff;
  border-color: transparent;
}

.category-icon {
  font-size: 16px;
}

.category-name {
  font-weight: 600;
}

/* 技能卡片网格布局 - 统一宽度 */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

/* 技能卡片统一样式 */
.skill-card {
  cursor: default;
  transition: all 0.3s ease;
  border-radius: 16px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.skill-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.skill-card :deep(.el-card__body) {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.skill-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.skill-name {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.skill-desc {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  flex: 1;
}

.skill-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.skill-scenes {
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.skill-scenes h4 {
  margin: 0 0 12px 0;
  font-size: 13px;
  color: #888;
  font-weight: 500;
}

.skill-scenes ul {
  margin: 0;
  padding-left: 20px;
}

.skill-scenes li {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.5;
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
  
  .skills-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>
