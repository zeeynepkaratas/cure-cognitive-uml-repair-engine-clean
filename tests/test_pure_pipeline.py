from zipfile import ZipFile
from data_pipeline.preprocessing.xml_to_csv import process
from data_pipeline.vector_db.build_index import segments


def test_xml_entities_provenance_and_sentence_split(tmp_path):
    archive = tmp_path / "source.zip"
    with ZipFile(archive, "w") as bundle:
        bundle.writestr(
            "document.xml",
            "<root><p>Dr. Smith records a complaint &amp;amp; assigns an officer.</p><p>The officer reviews the evidence and files a report.</p></root>",
        )
    output = tmp_path / "out.csv"
    result = process(archive, output, tmp_path / "manifest.csv")
    text = output.read_text(encoding="utf-8")
    assert result["xml_documents"] == 1 and result["new_rows"] == 2
    assert "&amp;" not in text and "document.xml" in text
    assert "Dr. Smith" in text


def test_character_segments_overlap_and_tail():
    chunks = list(segments("x" * 1100))
    assert [len(c) for c in chunks] == [500, 500, 200]
    assert list(segments("short")) == ["short"]
