from src.tags import primary_tag


def test_primary_tag_picks_highest():
    assert primary_tag(["pri:high", "pri:low", "other"]) == "pri:high"
