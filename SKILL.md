---
name: 小程序 Canvas 预览与视觉验证工作流
display_name: Canvas视觉验证
description: 为微信小程序 Canvas 项目提供本地预览+截图视觉验证工作流：启动静态预览服务（:9099，支持任意根目录/端口）、用 Selenium 对预览页执行 JS 并截图、按场景 YAML 做区域裁剪与回归对比。含 8 项 preview.html 验证清单（白屏/线条/居中/即时重绘/导出/色值/控制台/一致性）。触发词：预览 canvas/截图验证/视觉回归/验证渲染效果/小程序 canvas 验证/起预览服务。纯前端+Python 工具链，零业务依赖。
market_desc: 教备神器出品的【小程序 Canvas 验证工作流】：一行命令起本地预览服务，Selenium 自动截图 + 场景化区域裁剪，把"盲改看效果"变成可复现的视觉回归。任何微信小程序 Canvas 项目都该有的验证利器，杜绝格子歪了、字偏了才发现。
version: 1.0.0
author: 教备神器
tags: [小程序, canvas, 预览, 截图, 视觉验证, selenium]
---

# 小程序 Canvas 预览与视觉验证工作流

> 教备神器 · 工具模块。本地静态服务 + Selenium 截图，零业务依赖。

## 这是什么（给人看）

小程序 Canvas 改完样式，最怕"盲改"——肉眼看不出格子歪没歪、字偏没偏。本技能给你一套**可复现的视觉验证**：本地起一个预览服务，Selenium 自动打开预览页、执行你要的 JS（切模板/改参数）、截图，还能按场景把顶部/中部/底部裁出来做回归对比。任何微信小程序 Canvas 项目通用，告别凭感觉。

- 已附 `selftest.py`：启动服务并确认资源可访问，PASS 才算工作流可用。

## 何时使用

- "起个预览服务看看效果" / "帮我截图验证一下 Canvas"
- 改了网格/文字/颜色，想确认没歪、没偏、没糊
- 想做视觉回归（这次截图 vs 上次截图对比）

## 工作流（AI 必读）

```
1. 起服务：node preview-server.js <工具目录> [port]   # 默认 9099
2. 浏览器开 http://127.0.0.1:9099/<preview.html>        # Canvas 效果 = 小程序效果
3. 验证脚本：python verify_shot.py --url <url> --script "<JS>" --out ./shots --crop
4. 目检 / 对比 ./shots 下的 整页 + 顶/中/底 裁剪图
```

## 核心脚本签名（AI 直接调用）

```bash
# 静态预览服务（任意根目录/端口）
node references/preview-server.js [rootDir] [port]

# Selenium 截图 + 区域裁剪
python references/verify_shot.py \
  --url http://127.0.0.1:9099/your-preview.html \
  --script "ztOpenTemplate('pinyin'); ztSetMode('inst');" \
  --wait 5 --crop --out ./shots
```

## preview.html 验证清单（8 项，全部通过才算"验证通过"）

| # | 检查项 | 通过标准 |
|---|--------|---------|
| 1 | Canvas 正确渲染 | 打开 1 秒内非白屏 |
| 2 | 网格线清晰 | 放大 200% 无毛边/锯齿 |
| 3 | 文字居中 | 目测在格正中间，不偏 |
| 4 | 参数切换即时生效 | 改任一参数 <500ms 重绘 |
| 5 | 保存图片正常 | 下载 PNG 1240×1754、无变形 |
| 6 | 颜色一致 | 与设计令牌色值一致 |
| 7 | 控制台无报错 | F12 无红错（字体 404 可忽略） |
| 8 | 重复生成一致性 | 同参数连出 3 次完全一致 |

## Canvas 常见坑（自动规避）

| 坑 | 正确做法 |
|----|----------|
| 文字模糊 | `canvas.width = cssW * dpr`；`ctx.scale(dpr,dpr)`；先设 `ctx.font` |
| 文字偏移 | 手动 `ctx.textBaseline='middle'` |
| 线不直 | `lineWidth` 偶数、坐标整数 |
| 导出空白 | 绘制前先给 `canvas.width/height` 赋值 |

## 自测

```bash
python references/selftest.py   # 启动服务并确认首页/资源可访问，PASS 方可交付
```

## 引用文件

- `references/preview-server.js` — 静态预览服务（支持 rootDir/port 参数）
- `references/verify_shot.py` — Selenium 截图 + 区域裁剪（参数化）
- `references/snap1.yml` — 场景配置示例（练字字帖模板结构）
- `references/sample-preview.html` — 最小可运行预览页（自测用）
- `references/selftest.py` — Python 自测（启动服务 + 资源可访问校验）

## 注意事项

- `verify_shot.py` 需 `pip install selenium pillow`；无头 Chrome 环境。
- 与 `canvas-grid-engine` / `svg-to-canvas-replica` 配合：本技能负责"看效果"，前两者负责"画/复刻"。

## 教备神器 Canvas 工具链（组合使用）

本技能是「教备神器 · Canvas 工具链」的一环，四件组合覆盖「画 → 复刻 → 导出 → 验证」完整闭环：

- Canvas 学习纸网格引擎（画）：13 种教育网格 + 汉字居中 + 拼音标注，生成米字格/田字格字帖。
- SVG 转 Canvas 复刻引擎（复刻）：把现有纸质模板 SVG 零误差复刻成可改字、可打印的 Canvas。
- Canvas 多页 PDF 导出（导出）：多页 Canvas 一键合成标准 A4 PDF 直接打印。
- 小程序 Canvas 验证工作流（验证）：本地预览 + 截图视觉回归，杜绝格子歪、字偏。

完整方案与演示见「教备神器 Canvas 工具链落地页」（链接发布后回填）。
