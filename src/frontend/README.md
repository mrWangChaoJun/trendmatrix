# TrendMatrix Frontend

前端数据可视化与用户界面开发

## 技术栈

- Vue 3
- TypeScript
- Vite
- Pinia (状态管理)
- Vue Router
- D3.js (数据可视化)
- Tailwind CSS (样式)
- Axios (API 调用)

## 项目结构

```
src/
├── assets/            # 静态资源
├── components/        # 组件
│   ├── common/        # 通用组件
│   ├── charts/        # 图表组件
│   └── layout/        # 布局组件
├── composables/       # 组合式 API
├── config/            # 配置文件
├── views/             # 页面视图
│   ├── dashboard/     # 仪表盘
│   ├── signals/       # 信号系统
│   ├── solana/        # Solana 生态分析
│   ├── settings/      # 设置
│   └── auth/          # 认证
├── services/          # API 服务
├── stores/            # 状态管理
├── utils/             # 工具函数
├── router/            # 路由配置
├── styles/            # 全局样式
├── App.vue            # 根组件
└── main.ts            # 入口文件
```

## 开发命令

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 代码检查
npm run lint

# 类型检查
npm run type-check
```

## 主要功能

1. **仪表盘**：数据概览、趋势图表、关键指标
2. **信号系统**：信号列表、详情、历史记录、设置
3. **Solana 生态分析**：项目活跃度、开发者活动、NFT 市场、DeFi 协议
4. **用户认证**：登录、注册、权限管理
5. **系统设置**：用户配置、通知设置、API 管理

## 数据可视化

- 折线图：价格走势、交易量
- 柱状图：项目活跃度、开发者活动
- 饼图：市场份额、资产分布
- 热力图：相关性分析
- 雷达图：多维度指标分析
- 散点图：数据分布分析

## API 集成

前端通过 Axios 调用后端 API，主要包括：

- 信号系统 API
- Solana 生态分析 API
- 用户管理 API
- 数据查询 API

## 响应式设计

- 桌面端：完整功能布局
- 平板端：适配布局
- 移动端：简化布局，核心功能优先

## 性能优化

- 组件懒加载
- 图片优化
- 缓存策略
- 代码分割
- 虚拟列表

## 安全措施

- 身份认证
- 权限控制
- API 调用验证
- 数据加密
- 防 XSS 攻击
