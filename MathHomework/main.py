#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
My Math HOmework
函数极限求解器（by ZiaoLin,ID20261055129,with Gpt-6.3luna)
=========================================================
书写规则：
  乘方    ^               例：x^2        (1+1/x)^x
  开方    √               例：√x   √(x+1)   √2
  绝对值  |x|             例：|x|/x
  阶乘    n!   双阶乘 n!!  例：n!/(k!(n-k)!)
  组合数  C(n,k)  排列数 P(n,k)
  自然常数 e、e^x
  虚数单位 独立写的 i 会被当作 I（虚数单位）
  圆周率  pi 或 π
  无穷大  oo / inf / ∞     负无穷 -oo…
  对数    ln(x)   log(x)  log10(x)  log2(x)
  三角/反三角/双曲函数：sin cos tan cot sec csc
                        asin acos atan acot asec acsc
                        arcsin/arccos/arctan 亦可
                        sinh cosh tanh asinh acosh atanh
  取整    floor ceil frac
  特殊函数 erf erfc zeta DiracDelta Heaviside
  隐式乘法 2x   3sin(x)   2(x+1)   x(x+1)
=========================================================
用法：
  命令行： python main.py "sin(x)/x" x 0
           python main.py "(1+1/x)^x" x oo
           python main.py "1/x" x 0 +
           python main.py -f batch.txt
  交互式： python main.py

