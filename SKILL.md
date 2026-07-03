---
name: NE引文插入skills
description: 使用 NoteExpress/NE 为 Word DOCX 正式创建或导入文献条目，并插入可更新的 NoteExpress 链接引文字段。用于用户要求“用 NE 插入引文”“NoteExpress 创建单独文件夹后插入引用”“不要纯文本编号”“插入 Word 链接引文”“生成 NE.Ref/NE.Bib 字段”“修复 NoteExpress 引文”时。
---

# NE 引文插入 Skills

## 核心原则

1. 最终稿不能只留下普通文本 `[1]`、`[1-3]`。
2. 必须生成或复用 `NoteExpress` 条目，并在 `docx` 中写入 `ADDIN NE.Ref.{GUID}` 正文字段。
3. 参考文献列表必须由 `ADDIN NE.Bib` 字段包裹，便于 `NoteExpress` 后续更新。
4. 必须为本次任务创建独立 `NE_*` 文件夹，保存导入文件、数据库备份路径、编号清单、插入记录和审计结果。
5. 修改 `NoteExpress` 数据库前必须备份 `.ndb`。
6. 不覆盖原稿；输出带时间戳或语义后缀的新 `docx`。

## 默认工作流

1. 定位目标稿件：
   - 优先使用用户给出的目录和主稿文件。
   - 若目录中有多个 `docx`，优先选择非 `backup`、非临时锁文件、命名最像主稿的文件。
2. 创建独立文件夹：
   - 与稿件同目录创建 `NE_<manuscript-stem>_<YYYYMMDD>`。
   - 至少保存 `final_reference_order_manifest.csv`、`noteexpress_db_inserted_records.csv`、`database_backup_path.txt`。
3. 准备文献条目：
   - 优先使用用户提供的正式文献池、`RIS`、`CSV` 或稿件 `References`。
   - 按正文首次出现顺序编号。
   - DOI 相同的文献必须去重并复用同一条 `NoteExpress` 记录。
4. 创建或导入 `NoteExpress` 条目：
   - 在 `NoteExpress` 软件左侧 `题录` 下先创建本稿专用题录文件夹，文件夹名应与稿件或项目对应，例如 `NE_<manuscript-stem>_<YYYYMMDD>` 或用户指定名称。
   - 将本次 `RIS`/文献条目导入到该专用题录文件夹，避免导入到根目录、示例文件夹或其他课题文件夹。
   - 优先通过 `NoteExpress` 软件导入 `RIS`。
   - 若无法使用前台软件控制，但本机 `.ndb` 可读写，可直接操作 `SQLite` 数据库；必须先备份。
   - 默认数据库位置通常为 `%USERPROFILE%\Documents\NoteExpress\Libraries\<library>.ndb`。
5. 插入 Word 链接引文：
   - 把正文引用位置替换为 `ADDIN NE.Ref.{GUID}` 字段。
   - 在 `word/settings.xml` 写入对应 `w:docVar`，名称为 `NE.Ref{GUID}`。
   - 把参考文献区包进 `ADDIN NE.Bib` 字段。
6. 校验：
   - 统计 `NE.Ref`、`NE.Bib`、`docVar NE.Ref`。
   - 确认正文引用编号与参考文献编号闭合。
   - 确认 `docx` 可重开、图片数量未丢失、压缩包 `testzip()` 通过。
   - 如环境有 `Word`/`LibreOffice`，再做渲染校验。

## NoteExpress 数据库写入要点

`.ndb` 通常是 `SQLite`：

- 主表：`reference`
- 详情表：`reference_detail`
- 数据库标识：`dbstrings.name='dbid'`

新增记录时写入：

- `reference.id`
- `reference.uid1`、`uid2`、`uid3`、`uid4`
- `template`
- `author`
- `year`
- `title`
- `reference_detail` 中的 `_doi`、`_journal`、`_volume`、`_issue`、`_pages`、`_url`、`_date_display`

`UID` 规则：

- 用 `uuid.UUID(bytes_le=struct.pack("<iiii", uid1, uid2, uid3, uid4))` 还原为 `{GUID}`。
- 新条目可用 `uuid5(DBUID, DOI-or-title)` 生成稳定 `UID`，再拆成 4 个 signed int。

## Word 字段结构

正文引文必须是 Word 字段：

```text
begin fldChar
instrText:  ADDIN NE.Ref.{FIELD_GUID}
separate fldChar
visible text: [1] / [1-3]
end fldChar
```

同时在 `word/settings.xml` 的 `w:docVars` 中加入：

```xml
<w:docVar w:name="NE.Ref{FIELD_GUID}" w:val=" ADDIN NE.Ref.{FIELD_GUID}<Citation>...</Citation>_x000a_"/>
<w:docVar w:name="ne_docsoft" w:val="MSWord"/>
<w:docVar w:name="ne_docversion" w:val="NoteExpress 2.0"/>
<w:docVar w:name="ne_stylename" w:val="Vancouver"/>
```

参考文献区必须包含：

```text
ADDIN NE.Bib
```

详细字段模型见 `references/noteexpress-ooxml.md`。完成后可运行 `scripts/audit_ne_docx.py` 审计。

## 禁止事项

- 禁止把最终引用仅做成普通文本编号。
- 禁止未备份 `.ndb` 就写入数据库。
- 禁止覆盖用户原稿。
- 禁止删除或重建图片、表格、章节结构，除非用户明确要求。
- 禁止把未核验、无法定位来源的文献伪装成已导入 `NoteExpress` 条目。
