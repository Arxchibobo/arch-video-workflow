# 📖 使用教程 — 建筑方案汇报视频工作流

## 环境准备（Windows）

```cmd
git clone https://github.com/Arxchibobo/arch-video-workflow.git
cd arch-video-workflow
pip install -r requirements.txt
```

注意：需要安装 [ImageMagick](https://imagemagick.org/script/download.php)（moviepy 文字渲染依赖）。

## 快速开始

### Step 1: 编写项目脚本（Markdown 格式）

创建 `my_project.md`：

```markdown
# 绿色生态住宅项目

## 项目愿景
打造低碳、节能、宜居的未来社区
[image: modern eco-friendly residential building with green rooftop garden]

## 场地分析
地块面积 12000㎡，南向采光良好，北侧紧邻城市公园
[image: site analysis aerial view with sun path diagram]

## 设计理念
被动式节能 + 垂直绿化 + 雨水回收
[image: architectural concept diagram showing passive cooling system]

## 平面布局
三栋 18 层住宅围合中央花园，底层商业裙房
[image: architectural floor plan with landscaping]

## 效果展示
落地窗最大化自然采光，阳台种植箱一体化设计
[image: photorealistic rendering of modern apartment interior]
```

### Step 2: 生成视频

**占位模式**（无需 API Key，纯色背景+文字）：
```cmd
python -m arch_video --script my_project.md --output presentation.mp4
```

**AI 图片模式**（需要 OpenAI Key，生成效果图）：
```cmd
set OPENAI_API_KEY=sk-你的key
python -m arch_video --script my_project.md --output presentation.mp4 --dalle
```

**加背景音乐**：
```cmd
python -m arch_video --script my_project.md --output presentation.mp4 --music bgm.mp3
```

### Step 3: 播放视频

打开 `presentation.mp4`，每个章节自动生成标题卡+内容画面，带渐变转场。

## 参数调整

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--resolution` | 1920x1080 | 视频分辨率 |
| `--duration` | 5 | 每段时长（秒） |
| `--music` | 无 | 背景音乐路径 |
| `--dalle` | 关 | 是否用 DALL-E 生图 |

## 适用场景

- 建筑方案投标汇报视频
- 室内设计展示
- 项目进度总结
- 城市规划方案演示
