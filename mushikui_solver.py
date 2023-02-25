# 虫食い算数のsolver

import math
import re
from typing import List, Tuple


def find_star_index(str1: str, str2: str) -> int:
    """与えられた二つの文字列中の '*' の位置を見つける関数。

    Args:
        str1 (str): 入力文字列1
        str2 (str): 入力文字列2

    Returns:
        int: str1またはstr2中の最初の'*'の位置を返す。'*'がどちらにもない場合は-1を返す。
    """
    star1_first = str1.find("*")
    star1_last = str1.rfind("*")
    star2_first = str2.find("*")
    star2_last = str2.rfind("*")  # 11* -> 2

    priorities = [
        star1_first,
        len(str1) - star1_last - 1,
        star2_first,
        len(str2) - star2_last - 1,
    ]

    if star1_first == -1:
        priorities[0] = math.inf
        priorities[1] = math.inf
    if star2_first == -1:
        priorities[2] = math.inf
        priorities[3] = math.inf

    if star1_first == -1 and star2_first == -1:
        return -1

    min_index = priorities.index(min(priorities))

    if min_index == 0:
        return star1_first
    if min_index == 1:
        return star1_last
    if min_index == 2:
        return len(str1) + 1 + star2_first
    if min_index == 3:
        return len(str1) + 1 + star2_last


def get_next_node_candidates(node: Tuple[str, str]) -> List[Tuple[str, str]]:
    """次のノードの候補を生成する関数。

    Args:
        node (Tuple[str, str]): (被乗数, 乗数)を格納したタプル

    Returns:
        List[Tuple[str, str]]: 入力ノードに対する候補ノードのリスト
    """
    multiple_line_1, multiple_line_2 = node

    # get minimum star index
    line_joined = multiple_line_1 + "_" + multiple_line_2

    star_index = find_star_index(multiple_line_1, multiple_line_2)

    # star_index = line_joined.rfind("*") this is slow

    if star_index == -1:
        raise ValueError("Error: no answer")

    if star_index == 0 or star_index == len(multiple_line_1) + 1:
        replacing_numbers = [str(i) for i in range(1, 10)]
    else:
        replacing_numbers = [str(i) for i in range(10)]

    # star_index をreplacing_numbersで置き換える
    ret_joined = [
        line_joined[:star_index] + number + line_joined[star_index + 1:]
        for number in replacing_numbers
    ]

    return [tuple(line.split("_")) for line in ret_joined]


def is_correct_answer(
    node: Tuple[str, str],
    intermediate_lines_regex: List[re.Pattern],
    product_line_regex: re.Pattern,
) -> bool:
    """
    与えられたノードが正解かどうかをチェックする関数。

    Args:
        node: Tuple[str, str] 掛け算の左辺と右辺が含まれたタプル。例: ('10*1', '29')
        intermediate_lines_regex:List[re.Pattern] 掛け算の途中結果に対する正規表現のリスト。
        product_line_regex: re.Pattern 掛け算の結果に対する正規表現。

    Returns:
        正解の場合はTrue、そうでない場合はFalse。
    """
    # no star
    assert "*" not in node[0] and "*" not in node[1]

    multiple_line_1, multiple_line_2 = node

    # check product line
    product = str(int(multiple_line_1) * int(multiple_line_2))
    # 正規表現で完全一致かチェック
    if not product_line_regex.match(product):
        return False

    for multiple_line_2_char, intermediate_line_regex in zip(
        reversed(multiple_line_2), intermediate_lines_regex
    ):
        product_single = str(int(multiple_line_1) * int(multiple_line_2_char))
        if not intermediate_line_regex.match(product_single):
            return False

    return True