"""

import re
import sys
import os

from sympy import (
    Symbol, limit, Limit, oo, zoo, nan, I,
    sqrt, E, pi, log, exp,
    sin, cos, tan, cot, sec, csc,
    asin, acos, atan, acot, asec, acsc,
    sinh, cosh, tanh, asinh, acosh, atanh,
    Abs, sign, factorial, factorial2, gamma,
    binomial,
    floor, ceiling,
    erf, erfc,
    zeta,
    DiracDelta, Heaviside,
    GoldenRatio, EulerGamma, Catalan,
    latex,
)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)


# ----------------------------------------------------------------------------
# 0. 补上 sympy 顶层没有、或版本差异较大的函数
# ----------------------------------------------------------------------------

# 排列数 P(n,k) = n! / (n-k)!
def permutation(n, k):
    return factorial(n) / factorial(n - k)


# 小数部分 frac(x) = x - floor(x)
def frac(x):
    return x - floor(x)


# ceil 是 ceiling 的简写
ceil = ceiling

# erfi：若当前 sympy 版本没有，则退化为 erf
try:
    from sympy import erfi as _erfi
    erfi = _erfi
except ImportError:
    erfi = erf


# 以 10 / 2 为底的对数
def _log10(x):
    return log(x, 10)


def _log2(x):
    return log(x, 2)


# ----------------------------------------------------------------------------
# 1. 解析环境
# ----------------------------------------------------------------------------
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)

BASE_LOCALS = {
    # 常量
    'E': E, 'pi': pi, 'oo': oo, 'inf': oo, 'I': I,
    'GoldenRatio': GoldenRatio,
    'EulerGamma': EulerGamma,
    'Catalan': Catalan,
    # 根号 / 指数 / 对数
    'sqrt': sqrt, 'exp': exp, 'ln': log, 'log': log,
    'log10': _log10, 'log2': _log2,
    # 三角
    'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot,
    'sec': sec, 'csc': csc,
    # 反三角
    'asin': asin, 'acos': acos, 'atan': atan,
    'acot': acot, 'asec': asec, 'acsc': acsc,
    # 双曲
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    'asinh': asinh, 'acosh': acosh, 'atanh': atanh,
    # 组合数学
    'factorial': factorial, 'factorial2': factorial2,
    'binomial': binomial, 'binom': binomial,
    'permutation': permutation,
    'gamma': gamma,
    # 取整 / 绝对值 / 符号
    'Abs': Abs, 'abs': Abs, 'sign': sign,
    'floor': floor, 'ceil': ceil, 'ceiling': ceiling, 'frac': frac,
    # 特殊函数
    'erf': erf, 'erfc': erfc, 'erfi': erfi,
    'zeta': zeta,
    'DiracDelta': DiracDelta, 'Heaviside': Heaviside,
}

# 反三角 / 反双曲的别名
_ARCS = {
    'arcsin': 'asin', 'arccos': 'acos', 'arctan': 'atan',
    'arccot': 'acot', 'arcsec': 'asec', 'arccsc': 'acsc',
    'arsinh': 'asinh', 'arcosh': 'acosh', 'artanh': 'atanh',
}


def preprocess(s):
    """
    把"手写数学表达式"翻译成 SymPy 能看懂的语法。
    """
    if s is None:
        raise ValueError("表达式为空")
    s = str(s).strip()
    if not s:
        raise ValueError("表达式为空")

    # --- 全角 / 数学符号归一化 ---
    s = (s.replace('（', '(').replace('）', ')')
          .replace('［', '[').replace('］', ']')
          .replace('｛', '{').replace('｝', '}')
          .replace('×', '*').replace('·', '*').replace('÷', '/')
          .replace('−', '-').replace('–', '-').replace('—', '-')
          .replace('π', 'pi')
          .replace('∞', 'oo'))

    # --- 去掉所有空白字符 ---
    s = re.sub(r'\s+', '', s)

    # --- 乘方：^ -> ** ---
    s = s.replace('^', '**')

    # --- 开方 ---
    s = re.sub(r'√\(', 'sqrt(', s)                        # √(x+1)
    s = re.sub(r'√(\d+(?:\.\d+)?)', r'sqrt(\1)', s)       # √2
    s = re.sub(r'√([A-Za-z_]\w*)', r'sqrt(\1)', s)        # √x
    if '√' in s:
        raise ValueError("无法解析的根号写法，请写成 √x、√(x+1)、√2 这类形式")

    # --- 绝对值 |x| -> Abs(x) ---
    s = re.sub(r'\|([^|]+)\|', r'Abs(\1)', s)

    # --- 反三角 / 反双曲别名 ---
    for k, v in _ARCS.items():
        s = re.sub(r'\b' + k + r'\b', v, s)

    # --- 组合数 C(n,k) / 排列数 P(n,k) ---
    s = re.sub(r'\bC\(([^,()]+),([^,()]+)\)', r'binomial(\1,\2)', s)
    s = re.sub(r'\bP\(([^,()]+),([^,()]+)\)', r'permutation(\1,\2)', s)
    s = re.sub(r'\bbinom\(', 'binomial(', s)

    # --- 阶乘：先双阶乘，再单阶乘 ---
    s = re.sub(r'(\d+|[A-Za-z_]\w*|\([^()]*\))!!', r'factorial2(\1)', s)
    s = re.sub(r'(\d+|[A-Za-z_]\w*|\([^()]*\))!',  r'factorial(\1)',  s)

    # --- 自然常数 e -> E（只替换独立出现的 e） ---
    s = re.sub(r'(?<![A-Za-z_])e(?![A-Za-z_0-9])', 'E', s)

    # --- 虚数单位 i -> I（只替换独立出现的 i） ---
    s = re.sub(r'(?<![A-Za-z_])i(?![A-Za-z_0-9])', 'I', s)

    return s


def to_expr(s, extra_locals=None):
    """字符串 -> SymPy 表达式"""
    src = preprocess(s)
    loc = dict(BASE_LOCALS)
    if extra_locals:
        loc.update(extra_locals)
    try:
        return parse_expr(src, local_dict=loc,
                          transformations=TRANSFORMS, evaluate=True)
    except Exception as exc:
        raise ValueError(
            "无法解析表达式 “%s”（转换后为 “%s”）：%s" % (s, src, exc)
        ) from exc


# ----------------------------------------------------------------------------
# 2. 方向 & 趋近点
# ----------------------------------------------------------------------------
_DIR_ALIASES = {
    '+': '+', 'right': '+', '右': '+', '右极限': '+', '0+': '+',
    '-': '-', 'left':  '-', '左': '-', '左极限': '-', '0-': '-',
    '+-': '+-', 'both': '+-', '双向': '+-', '两侧': '+-',
    'none': '+-', 'default': '+-', '': '+-',
}


def normalize_direction(d):
    if d is None:
        return '+-'
    return _DIR_ALIASES.get(str(d).strip().lower(), '+-')


def parse_point(pt_str, extra_locals=None):
    """解析趋近点，支持 '0+' / '0-' 这种组合写法。"""
    s = str(pt_str).strip().replace(' ', '')
    auto_dir = None
    if s.endswith('+') or s.endswith('＋'):
        auto_dir, s = '+', s[:-1]
    elif s.endswith('-') or s.endswith('－'):
        auto_dir, s = '-', s[:-1]
    if s == '' or s in ('+', '-'):
        s = '0'
    return to_expr(s, extra_locals), auto_dir


# ----------------------------------------------------------------------------
# 3. 核心：求极限
# ----------------------------------------------------------------------------
def calc_limit(expr_str, var_name='x', point_str='0', direction=None):
    x = Symbol(var_name)
    extra = {var_name: x}

    f = to_expr(expr_str, extra)
    p, auto_dir = parse_point(point_str, extra)
    d = normalize_direction(direction if direction is not None else auto_dir)

    res = limit(f, x, p, dir=d)
    return f, x, p, d, res


# ----------------------------------------------------------------------------
# 4. 未定式提示
# ----------------------------------------------------------------------------
def check_indeterminate(f_expr, var, point):
    try:
        num, den = f_expr.as_numer_denom()
        ln = limit(num, var, point)
        ld = limit(den, var, point)
    except Exception:
        return
    if ln == 0 and ld == 0:
        print("  ⚠ 检测到 0/0 型未定式，可尝试洛必达法则。")
    elif ln in (oo, -oo) and ld in (oo, -oo):
        print("  ⚠ 检测到 ∞/∞ 型未定式，可尝试洛必达法则。")


# ----------------------------------------------------------------------------
# 5. 绘图
# ----------------------------------------------------------------------------
def plot_near_limit(f_expr, var, point, delta=1.0, n=400):
    try:
        import numpy as np
        import matplotlib.pyplot as plt
    except ImportError:
        print("  (绘图需要 numpy 与 matplotlib，请先安装)")
        return
    from sympy import lambdify

    if not point.is_number:
        print("  (趋近点不是数值，跳过绘图)")
        return
    try:
        p = float(point)
    except Exception:
        print("  (趋近点无法转为实数，跳过绘图)")
        return

    try:
        f = lambdify(var, f_expr, 'numpy')
    except Exception as exc:
        print("  无法转换为数值函数：%s" % exc)
        return

    xs = np.linspace(p - delta, p + delta, n)
    xs = xs[np.abs(xs - p) > 1e-6]
    with np.errstate(all='ignore'):
        ys = f(xs)

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label=str(f_expr))
    plt.axvline(p, color='r', linestyle='--', label='%s→%s' % (var, point))
    plt.legend()
    plt.grid(True)
    plt.title('f(%s) = %s' % (var, f_expr))
    plt.show()


# ----------------------------------------------------------------------------
# 6. 输出
# ----------------------------------------------------------------------------
def _dir_text(d):
    return {'+': '右极限 (a⁺)',
            '-': '左极限 (a⁻)',
            '+-': '双侧极限'}[d]


def run_once(expr_str, var_name='x', point_str='0', direction=None,
             show_latex=True):
    print('-' * 62)
    try:
        f, x, p, d, res = calc_limit(expr_str, var_name, point_str, direction)
    except Exception as exc:
        print("✗ 出错：%s" % exc)
        return None

    print("  原式   : %s" % expr_str)
    print("  解析为 : %s" % f)
    if show_latex:
        try:
            print("  LaTeX  : %s" % latex(f))
        except Exception:
            pass
    print("  自变量 : %s" % x)
    print("  趋近点 : %s   方向: %s" % (p, _dir_text(d)))

    # 未定式提示
    check_indeterminate(f, x, p)

    if isinstance(res, Limit):
        print("  ✗ 未能求出极限（SymPy 返回了未求值形式）")
        print("     %s" % res)
        return res

    print("  ✓ 极限 = %s" % res)
    if show_latex:
        try:
            print("  LaTeX  : %s" % latex(res))
        except Exception:
            pass

    try:
        if res.is_number and not res.is_Integer and not res.is_Rational:
            print("     ≈ %s" % res.evalf(12))
        elif res.is_Rational and res.q != 1:
            print("     ≈ %s" % res.evalf(12))
    except Exception:
        pass

    if res is zoo:
        print("      （复数意义下的无穷大，通常说明该极限不存在）")
    if res is nan:
        print("      （结果未定义，极限可能不存在）")

    return res


# ----------------------------------------------------------------------------
# 7. 批量处理
# ----------------------------------------------------------------------------
def batch_process(file_path):
    """从文本文件读取多行：表达式, 变量, 趋近点, 方向"""
    if not os.path.isfile(file_path):
        print("文件不存在：%s" % file_path)
        return
    with open(file_path, 'r', encoding='utf-8') as fp:
        for lineno, line in enumerate(fp, 1):
            raw = line.strip()
            if not raw or raw.startswith('#'):
                continue
            parts = [p.strip() for p in raw.split(',')]
            expr = parts[0]
            var = parts[1] if len(parts) > 1 and parts[1] else 'x'
            pt = parts[2] if len(parts) > 2 and parts[2] else '0'
            d = parts[3] if len(parts) > 3 and parts[3] else None
            print("\n[第 %d 行] %s" % (lineno, raw))
            run_once(expr, var, pt, d)


# ----------------------------------------------------------------------------
# 8. 入口
# ----------------------------------------------------------------------------
BANNER = r"""
============================================================
            函数极限自动求解器（增强版）  SymPy
