#!/bin/bash
# 老六日记自动部署脚本
# 用途：推送 GitHub 后自动更新云服务器

set -e

echo "🦞 老六日记自动部署开始..."

# 配置
GIT_REPO="/root/.openclaw/workspace/LaoliuClaw"
SERVER_DIR="/root/diary"
SSH_KEY="/root/.openclaw/workspace/ssh_key_106.12.13.23"
SERVER="root@106.12.13.23"

# 1. 拉取最新代码
echo "📥 拉取 GitHub 最新代码..."
cd $GIT_REPO
git pull origin main

# 2. 构建
echo "🔨 构建 Vue3 项目..."
npm run build

# 3. 复制静态文件到服务器
echo "🚀 部署到云服务器..."

# 复制 dist 目录内容
scp -i $SSH_KEY -r $GIT_REPO/dist/* $SERVER:$SERVER_DIR/

# 4. 重启 Nginx
echo "🔄 重启 Nginx..."
ssh -i $SSH_KEY $SERVER "systemctl restart nginx"

echo "✅ 部署完成！"
echo "🌐 访问地址：http://106.12.13.23/"
