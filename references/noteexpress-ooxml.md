# NoteExpress OOXML Reference

## `NE.Ref` 文档变量

每个正文引文对应一个字段 `FIELD_GUID`，并在 `word/settings.xml` 中保存同名文档变量：

```xml
<w:docVar
  w:name="NE.Ref{FIELD_GUID}"
  w:val=" ADDIN NE.Ref.{FIELD_GUID}<Citation>...groups...</Citation>_x000a_"/>
```

`<Citation>` 内每篇文献使用一个 `<Group>`：

```xml
<Citation>
  <Group>
    <References>
      <Item>
        <ID>10001</ID>
        <UID>{REFERENCE-UID-GUID}</UID>
        <Title>Article title</Title>
        <Template>Journal Article</Template>
        <Star>0</Star>
        <Tag>0</Tag>
        <Author>Author A, Author B, et al</Author>
        <Year>2026</Year>
        <Details>
          <_doi>10.xxxx/yyyy</_doi>
          <_journal>Journal</_journal>
          <_volume>1</_volume>
          <_issue>2</_issue>
          <_pages>1-9</_pages>
          <_url>https://doi.org/10.xxxx/yyyy</_url>
          <_date_display>2026</_date_display>
        </Details>
        <Extra>
          <DBUID>{NOTEEXPRESS-DBUID}</DBUID>
        </Extra>
      </Item>
    </References>
  </Group>
</Citation>
```

## 正文 `NE.Ref` 字段

正文显示 `[1]`、`[1-3]` 等，但必须由 Word 字段承载：

```xml
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> ADDIN NE.Ref.{FIELD_GUID}</w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r><w:t>[1-3]</w:t></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
```

## 参考文献区 `NE.Bib`

把参考文献列表放在字段结果内：

```xml
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> ADDIN NE.Bib</w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
... numbered bibliography text ...
<w:r><w:fldChar w:fldCharType="end"/></w:r>
```

## 审计标准

- `word/document.xml` 中存在 `ADDIN NE.Ref.`。
- `word/document.xml` 中存在 `ADDIN NE.Bib`。
- `word/settings.xml` 中存在与正文 `NE.Ref` 数量一致的 `w:docVar w:name="NE.Ref{...}"`。
- `w:docVar` 中的每个 `<Item>` 都有 `ID`、`UID`、`Title`、`Template`、`Author`、`Year`、`DBUID`。
