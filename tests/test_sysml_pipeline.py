from app.generators.sysml_pipeline import generate_l1_sysml


def test_generate_l1_sysml(tmp_path):

    output_file = tmp_path / "L1_TwoTankController.sysml"

    result = generate_l1_sysml(str(output_file))

    assert result.exists()

    content = result.read_text(encoding="utf-8")

    assert "package L1_TwoTankController" in content
    assert "part TK-101 : Tank;" in content
    assert "part TK-102 : Tank;" in content
    assert "part XV-101 : OnOffValve;" in content
    assert "FILL_T1" in content
    assert "TRANSFER_T1_T2" in content
    assert "SHUTDOWN" in content