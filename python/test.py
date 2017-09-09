import cProfile

import env
import interp
import std
import type

e = env.Env()
tmp = lambda: [interp.interp0(["do", ["load", type.String("test.kf")]], e, None) for i in range(0, 200)]
cProfile.run("tmp()", sort="tottime")
print(len(e.env))
"""
         8970826 function calls (8426026 primitive calls) in 5.486 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
343400/200    0.991    0.000    5.484    0.027 interp.py:163(interp0)
   194800    0.510    0.000    0.617    0.000 env.py:9(get)
   601800    0.506    0.000    0.506    0.000 interp.py:59(next)
      400    0.426    0.001    1.600    0.004 interp.py:75(preProcess)
    59200    0.296    0.000    0.424    0.000 interp.py:10(parse_value)
45200/2000    0.278    0.000    3.266    0.002 type.py:113(__call__)
  1671002    0.245    0.000    0.245    0.000 {built-in method builtins.isinstance}
87000/200    0.239    0.000    5.482    0.027 type.py:177(__call__)
   601400    0.206    0.000    0.712    0.000 interp.py:57(__next__)
309400/254000    0.196    0.000    0.239    0.000 env.py:70(clean)
  1381000    0.121    0.000    0.121    0.000 {built-in method builtins.id}
   390800    0.106    0.000    0.169    0.000 type.py:38(is_lazy)
      400    0.102    0.000    1.869    0.005 interp.py:145(parse)
   219000    0.085    0.000    0.085    0.000 env.py:55(__init__)
   219000    0.083    0.000    0.273    0.000 env.py:82(__del__)
   225600    0.079    0.000    0.526    0.000 interp.py:87(writeBuffer)
   386000    0.073    0.000    0.074    0.000 env.py:60(extend)
   669804    0.072    0.000    0.072    0.000 {method 'append' of 'list' objects}
     5600    0.058    0.000    0.808    0.000 std.py:343(_filter)
   118401    0.053    0.000    0.053    0.000 {method 'join' of 'str' objects}
      400    0.051    0.000    0.052    0.000 {built-in method io.open}
   175600    0.048    0.000    0.064    0.000 interp.py:92(addBuffer)
    55200    0.043    0.000    0.049    0.000 env.py:26(define)
    12400    0.040    0.000    0.047    0.000 type.py:82(__init__)
   173400    0.039    0.000    0.039    0.000 {method 'startswith' of 'str' objects}
   306600    0.039    0.000    0.039    0.000 type.py:26(is_none)
  400/200    0.035    0.000    5.418    0.027 std.py:165(_load)
    55200    0.033    0.000    0.036    0.000 env.py:42(__delitem__)
7600/1000    0.031    0.000    2.943    0.003 std.py:80(_if)
    59200    0.028    0.000    0.035    0.000 util.py:1(is_quote_by)
 2600/200    0.025    0.000    5.446    0.027 std.py:12(_do)
   207400    0.024    0.000    0.024    0.000 {built-in method builtins.len}
 2800/200    0.024    0.000    2.578    0.013 std.py:97(_let)
    52600    0.023    0.000    0.029    0.000 env.py:65(add)
     9800    0.022    0.000    0.092    0.000 std.py:358(_dot)
    70000    0.019    0.000    0.019    0.000 {method 'pop' of 'list' objects}
     4400    0.019    0.000    0.050    0.000 std.py:46(_def)
9000/6200    0.018    0.000    0.041    0.000 std.py:395(quote_interp)
      400    0.018    0.000    0.021    0.000 {method 'read' of '_io.TextIOWrapper' objects}
    21200    0.017    0.000    0.020    0.000 type.py:47(__iter__)
    47000    0.015    0.000    0.057    0.000 env.py:38(clean)
     7400    0.013    0.000    0.014    0.000 std.py:220(_ge)
     7400    0.012    0.000    0.013    0.000 std.py:212(_lt)
12400/10800    0.011    0.000    0.017    0.000 type.py:161(__del__)
     5600    0.009    0.000    0.013    0.000 type.py:69(__add__)
     9000    0.009    0.000    0.041    0.000 std.py:70(_fn)
     1800    0.007    0.000    0.069    0.000 std.py:135(_set)
     1400    0.007    0.000    0.015    0.000 interp.py:28(parse_string)
     2800    0.007    0.000    0.012    0.000 std.py:371(_split)
     6200    0.007    0.000    0.025    0.000 {built-in method _functools.reduce}
     7400    0.006    0.000    0.008    0.000 type.py:73(append)
    20400    0.005    0.000    0.005    0.000 type.py:43(__init__)
     2000    0.005    0.000    0.006    0.000 env.py:15(set)
     6200    0.004    0.000    0.017    0.000 std.py:178(<lambda>)
     7600    0.004    0.000    0.004    0.000 std.py:196(_eq)
     5800    0.004    0.000    0.005    0.000 type.py:63(__len__)
     9800    0.004    0.000    0.004    0.000 {built-in method builtins.getattr}
     6200    0.004    0.000    0.044    0.000 std.py:390(_quote)
     5600    0.004    0.000    0.004    0.000 type.py:55(__getitem__)
     9400    0.003    0.000    0.004    0.000 type.py:35(is_func)
     8800    0.003    0.000    0.004    0.000 type.py:32(is_quote)
      400    0.003    0.000    0.003    0.000 {built-in method _codecs.utf_8_decode}
      200    0.002    0.000    0.169    0.001 std.py:116(_while)
     3200    0.002    0.000    0.024    0.000 std.py:176(_add)
     2200    0.002    0.000    0.002    0.000 interp.py:51(__init__)
      200    0.002    0.000    0.002    0.000 type.py:45(__repr__)
      400    0.001    0.000    0.004    0.000 codecs.py:318(decode)
     2000    0.001    0.000    0.003    0.000 std.py:184(_mul)
        1    0.001    0.001    5.485    5.485 test.py:9(<listcomp>)
      400    0.001    0.000    0.001    0.000 codecs.py:308(__init__)
     1000    0.001    0.000    0.002    0.000 std.py:180(_sub)
     3800    0.001    0.000    0.001    0.000 {method 'extend' of 'list' objects}
     2000    0.001    0.000    0.001    0.000 std.py:186(<lambda>)
      400    0.001    0.000    0.039    0.000 std.py:292(_eval)
      600    0.000    0.000    0.000    0.000 std.py:259(_shr)
     2400    0.000    0.000    0.000    0.000 std.py:266(_printf)
      200    0.000    0.000    0.024    0.000 type.py:211(__call__)
      600    0.000    0.000    0.000    0.000 std.py:241(_bitand)
      800    0.000    0.000    0.000    0.000 std.py:236(_neq)
      200    0.000    0.000    0.000    0.000 type.py:203(__init__)
     2200    0.000    0.000    0.000    0.000 interp.py:55(__iter__)
      200    0.000    0.000    0.001    0.000 std.py:75(_lazy)
      400    0.000    0.000    0.000    0.000 codecs.py:259(__init__)
      200    0.000    0.000    0.004    0.000 std.py:157(_apply)
     1000    0.000    0.000    0.000    0.000 std.py:182(<lambda>)
      200    0.000    0.000    0.000    0.000 type.py:216(__del__)
        1    0.000    0.000    5.486    5.486 <string>:1(<module>)
        1    0.000    0.000    5.486    5.486 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 __init__.py:71(search_function)
        1    0.000    0.000    0.000    0.000 codecs.py:93(__new__)
        1    0.000    0.000    0.000    0.000 __init__.py:43(normalize_encoding)
        1    0.000    0.000    0.000    0.000 utf_8.py:33(getregentry)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.__import__}
        1    0.000    0.000    5.485    5.485 test.py:9(<lambda>)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:989(_handle_fromlist)
        2    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        4    0.000    0.000    0.000    0.000 {method 'isalnum' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {built-in method __new__ of type object at 0x000000006F4D3430}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
46
"""