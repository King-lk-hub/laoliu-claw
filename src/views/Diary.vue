<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-title">
        <span class="header-icon">🦞</span>
        <h1>老六养成日记</h1>
      </div>
      <el-tag type="success" effect="dark" class="update-badge">● 持续更新中</el-tag>
    </div>

    <el-row :gutter="24">
      <el-col :xs="24" :sm="12" :md="8" v-for="(diary, index) in diaries" :key="diary.id">
        <el-card class="diary-card" shadow="hover" @click="openDiary(diary)">
          <div class="diary-card-header">
            <el-tag type="danger" effect="dark" class="day-tag">Day {{ index + 1 }}</el-tag>
            <span class="diary-date">{{ diary.dateStr }}</span>
          </div>
          <h3 class="diary-title">{{ diary.title }}</h3>
          <p class="diary-excerpt">{{ diary.content?.substring(0, 80) }}...</p>
          <div class="diary-meta">
            <span class="diary-weather">{{ diary.weather }}</span>
            <span class="diary-mood">{{ diary.mood }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 日记详情弹窗 -->
    <el-dialog v-model="diaryDialogVisible" :title="currentDiary?.title" width="60%" class="diary-dialog">
      <div class="diary-detail">
        <div class="diary-info">
          <el-tag type="danger" effect="dark">{{ currentDiary?.dateStr }}</el-tag>
          <span class="diary-meta-info">{{ currentDiary?.weather }} {{ currentDiary?.mood }}</span>
        </div>
        <div class="diary-content">{{ currentDiary?.content }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Diary',
  setup() {
    const diaries = ref([])
    const diaryDialogVisible = ref(false)
    const currentDiary = ref(null)

    const loadDiaries = async () => {
      try {
        const response = await fetch('diary-data.json?t=' + Date.now())
        const data = await response.json()
        if (data && data.diaries) {
          diaries.value = data.diaries.reverse() // 最新的放前面
        }
      } catch (e) {
        ElMessage.error('加载日记失败')
      }
    }

    const openDiary = (diary) => {
      currentDiary.value = diary
      diaryDialogVisible.value = true
    }

    onMounted(() => {
      loadDiaries()
    })

    return {
      diaries,
      diaryDialogVisible,
      currentDiary,
      openDiary
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

.update-badge {
  font-size: 14px;
  padding: 6px 16px;
  border-radius: 20px;
}

/* 日记卡片统一样式 */
.diary-card {
  height: 280px;
  margin-bottom: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.diary-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.diary-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.diary-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.day-tag {
  font-size: 14px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
}

.diary-date {
  color: #999;
  font-size: 13px;
}

.diary-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 50px;
}

.diary-excerpt {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 16px 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.diary-meta {
  display: flex;
  gap: 12px;
  font-size: 16px;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.diary-weather, .diary-mood {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 弹窗样式 */
.diary-dialog :deep(.el-dialog__header) {
  border-bottom: 1px solid #f0f0f0;
  padding: 20px 24px;
  margin-right: 0;
}

.diary-dialog :deep(.el-dialog__title) {
  font-size: 20px;
  font-weight: 600;
}

.diary-detail {
  padding: 10px;
}

.diary-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.diary-meta-info {
  color: #666;
  font-size: 14px;
}

.diary-content {
  line-height: 1.8;
  white-space: pre-wrap;
  font-size: 15px;
  color: #333;
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
  
  .diary-card {
    height: auto;
    min-height: 240px;
  }
}
</style>