def check_mod(multiple_1: str, multiple_2: str, product: str) -> bool:
    """
    掛け算の結果が信頼できる桁数まで一致しているかの確認。mod 10**n で一致しているかを確認する。

    Args:
        multiple_1: 掛け算の左辺の数字の文字列。
        multiple_2: 掛け算の右辺の数字の文字列。
        product: 掛け算の結果の数字の文字列。

    Returns:
        信頼できる桁数まで一致している場合はTrue、そうでない場合はFalse。
        信頼できる桁数が0のときはTrueを返す。
    """

    # 信頼できる桁数を計算
    last_star_index1 = multiple_1.rfind("*")
    last_star_index2 = multiple_2.rfind("*")
    last_star_product = product.rfind("*")

    if last_star_index1 == -1:
        reliable_digit1 = math.inf
    else:
        reliable_digit1 = len(multiple_1) - \
            last_star_index1 - 1  # *99 なら3-0-1 = 2

    if last_star_index2 == -1:
        reliable_digit2 = math.inf
    else:
        reliable_digit2 = len(multiple_2) - \
            last_star_index2 - 1  # *99 なら3-0-1 = 2

    if last_star_product == -1:
        reliable_digit_product = math.inf
    else:
        reliable_digit_product = len(
            product) - last_star_product - 1  # *99 なら3-0-1 = 2

    reliable_digit = min(reliable_digit1, reliable_digit2,
                         reliable_digit_product)
    if reliable_digit == 0:
        return True

    if reliable_digit == math.inf:
        return int(multiple_1) * int(multiple_2) == int(product)

    # 信頼できる桁数までの桁数が一致しているかチェック

    multiple_1 = multiple_1[last_star_index1 + 1:]
    multiple_2 = multiple_2[last_star_index2 + 1:]
    return (
        str(int(multiple_1) * int(multiple_2))[-reliable_digit:]
        == product[-reliable_digit:]
    )


def make_min_max(string: str) -> Tuple[int, int]:
    """
    stringの最小値と最大値を計算する。

    Args:
        string (str): *を含む文字列

    Returns:
        tuple: stringが取りうる最小値と最大値のタプル。
    """
    min_str = string.replace("*", "0")
    max_str = string.replace("*", "9")
    if min_str[0] == "0":
        # replace first 0 to 1
        min_str = "1" + min_str[1:]
    return int(min_str), int(max_str)


def range_check(multiple_1: str, multiple_2: str, product_min: int, product_max: int):
    """
    productの最小値と最大値が、掛け算の最小値と最大値と範囲が重なるかどうかチェックする。

    Args:
        multiple_1 (str): *を含む1つ目の掛けられる数
        multiple_2 (str): *を含む2つ目の掛けられる数
        product_min (int): 掛け算の結果の最小値
        product_max (int): 掛け算の結果の最大値

    Returns:
        bool: productの最小値と最大値が掛け算の最小値と最大値の範囲と重なる場合はTrue。それ以外はFalse。
    """
    multiple_1_min, multiple_1_max = make_min_max(multiple_1)
    multiple_2_min, multiple_2_max = make_min_max(multiple_2)
    if multiple_1_max * multiple_2_max < product_min:
        return False
    if multiple_1_min * multiple_2_min > product_max:
        return False
    return True


def is_wrong_answer_mod(
    node: Tuple[int, int], intermediate_lines: List[str], product_line: str
) -> bool:
    """
    各桁の掛け算と全部の掛け算の結果に対してmodでみて、nodeが正しい答えでない場合にTrueを返す。

    Args:
        node (tuple): *を含む2つの数
        intermediate_lines (list): *を含む中間の計算のリスト
        product_line (str): *を含む計算結果

    Returns:
        bool: 正しい答えでない場合はTrue。それ以外はFalse。
    """
    if not check_mod(node[0], node[1], product_line):
        return True

    for char_in_node_2, intermediate_line in zip(reversed(node[1]), intermediate_lines):
        if not check_mod(node[0], char_in_node_2, intermediate_line):
            return True
    return False


