import { createRouter, createWebHistory } from 'vue-router'
import Diary from '../views/Diary.vue'
import News from '../views/News.vue'
import English from '../views/English.vue'
import Tech from '../views/Tech.vue'
import Skills from '../views/Skills.vue'
import Workbench from '../views/Workbench.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', redirect: '/diary' },
  { path: '/diary', component: Diary },
  { path: '/news', component: News },
  { path: '/english', component: English },
  { path: '/tech', component: Tech },
  { path: '/skills', component: Skills },
  { path: '/workbench', component: Workbench },
  { path: '/about', component: About }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
