from app.generators.file_writer import save_text


def test_save_text(tmp_path):

    output_file = tmp_path / "example.sysml"

    content = "package TestSystem {}"

    save_text(content, str(output_file))

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == content