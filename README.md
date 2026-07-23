# 三角洲行动每日数据

每天自动抓取 [kkrb.net](https://www.kkrb.net) 的三角洲行动游戏数据，通过 GitHub Pages 展示。

## 数据内容

- 今日密码（大坝/长弓/巴克/航天/AZ3/监狱/彩六联动房）
- 制造推荐（技术中心/工作台/制药台/防具台 各取利润最高）
- 兑换推荐（收益前3）
- 指定子弹昨日最高/最低价

## 运行机制

1. **GitHub Actions** 每天北京时间 00:20 自动运行 `fetch_data.py`
2. 脚本从 kkrb.net 抓取数据，生成 `data.json`
3. 自动提交到仓库，GitHub Pages 随即更新
4. 手机访问 GitHub Pages URL 即可查看，支持一键复制

## 手动触发

在 GitHub 仓库的 Actions 页面，选择 "Daily Data Fetch" workflow，点击 "Run workflow" 即可手动触发。

## 文件说明

| 文件 | 用途 |
|------|------|
| `delta_daily.py` | 核心抓取脚本（kkrb.net API 客户端） |
| `fetch_data.py` | 云端入口，调用核心脚本并输出 data.json |
| `index.html` | 手机端网页（暗色主题 + 一键复制） |
| `.github/workflows/daily.yml` | GitHub Actions 定时任务 |
| `data.json` | 最新数据（自动更新） |
