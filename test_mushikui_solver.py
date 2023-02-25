import re

import pytest

from mushikui_solver import (
    check_mod,
    convert_to_regex,
    find_star_index,
    get_next_node_candidates,
    is_correct_answer,
    is_wrong_answer_mod,
    is_wrong_answer_range,
    make_min_max,
    make_min_max_product_line,
    range_check,
    solver,
    validate_input
)


def test_find_star_index():
    assert find_star_index("1*22", "111") == 1
    assert find_star_index("12*2", "111*11") == 2
    assert find_star_index("12*2", "11111") == 2
    assert find_star_index("1*22", "111**211") == 1
    assert find_star_index("11*22", "*111**211") == 6
    assert find_star_index("", "*111**211") == 1
    assert find_star_index(
        "1*1*12*2", "111**211*") == "1*1*12*2_111**211*".rfind("*")

    assert find_star_index("12", "111") == -1
    assert find_star_index("", "") == -1
    assert find_star_index("*", "*") in [0, 2]


def test_get_next_node_candidates():
    node1 = ("11*22", "3*4")
    expected = [("11*22", f"3{i}4") for i in range(10)]

    assert get_next_node_candidates(node1) == expected

    node2 = ("1*2", "34")
    expected = [(f"1{i}2", "34") for i in range(10)]
    assert get_next_node_candidates(node2) == expected

    node_3 = ("1*2", "*34")
    expected = [("1*2", f"{i}34") for i in range(1, 10)]
    assert get_next_node_candidates(node_3) == expected

    node_4 = ("*12", "34")
    expected = [(f"{i}12", "34") for i in range(1, 10)]
    assert get_next_node_candidates(node_4) == expected

    node_5 = ("*1*2", "34")
    expected = [(f"{i}1*2", "34") for i in range(1, 10)]
    assert get_next_node_candidates(node_5) == expected

    node_5 = ("1*2*", "34")
    expected = [(f"1*2{i}", "34") for i in range(0, 10)]
    assert get_next_node_candidates(node_5) == expected

    node_3 = ("1*2", "*3*4")
    expected = [("1*2", f"{i}3*4") for i in range(1, 10)]
    assert get_next_node_candidates(node_3) == expected

    node_3 = ("1*2", "3*4*")
    expected = [("1*2", f"3*4{i}") for i in range(0, 10)]
    assert get_next_node_candidates(node_3) == expected

    node_bad = ("12", "34")

    with pytest.raises(ValueError):
        get_next_node_candidates(node_bad)


def test_solver():
    # テストケース1
    multiple_line_1 = "5**"  # 517
    multiple_line_2 = "*4"  # 64
    intermediate_lines = ["20*8", "3**2"]
    product_line = "3308*"  # 33088

    assert solver(
        multiple_line_1, multiple_line_2, intermediate_lines, product_line
    ) == ("517", "64")

    # テストケース2
    multiple_line_1 = "**7"  # 107
    multiple_line_2 = "7*"  # 72
    intermediate_lines = ["***", "***"]
    product_line = "77**"  # 7704

    assert solver(
        multiple_line_1, multiple_line_2, intermediate_lines, product_line
    ) == ("107", "72")

    # len(intermediate_lines) != len(product_line2)
    with pytest.raises(ValueError) as e:
        solver(
            multiple_line_1,
            "*",
            intermediate_lines,
            product_line,
        )
    assert (
        str(e.value)
        == "Error: the length of multiple_line2 and intermediate_lines are different"
    )

    # no answer
    with pytest.raises(ValueError) as e:
        solver(
            "***",
            "**",
            ["***", "***"],
            "9973",  # prime number
        )
    assert str(e.value) == "Error: no answer"


def test_convert_to_regex():
    assert convert_to_regex("*1") == re.compile("[1-9]1")
    assert convert_to_regex("12*") == re.compile("12[0-9]")
    assert convert_to_regex("*") == re.compile("[1-9]")
    assert convert_to_regex("12*34") == re.compile("12[0-9]34")


