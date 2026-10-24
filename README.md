# video-skills

可复用的视频制作技能库。把真实制作中有效的方法、提示词和验证工具整理成独立 Skill，供 Claude Code、Codex 等编码助手使用。

## 技能目录

| Skill | 用途 |
| --- | --- |
| [reference-code-mv](skills/reference-code-mv/SKILL.md) | 分析参考视频，让 Claude 用代码绘制整首 MV，检查画风、镜头、歌词时间和最终视频 |

第一项技能来自一次完整的代码 MV 制作实践：从参考分析到整曲渲染。支持像素桌面、剪纸、手绘等方向，**不预设所有作品都长成同一种风格**。

## 使用

```bash
git clone https://github.com/frameecho/video-skills.git
```

Claude Code：将 `skills/reference-code-mv` 文件夹复制到项目的 `.claude/skills/`。Codex：复制到 `~/.codex/skills/`。不要将仓库根目录当作一个 Skill 安装。

也可以让编码助手直接读取这个仓库内的 `skills/reference-code-mv/SKILL.md`。

示例请求：

> 使用 reference-code-mv。参考我提供的视频，用这首歌制作完整 MV。核心画面和分镜由 Claude 编码完成。请先分析参考视频的构图、材质、字体、运动和节奏，再自主决定镜头。先做代表性样片并对照参考检查，通过后继续整首，最后提供源码、成片和验证结果。

提供你有权使用的音频、可用的歌词时间文件、参考视频和目标画幅。没有逐字时间时，助手应明确说明采用句内插值，而不能称为精确逐字对齐。

## 包含什么

- 参考分析方法及可直接填写的 Claude 任务提示词。
- 确定性 Canvas 模板、逐帧渲染器、关键帧提取和视频检查工具。
- 完整度、音轨、像素格式、黑场与片尾检查。
- 独立文件夹结构，今后新增技能放进 `skills/<skill-name>/`，无需改动已有技能。

工具运行说明见 [渲染与验收](skills/reference-code-mv/references/render-and-qa.md)。开发检查：`python3 scripts/check_repository.py`；集成测试需要 FFmpeg、Node.js 和 Playwright，见 [贡献指南](CONTRIBUTING.md)。

仓库不附带商业歌曲、歌词、参考视频、私人项目和平台登录信息。发布到视频平台是另外的操作，需要用户明确要求。

## 致谢与许可

制作思路受到 [Win-Hao/music-mv](https://github.com/Win-Hao/music-mv) 启发。本仓库的说明、模板与辅助脚本独立编写，使用 [MIT License](LICENSE)。外部媒体、字体和依赖仍遵循各自许可。