def is_wrong_answer_range(
    node: Tuple[int, int],
    intermediate_lines_min_max: List[Tuple[int, int]],
    product_line_min_max: Tuple[int, int],
) -> bool:
    """
    各桁の掛け算と全部の掛け算の結果に対して桁数の観点でみて、nodeが正しい答えでない場合にTrueを返す。


    Args:
        node (tuple): *を含む2つの数
        intermediate_lines_min_max (list): 中間の計算の最小値と最大値のリスト
        product_line_min_max (tuple): 計算結果の最小値と最大値のタプル

    Returns:
        bool: 桁数の観点で正しい答えでない場合はTrue。それ以外はFalse。
    """

    product_min, product_max = product_line_min_max
    if not range_check(node[0], node[1], product_min, product_max):
        return True

    for char_in_node_2, intermediate_line_min_max in zip(
        reversed(node[1]), intermediate_lines_min_max
    ):
        min_, max_ = intermediate_line_min_max
        if not range_check(node[0], char_in_node_2, min_, max_):
            return True
    return False


def convert_to_regex(line: str) -> re.Pattern:
    """
    文字列を正規表現に変換する。

    Args:
        line (str): *を含む文字列

    Returns:
        re.Pattern: 入力の*を正規表現に置き換えたオブジェクト
    """

    # 先頭の*を[1-9]に置き換える
    if line[0] == "*":
        line = "[1-9]" + line[1:]
    # 他の* を [0-9]に置き換える
    line = line.replace("*", "[0-9]")
    return re.compile(line)


def make_min_max_product_line(
    product_line: str, intermediate_lines_min_max: List[Tuple[int, int]]
):
    """掛け算の結果の最小値と最大値を計算する。
       product_lineの最小値と最大値と、intermediate_lines_min_maxから作られる最小値と最大値の狭いレンジを返す。

    Args:
        product_line (str): 掛け算の結果を表す文字列。
        intermediate_lines_min_max (List[Tuple[int, int]]): 掛け算の中間結果の最小値と最大値のリスト。

    Returns:
        Tuple[int, int]: 掛け算の結果の最小値と最大値をタプルで返す。
    """
    tmp_min, tmp_max = make_min_max(product_line)

    tmp_min2 = 0
    tmp_max2 = 0

    for i, intermediate_line_min_max in enumerate(intermediate_lines_min_max):
        tmp_min2 += intermediate_line_min_max[0] * 10**i
        tmp_max2 += intermediate_line_min_max[1] * 10**i
    return max(tmp_min, tmp_min2), min(tmp_max, tmp_max2)


def validate_input(
    multiple_line1: str,
    multiple_line2: str,
    intermediate_lines: List[str],
    product_line: str,
):
    """
    入力値が適切かどうかを検証する関数

    Args:
        multiple_line1 (str): 掛けられる数1を表す文字列
        multiple_line2 (str): 掛けられる数2を表す文字列
        intermediate_lines (List[str]): 一桁ごとの計算結果を表す文字列が格納されたリスト
        product_line (str): 掛け算の結果を表す文字列

    Raises:
        ValueError: multiple_line2とintermediate_linesの長さが異なる場合、
                    multiple_line1、multiple_line2、product_line、intermediate_linesのいずれかに数字と*以外の文字が含まれる場合

    """
    if len(multiple_line2) != len(intermediate_lines):
        raise ValueError(
            "Error: the length of multiple_line2 and intermediate_lines are different"
        )
    # 数字と*のみからなるかチェック
    regex = re.compile(r"^[0-9*]+$")
    if not regex.match(multiple_line1):
        raise ValueError(
            "Error: multiple_line1 should contain only numbers and *, and length should be 1 or more")

    if not regex.match(multiple_line2):
        raise ValueError(
            "Error: multiple_line2 should contain only numbers and *, and length should be 1 or more")

    if not regex.match(product_line):
        raise ValueError(
            "Error: product_line should contain only numbers and *, and length should be 1 or more")

    for intermediate_line in intermediate_lines:
        if not regex.match(intermediate_line):
            raise ValueError(
                "Error: intermediate_line should contain only numbers and *, and length should be 1 or more"
            )


