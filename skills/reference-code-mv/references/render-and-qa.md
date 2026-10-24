# 渲染与验收

依赖：Python 3.9+ 标准库、FFmpeg/ffprobe、Node.js 18+、Playwright。在工作目录安装 `npm install playwright`，并使用 `npx playwright install chromium` 安装浏览器，或设置 `BROWSER_EXECUTABLE` 指向已有 Chrome。`PLAYWRIGHT_MODULE` 可指定模块路径；默认从渲染脚本及当前目录解析。

```bash
python3 scripts/inspect_media.py reference.mp4 --out work/reference --count 12
node scripts/render_canvas.cjs assets/scene.html work/demo.mp4 2 30
python3 scripts/validate_video.py work/demo.mp4 --duration 2 --fps 30
```

以上命令在 Skill 目录运行。渲染器使用页面 `window.renderFrame(t)`，`window.VIDEO_WIDTH`、`window.VIDEO_HEIGHT`，等待 `document.fonts.ready` 和可选 `window.ready` Promise。模板默认 640×360。先复制到项目中改造，勿将最小模板冒充成片。

带音轨：`node scripts/render_canvas.cjs project/index.html work/final.mp4 217.75 30 song.mp3`。时长应从实际音频测得，不照抄示例。输出不覆盖已有文件。渲染失败可能保留部分文件，应另取名称重试；只有退出码 0 且 manifest 完整才算完成。

帧数使用 `ceil(duration*fps)`，最后帧时间 `(N-1)/fps`。输出应覆盖音频尾部，误差控制在一个帧间隔加编码容差内。渲染器不支持断点续跑或分段拼接，避免旧帧混用。另行实现并行时，每段用整数帧区间 `[start,end)`，检查零帧缝隙、零重叠、最后一段覆盖和源码/素材指纹一致后拼接。

逐帧 PNG 输入经 FFmpeg 编码为 H.264 yuv420p、有限色域、AAC；不自动调节响度。若另用 JPEG 输入，要显式处理 full-range 到 limited-range，不能只改像素格式标签。不要为省时重复压缩已经合格的成片。

validate_video 默认要求音频，静音样片用 `--silent`。黑场允许量默认 0；明确设计了片尾淡出时使用 `--allow-tail-black 0.4` 等实际容差。工具检查全片解码、真实解码帧数、格式、音频、时长与黑场；不能证明叙事、美感、歌词同步或听感。

人工验收需检查参考对照、字幕安全区和错字、高潮视觉变化、转场连续、片尾完整、音画同步及音量。必要时用 ebur128 测量源音轨与输出响度，避免把转码导致的响度变化误当作创作选择。不要把“未发现异常”夸大为未执行的验证。