def test_is_wrong_answer_mod():
    # mod product is bad
    assert is_wrong_answer_mod(
        ("517", "*4"), ["****", "****"], "33087") == True
    assert is_wrong_answer_mod(
        ("5*7", "*4"), ["****", "****"], "33087") == True
    assert is_wrong_answer_mod(
        ("517", "64"), ["****", "****"], "****7") == True
    assert is_wrong_answer_mod(
        ("*17", "64"), ["****", "****"], "***87") == True

    # mod product is good
    assert not is_wrong_answer_mod(
        ("*17", "64"), ["****", "****"], "***88") == True
    assert not is_wrong_answer_mod(
        ("517", "64"), ["****", "****"], "***88") == True

    # intermidiate mod is bad
    assert is_wrong_answer_mod(
        ("517", "64"), ["****", "***1"], "*****") == True
    assert is_wrong_answer_mod(
        ("517", "*4"), ["***7", "****"], "*****") == True
    assert is_wrong_answer_mod(
        ("5*7", "64"), ["***7", "***1"], "*****") == True

    # intermidiate mod is good
    assert not is_wrong_answer_mod(
        ("517", "64"), ["***8", "***2"], "*****") == True
    assert not is_wrong_answer_mod(
        ("517", "*4"), ["***8", "****"], "*****") == True
    assert not is_wrong_answer_mod(
        ("5*7", "64"), ["***8", "***2"], "*****") == True


def test_make_make_min_max_product_line():
    product_line = "**"
    intermediate_lines_min_max = [(1, 5), (2, 4)]
    assert make_min_max_product_line(product_line, intermediate_lines_min_max) == (
        21,
        45,
    )

    product_line = "3*"
    intermediate_lines_min_max = [(1, 5), (2, 4)]
    assert make_min_max_product_line(product_line, intermediate_lines_min_max) == (
        30,
        39,
    )

    product_line = "3*"
    intermediate_lines_min_max = [(1, 4), (2, 3)]
    assert make_min_max_product_line(product_line, intermediate_lines_min_max) == (
        30,
        34,
    )


def test_is_wrong_answer_range():
    assert is_wrong_answer_range(
        ("5*7", "64"), [(1000, 9999), (1000, 9999)], (40000, 49999)
    )
    assert is_wrong_answer_range(
        ("5*7", "64"), [(1000, 9999), (1000, 9999)], (20000, 29999)
    )

    assert is_wrong_answer_range(
        ("***", "8*"), [(1000, 9999), (1000, 9999)], (90000, 99999)
    )
    assert is_wrong_answer_range(
        ("***", "1*"), [(1000, 9999), (1000, 9999)], (100, 999)
    )

    assert is_wrong_answer_range(
        ("***", "**"), [(10, 99), (100, 999)], (100, 999))
    assert is_wrong_answer_range(
        ("***", "**"), [(10, 99), (10000, 99999)], (100, 999))


def test_range_check():
    assert range_check("1*2", "3*4", 75640, 75649)
    assert not range_check("1*2", "3*4", 76640, 76649)

    assert not range_check("1**", "1**", 0, 9999)
    assert not range_check("*", "*", 0, 0)
    assert not range_check("*", "*", 90, 99)

    assert range_check("1**", "1**", 20000, 20001)
    assert range_check("*", "*", 81, 81)
    assert range_check("*", "*", 1, 9)


def test_make_min_max():
    assert make_min_max("1*2") == (102, 192)
    assert make_min_max("***") == (100, 999)
    assert make_min_max("1") == (1, 1)