============================================================
 书写规则：
  乘方   ^         开方 √          绝对值 |x|
  阶乘   n!  n!!   组合 C(n,k)     排列 P(n,k)
  自然常数 e      虚数单位 i       圆周率 pi 或 π
  无穷大 oo / inf / ∞             负无穷 -oo
  对数  ln(x)  log(x)  log10(x)  log2(x)
  三角 sin cos tan cot sec csc    反三角 asin/acos/atan ... 或 arcsin/...
  双曲 sinh cosh tanh ...         取整 floor ceil frac
  特殊函数 erf erfc zeta Heaviside DiracDelta
  隐式乘法 2x   3sin(x)   2(x+1)   x(x+1)
============================================================
"""


def interactive():
    print(BANNER)
    while True:
        try:
            expr = input("函数 f(x)  (直接回车退出): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not expr:
            break

        try:
            var = input("  自变量   [x] : ").strip() or 'x'
            pt = input("  趋近点   [0] : ").strip() or '0'
            d = input("  方向 both/+/- [both]: ").strip() or None
        except (EOFError, KeyboardInterrupt):
            print()
            break

        res = run_once(expr, var, pt, d)

        try:
            want_plot = input("  是否画图？[y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if want_plot == 'y' and res is not None:
            try:
                x = Symbol(var)
                f = to_expr(expr, {var: x})
                p, _ = parse_point(pt, {var: x})
                plot_near_limit(f, x, p)
            except Exception as exc:
                print("  绘图失败：%s" % exc)
        print()

    print("再见！")


def main():
    args = sys.argv[1:]

    if not args:
        interactive()
        return

    if args[0] in ('-h', '--help'):
        print(BANNER)
        return

    if args[0] == '-f':
        if len(args) < 2:
            print("用法：python main.py -f <文件路径>")
            return
        batch_process(args[1])
        return

    # 命令行单次计算
    expr = args[0]
    var = args[1] if len(args) > 1 else 'x'
    pt = args[2] if len(args) > 2 else '0'
    d = args[3] if len(args) > 3 else None
    run_once(expr, var, pt, d)


if __name__ == '__main__':
    main()