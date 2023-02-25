# mushikui
## 概要

ここに実装されている関数solverは、与えられた掛け算の虫食い算を解くものです。関数は以下の引数をとります。

multiple_line1 (str)：掛けられる数を表す文字列。数字と\*のみからなる。  
multiple_line2 (str)：掛ける数を表す文字列。数字と\*のみからなる。  
intermediate_lines (List[str])：掛け算の中間結果を表す文字列のリスト。0の場合は0と表す。数字と\*のみからなる。  
product_line (str)：掛け算の結果を表す文字列。数字と*のみからなる。  

戻り値は、掛けられる数と掛ける数のタプルです。また、引数の値に誤りがある場合はValueErrorが発生します。
答えが複数あるかどうかのチェックは行っておらず、最初に見つかった組み合わせを返します。

関数の処理は、深さ優先探索を用いて、掛けられる数と掛ける数の組み合わせを調べていきます。掛け算の中間結果と掛け算の結果が与えられているため、それらをもとに掛けられる数と掛ける数を求めることができます。

## 処理概要
1. 入力に対して、各行の取りうる値の幅を求める。
2. 空のスタックを用意する。
3. どこの虫食い文字を探索するかを決める。数字の両端に近い虫食いを優先する。
4. その虫食い文字に対して、取りうる値を入れていく。取りうる値の幅と矛盾しないか、mod 10^n が矛盾しないかを確認する。矛盾している場合はスタックに積まない。
5. 虫食い部分が全て埋まっている場合は、検証を行う。正解なら終了、不正解ならスタックに積まない。
6. スタックの最後から取り出し(深さ優先探索)、次の虫食い文字を探索する。(3)に戻る。
7. スタックが空になったら、探索失敗として終了する。

## 検証
* 処理概要の6を「スタックの最初から取り出す」とすると、幅優先探索になる。10倍ぐらいの計算量がかかる。虫食い算は最後まで探索しないと答えがわからないため、深さ優先探索が適している。

* 処理概要3の「数字の両端に近い虫食いを優先する」の工夫が、計算量を大幅に削減している。実際この処理を外して、探索する虫食いを前から順番にするようにすると、計算時間が大幅に増加した。