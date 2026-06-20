import master_Mind as game


def test_Backdoor_Removed():
    assert not hasattr(game, "show_Secret")
    assert game.parse_Guess("cheat") is None


def test_Get_Feedback():
    assert game.get_Feedback(
        ["R", "G", "B", "Y"], ["R", "G", "B", "Y"]
    ) == (4, 0)
    assert game.get_Feedback(
        ["R", "G", "B", "Y"], ["Y", "B", "G", "R"]
    ) == (0, 4)
    assert game.get_Feedback(
        ["R", "R", "G", "B"], ["R", "G", "R", "O"]
    ) == (1, 2)


def test_Parse_Guess():
    assert game.parse_Guess("RGBY") == ["R", "G", "B", "Y"]
    assert game.parse_Guess("R G B Y") == ["R", "G", "B", "Y"]
    assert game.parse_Guess("rood groen blauw geel") == [
        "R", "G", "B", "Y"
    ]
    assert game.parse_Guess("R G B") is None


def test_Generate_Code():
    generated_Code = game.generate_Code()
    assert len(generated_Code) == 4
    assert all(color in game.COLORS for color in generated_Code)


def run_Tests():
    test_Backdoor_Removed()
    test_Get_Feedback()
    test_Parse_Guess()
    test_Generate_Code()
    print("Alle tests geslaagd.")


if __name__ == "__main__":
    run_Tests()
