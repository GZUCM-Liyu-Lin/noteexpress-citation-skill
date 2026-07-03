import argparse
import re
import zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docx")
    args = parser.parse_args()

    docx = Path(args.docx)
    with zipfile.ZipFile(docx) as z:
        bad = z.testzip()
        xml = {
            name: z.read(name).decode("utf-8", errors="ignore")
            for name in z.namelist()
            if name.startswith("word/") and name.endswith(".xml")
        }
        media = [name for name in z.namelist() if name.startswith("word/media/") and not name.endswith("/")]

    combined = "\n".join(xml.values())
    settings = xml.get("word/settings.xml", "")
    document = xml.get("word/document.xml", "")
    instr = re.findall(r"<w:instrText[^>]*>(.*?)</w:instrText>", document)

    ne_ref_instr = [item for item in instr if "ADDIN NE.Ref." in item]
    ne_bib_instr = [item for item in instr if "ADDIN NE.Bib" in item]
    docvar_refs = re.findall(r'w:name="NE\.Ref\{[^"]+\}"', settings)

    print(f"docx={docx}")
    print(f"zip_bad={bad}")
    print(f"media={len(media)}")
    print(f"NE.Ref instr={len(ne_ref_instr)}")
    print(f"NE.Bib instr={len(ne_bib_instr)}")
    print(f"NE.Ref docVars={len(docvar_refs)}")
    print(f"NoteExpress markers total={combined.count('NoteExpress') + combined.count('NE.Ref') + combined.count('NE.Bib')}")

    if bad is not None:
        raise SystemExit(2)
    if not ne_ref_instr or not ne_bib_instr or len(ne_ref_instr) != len(docvar_refs):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
