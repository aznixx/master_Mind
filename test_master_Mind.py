import os

import master_Mind as game


def test_Backdoor_Removed():
    assert not hasattr(game, "show_Secret")
    assert game.parse_Guess("cheat") is None


def test_Admin_Check():
    old_Password = os.environ.get(game.ADMIN_PASSWORD_ENV)

    try:
        os.environ.pop(game.ADMIN_PASSWORD_ENV, None)
        assert not game.is_Admin_Password("test")

        os.environ[game.ADMIN_PASSWORD_ENV] = "test"
        assert game.is_Admin_Password("test")
        assert not game.is_Admin_Password("wrong")
    finally:
        if old_Password is None:
            os.environ.pop(game.ADMIN_PASSWORD_ENV, None)
        else:
            os.environ[game.ADMIN_PASSWORD_ENV] = old_Password


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
    test_Admin_Check()
    test_Get_Feedback()
    test_Parse_Guess()
    test_Generate_Code()
    print("Alle tests geslaagd.")


if __name__ == "__main__":
    run_Tests()
