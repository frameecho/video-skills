# 添加一个视频 Skill

每个技能放在 `skills/<lowercase-hyphen-name>/`，必须包含带 `name`、`description` YAML 头的 `SKILL.md`。名称与文件夹一致。只增加确有用途的 `references/`、`scripts/`、`assets/`；不要建立空的未来类别。

入口说明触发场景和关键决策；长提示词、格式约定放进 references，并从入口链接。脚本给出依赖、参数和实际运行示例。UI 元数据可放在 agents/openai.yaml。新增技能时更新 README 目录。

不要提交歌曲、完整歌词、用户参考视频、生成成片、账户信息、令牌、绝对私人路径和运行日志。引用第三方实现时保留许可证和署名。

验证：

```bash
python3 scripts/check_repository.py
python3 tests/smoke.py
```

集成测试需要 `ffmpeg`、`ffprobe` 在 PATH，Node.js 18+、`npm install playwright` 和 `npx playwright install chromium`。可用 `PLAYWRIGHT_MODULE` 指定 Playwright 模块路径，`BROWSER_EXECUTABLE` 指定已有 Chrome。Python 仅标准库。测试在系统临时目录生成两秒的纯色几何动画和合成音，不使用任何歌曲。