def test_check_mod():
    # テストケース1: 正しい場合（信頼できる桁数が1の場合）
    multiple_1 = "5*3"
    multiple_2 = "2*7"
    product = "16*11"

    assert check_mod(multiple_1, multiple_2, product) == True

    # テストケース2: 正しい場合（信頼できる桁数が0の場合）
    multiple_1 = "31*"
    multiple_2 = "*2"
    product = "0"

    assert check_mod(multiple_1, multiple_2, product) == True

    # テストケース3: 信頼できる桁数が全ての場合
    multiple_1 = "56"
    multiple_2 = "72"
    product = "4032"

    assert check_mod(multiple_1, multiple_2, product) == True

    # テストケース4: 不正な場合
    multiple_1 = "5*3"
    multiple_2 = "2*7"
    product = "16*10"

    # テストケース5:　片方の信頼できる桁数が全ての場合
    multiple_1 = "*11"
    multiple_2 = "11"
    product = "*21"

    assert check_mod(multiple_1, multiple_2, product) == True


def test_is_correct_answer():
    # テストケース1: 正しい場合
    multiple_line_1 = "517"
    multiple_line_2 = "64"
    intermediate_lines = ["20*8", "3**2"]
    product_line = "3308*"  # 33088

    intermediate_lines_regex = [convert_to_regex(
        line) for line in intermediate_lines]
    product_line_regex = convert_to_regex(product_line)

    assert (
        is_correct_answer(
            (multiple_line_1, multiple_line_2),
            intermediate_lines_regex,
            product_line_regex,
        )
        == True
    )

    intermediate_lines = ["***8", "***2"]
    product_line = "*3***"  # 33088

    intermediate_lines_regex = [convert_to_regex(
        line) for line in intermediate_lines]
    product_line_regex = convert_to_regex(product_line)

    assert (
        is_correct_answer(
            (multiple_line_1, multiple_line_2),
            intermediate_lines_regex,
            product_line_regex,
        )
        == True
    )

    intermediate_lines = ["20*8", "3**2"]
    product_line = "4308*"  # 33088

    intermediate_lines_regex = [convert_to_regex(
        line) for line in intermediate_lines]
    product_line_regex = convert_to_regex(product_line)

    assert (
        not is_correct_answer(
            (multiple_line_1, multiple_line_2),
            intermediate_lines_regex,
            product_line_regex,
        )
        == True
    )

    intermediate_lines = ["30*8", "3**2"]
    product_line = "3308*"  # 33088

    intermediate_lines_regex = [convert_to_regex(
        line) for line in intermediate_lines]
    product_line_regex = convert_to_regex(product_line)

    assert (
        not is_correct_answer(
            (multiple_line_1, multiple_line_2),
            intermediate_lines_regex,
            product_line_regex,
        )
        == True
    )


def test_validate_input():
    with pytest.raises(ValueError):
        # multiple_line1にaが含まれている
        validate_input("a*1", "23*", ["456*"], "789*")

    with pytest.raises(ValueError):
        # multiple_line2にaが含まれている
        validate_input("12", "23*a", ["456*"], "789*")

    with pytest.raises(ValueError):
        # intermediate_linesの長さがmultiple_line2と異なる
        validate_input("12", "23", ["456", "78*", "*"], "90*")

    with pytest.raises(ValueError):
        validate_input("12", "23", ["456", "78*"],
                       "90a")  # product_lineにaが含まれている

    with pytest.raises(ValueError):
        # intermediate_linesにaが含まれている
        validate_input("12", "23", ["456", "78*a"], "90*")

    with pytest.raises(ValueError):
        # 空文字はエラー
        validate_input("1", "", ["456", "78*a"], "90*")

    with pytest.raises(ValueError):
        # 空文字はエラー
        validate_input("1", "23", ["", "78*a"], "90*")

    with pytest.raises(ValueError):
        # 空文字はエラー
        validate_input("1", "23", ["456", ""], "90*")

    with pytest.raises(ValueError):
        # 空文字はエラー
        validate_input("1", "23", ["456", "78*a"], "")

    with pytest.raises(ValueError):
        # 空文字はエラー
        validate_input("", "", [], "")

    # エラーにならないケース
    validate_input("1*2*", "*2*3*",
                   ["*4*5*6**", "***789", "*", "*", "3141"], "9*0*2*")