def solver(
    multiple_line1: str,
    multiple_line2: str,
    intermediate_lines: List[str],
    product_line: str,
):
    """与えられた虫食い算を解く。

    Args:
        multiple_line1 (str): 掛けられる数を表す文字列。数字と*のみからなる。
        multiple_line2 (str): 掛ける数を表す文字列。数字と*のみからなる。
        intermediate_lines (List[str]): 掛け算の中間結果を表す文字列のリスト。0の場合は0と表す。数字と*のみからなる。
        product_line (str): 掛け算の結果を表す文字列。数字と*のみからなる。

    Returns:
        Tuple[str, str]: 掛けられる数と掛ける数をタプルで返す。

    Raises:
        ValueError: 掛ける数の桁数と中間結果の数が一致していない場合、解が見つからない場合。
    """
    print(f"{multiple_line1}")
    print(f"{multiple_line2}")
    print(f"intermediate:")
    for line in intermediate_lines:
        print(f"{line}")
    print(f"product:")
    print(f"{product_line}")

    validate_input(multiple_line1, multiple_line2,
                   intermediate_lines, product_line)

    intermediate_lines_min_max = [make_min_max(
        line) for line in intermediate_lines]
    product_line_min_max = make_min_max_product_line(
        product_line, intermediate_lines_min_max
    )

    intermediate_lines_regex = [convert_to_regex(
        line) for line in intermediate_lines]
    product_line_regex = convert_to_regex(product_line)

    visited = set()
    stack = [(multiple_line1, multiple_line2)]
    counter = 0
    while stack:
        node = stack.pop()
        if counter % 1 == 0:
            print(f"counter:{counter},node:{node},len(stack):{len(stack)}")
        counter += 1
        if node in visited:
            continue
        visited.add(node)

        # "****" -> "***0", "***1", "***2", "***3", "***4", "***5", "***6", "***7", "***8", "***9"
        next_node_candidates = get_next_node_candidates(node)

        for candidate in next_node_candidates:
            if candidate in visited:
                continue

            # 全部埋まったらチェック
            if "*" not in candidate[0] and "*" not in candidate[1]:
                if is_correct_answer(
                    candidate, intermediate_lines_regex, product_line_regex
                ):
                    answer = candidate
                    print(f"Answer: {answer}")

                    for ans2_char in reversed(answer[1]):
                        print(
                            f"intermediate:{int(answer[0]) * int(ans2_char)}")
                    print(f"product:{int(answer[0]) * int(answer[1])}")
                    print(f"visited:{len(visited)}")
                    visited.add(candidate)

                    return candidate
                else:
                    # wrong answer
                    visited.add(candidate)
                    continue

            # 枝切り用
            if is_wrong_answer_mod(candidate, intermediate_lines, product_line):
                # print(f"wrong answer mod:{candidate}")
                visited.add(candidate)
                continue

            if is_wrong_answer_range(
                candidate, intermediate_lines_min_max, product_line_min_max
            ):
                visited.add(candidate)
                # print(f"wrong answer range:{candidate}")
                continue

            stack.append(candidate)
    print(f"visited:{len(visited)}")
    raise ValueError("Error: no answer")


if __name__ == "__main__":
    multiple_line_1 = "******"
    multiple_line_2 = "****"
    intermediate_lines = ["66****", "6*****", "**666**", "**6**6"]
    product_line = "****66****"

    solver(multiple_line_1, multiple_line_2, intermediate_lines, product_line)

    multiple_line_1 = "2*"
    multiple_line_2 = "**"
    intermediate_lines = ["*3*", "**"]
    product_line = "*4*"

    solver(multiple_line_1, multiple_line_2, intermediate_lines, product_line)

    multiple_line_1 = "**1"
    multiple_line_2 = "*2*"
    intermediate_lines = ["*3**", "*4**", "*5**"]
    product_line = "6*****"

    solver(multiple_line_1, multiple_line_2, intermediate_lines, product_line)
