# NE 引文插入 Skill

一个用于 `Codex` 的 `NoteExpress` 引文插入技能。它的目标不是生成普通文本编号，而是在 `Word DOCX` 中写入可由 `NoteExpress` 更新的 `NE.Ref` / `NE.Bib` 字段，并提供基础审计脚本。

## 功能

- 创建或复用 `NoteExpress` 文献条目。
- 在 `DOCX` 正文中写入 `ADDIN NE.Ref.{GUID}` 字段。
- 在参考文献区写入 `ADDIN NE.Bib` 字段。
- 在 `word/settings.xml` 中维护对应的 `NE.Ref{GUID}` 文档变量。
- 提供 `scripts/audit_ne_docx.py` 检查 `NE.Ref`、`NE.Bib`、`docVar` 和压缩包完整性。

## 目录

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── noteexpress-ooxml.md
└── scripts/
    └── audit_ne_docx.py
```

## 使用

将本仓库复制到本地 `Codex` 技能目录，例如：

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\NE引文插入skills"
```

在需要处理稿件时调用：

```text
Use $NE引文插入skills to create NoteExpress records, insert NE.Ref/NE.Bib fields into a Word manuscript, and audit citation closure.
```

## 审计脚本

```bash
python scripts/audit_ne_docx.py manuscript.docx
```

脚本会检查：

- `DOCX` 压缩包完整性。
- `word/document.xml` 中的 `ADDIN NE.Ref.`。
- `word/document.xml` 中的 `ADDIN NE.Bib`。
- `word/settings.xml` 中对应的 `NE.Ref{GUID}` 文档变量数量。
- 媒体文件数量和 `NoteExpress` 标记数量。

## 注意

- 修改 `.ndb` 数据库前必须先备份。
- 不要把最终引文只做成普通文本 `[1]`。
- 不要覆盖原稿，输出应使用新文件名。
- 不要删除或重建稿件中的图片、表格、章节结构，除非用户明确要求。

## License

No license has been specified.
