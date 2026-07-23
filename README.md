# 三角洲每日数据

数据来源：[kkrb.net](https://www.kkrb.net/) 三角洲行动一图流，每天 00:20 自动抓取。访问 GitHub Pages 在线查看。

## 数据内容

- 每日密码（大坝/长弓/巴克/航天/AZ3/监狱）
- 制造推荐
- 兑换推荐
- 指定子弹昨日最高/最低价（.357 Magnum FMJ/JHP、玻纤柳叶箭矢、9x39mm SP5、12 Gauge独头 AP-20）

## 自动化流程

1. **GitHub Actions** 每天北京时间 00:20 运行脚本 `fetch_data.py`
2. 脚本从 kkrb.net 抓取数据，写入 `data.json`
3. GitHub Pages 自动部署最新页面
4. 手机或电脑访问 GitHub Pages URL 即可查看

## 手动触发

进入 GitHub 仓库的 Actions 页面，找到 Daily Data Fetch workflow，点击 Run workflow 即可手动运行。

## 文件说明

| 文件 | 说明 |
|------|------|
| `delta_daily.py` | 核心抓取脚本（kkrb.net API） |
| `fetch_data.py` | 云端入口脚本，运行后输出 data.json |
| `index.html` | 手机端网页（暗色主题 + 一键复制） |
| `.github/workflows/daily.yml` | GitHub Actions 定时任务 |
| `data.json` | 每日数据（自动更新） |

_Last deployment check: 2026-07-24_
