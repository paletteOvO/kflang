import cProfile

import env
import interp
import std
import type

e = env.Env()
tmp = lambda: [interp.interp0(["load", type.String("test.kf")], e, None) for i in range(0, 100)]
cProfile.run("tmp()", sort="tottime")
print(len(e.env))
"Enabled GC"
"""
PS C:\manhong\WorkSpace\Project\interp> .\test.py
         4280626 function calls (3644726 primitive calls) in 7.529 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
204300/100    1.596    0.000    7.502    0.075 interp.py:138(interp0)
      100    0.632    0.006    1.432    0.014 interp.py:24(parser)
57400/100    0.562    0.000    7.498    0.075 func.py:72(__call__)
    48000    0.553    0.000    0.704    0.000 interp.py:8(value_parser)
   105500    0.537    0.000    0.537    0.000 env.py:7(get)
229400/41100    0.467    0.000    0.467    0.000 env.py:70(clean)
17300/3700    0.432    0.000    4.413    0.001 func.py:14(__call__)
  1219002    0.398    0.000    0.398    0.000 {built-in method builtins.isinstance}
   139000    0.334    0.000    0.334    0.000 env.py:56(__init__)
183800/20400    0.296    0.000    0.296    0.000 env.py:85(cleanClosureGC)
   211000    0.149    0.000    0.234    0.000 type.py:36(is_lazy)
   289200    0.145    0.000    0.193    0.000 env.py:61(extend)
   436104    0.139    0.000    0.139    0.000 {method 'append' of 'list' objects}
   175900    0.118    0.000    0.166    0.000 type.py:24(is_string)
   217200    0.091    0.000    0.172    0.000 type.py:27(is_quote)
    24000    0.085    0.000    0.085    0.000 env.py:27(define)
5600/2200    0.081    0.000    5.454    0.002 std.py:10(_do)
     3000    0.066    0.000    1.113    0.000 std.py:321(_filter)
    96000    0.066    0.000    0.066    0.000 {method 'startswith' of 'str' objects}
    20400    0.065    0.000    0.361    0.000 env.py:42(cleanClosure)
    48000    0.056    0.000    0.072    0.000 type.py:30(is_quote_by)
      100    0.050    0.000    7.490    0.075 std.py:145(_load)
     4300    0.042    0.000    0.092    0.000 std.py:336(_dot)
4300/4100    0.041    0.000    0.219    0.000 interp.py:171(quote_interp)
      100    0.038    0.000    0.039    0.000 {built-in method io.open}
   175500    0.038    0.000    0.038    0.000 type.py:21(is_none)
   129700    0.036    0.000    0.036    0.000 {built-in method builtins.len}
 1900/400    0.033    0.000    3.032    0.008 std.py:81(_let)
    41800    0.031    0.000    0.497    0.000 env.py:38(clean)
 4800/800    0.029    0.000    3.843    0.005 std.py:64(_if)
     3000    0.029    0.000    0.339    0.000 std.py:119(_set)
     2600    0.026    0.000    0.273    0.000 std.py:34(_def)
      100    0.026    0.000    0.027    0.000 {method 'read' of '_io.TextIOWrapper' objects}
        1    0.026    0.026    7.529    7.529 <string>:1(<module>)
     3700    0.023    0.000    0.023    0.000 std.py:192(_lt)
     3700    0.023    0.000    0.024    0.000 std.py:200(_ge)
     7000    0.020    0.000    0.042    0.000 std.py:54(_fn)
    19800    0.018    0.000    0.024    0.000 env.py:66(add)
    17300    0.018    0.000    0.021    0.000 type.py:33(is_func)
     7500    0.016    0.000    0.024    0.000 func.py:5(__init__)
     8100    0.015    0.000    0.022    0.000 {built-in method _functools.reduce}
    48001    0.013    0.000    0.013    0.000 {method 'join' of 'str' objects}
    27500    0.010    0.000    0.010    0.000 {method 'pop' of 'list' objects}
      200    0.008    0.000    0.789    0.004 std.py:100(_while)
     3000    0.007    0.000    0.007    0.000 env.py:14(set)
     1400    0.006    0.000    0.008    0.000 std.py:349(_split)
     4400    0.006    0.000    0.018    0.000 std.py:156(_add)
     1100    0.005    0.000    0.006    0.000 std.py:184(_gt)
     6900    0.004    0.000    0.004    0.000 std.py:158(<lambda>)
     4900    0.003    0.000    0.003    0.000 std.py:176(_eq)
     4300    0.003    0.000    0.003    0.000 {built-in method builtins.getattr}
     2000    0.002    0.000    0.002    0.000 std.py:162(<lambda>)
     2000    0.002    0.000    0.007    0.000 std.py:160(_sub)
     1400    0.001    0.000    0.001    0.000 {method '__getitem__' of 'list' objects}
     2000    0.001    0.000    0.002    0.000 env.py:81(addClosureGC)
     1500    0.001    0.000    0.006    0.000 std.py:164(_mul)
      300    0.001    0.000    0.045    0.000 std.py:272(_eval)
      100    0.001    0.000    0.044    0.000 std.py:308(_reduce)
      100    0.001    0.000    0.037    0.000 std.py:295(_map)
        1    0.001    0.001    7.503    7.503 test.py:7(<listcomp>)
     1500    0.001    0.000    0.001    0.000 std.py:166(<lambda>)
      100    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
      100    0.000    0.000    0.001    0.000 codecs.py:318(decode)
      400    0.000    0.000    0.000    0.000 std.py:239(_shr)
      200    0.000    0.000    0.006    0.000 std.py:138(_apply)
      300    0.000    0.000    0.000    0.000 std.py:221(_bitand)
      100    0.000    0.000    0.000    0.000 codecs.py:308(__init__)
      400    0.000    0.000    0.000    0.000 std.py:216(_neq)
      100    0.000    0.000    0.001    0.000 func.py:103(__call__)
      200    0.000    0.000    0.001    0.000 std.py:172(_mod)
      100    0.000    0.000    0.000    0.000 codecs.py:259(__init__)
      100    0.000    0.000    0.000    0.000 std.py:59(_lazy)
      100    0.000    0.000    0.000    0.000 std.py:233(_shl)
      100    0.000    0.000    0.000    0.000 func.py:94(__init__)
      200    0.000    0.000    0.000    0.000 std.py:174(<lambda>)
1242
"""

"Disabled GC"
"""
PS C:\manhong\WorkSpace\Project\interp> .\test.py
         4280626 function calls (3644726 primitive calls) in 7.166 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
204300/100    1.620    0.000    7.134    0.071 interp.py:138(interp0)
   105500    0.569    0.000    0.569    0.000 env.py:7(get)
      100    0.526    0.005    1.200    0.012 interp.py:24(parser)
183800/20400    0.451    0.000    0.451    0.000 env.py:86(cleanClosureGC)
    48000    0.445    0.000    0.558    0.000 interp.py:8(value_parser)
17300/3700    0.395    0.000    4.650    0.001 func.py:14(__call__)
  1219002    0.371    0.000    0.371    0.000 {built-in method builtins.isinstance}
229400/41100    0.363    0.000    0.363    0.000 env.py:70(clean)
57400/100    0.354    0.000    7.130    0.071 func.py:72(__call__)
   139000    0.323    0.000    0.323    0.000 env.py:56(__init__)
   175900    0.167    0.000    0.216    0.000 type.py:24(is_string)
   211000    0.158    0.000    0.252    0.000 type.py:36(is_lazy)
   217200    0.140    0.000    0.192    0.000 type.py:27(is_quote)
   289200    0.133    0.000    0.168    0.000 env.py:61(extend)
   436104    0.098    0.000    0.098    0.000 {method 'append' of 'list' objects}
5600/2200    0.080    0.000    5.338    0.002 std.py:10(_do)
     3000    0.069    0.000    1.022    0.000 std.py:321(_filter)
   129700    0.069    0.000    0.069    0.000 {built-in method builtins.len}
 4800/800    0.059    0.000    3.915    0.005 std.py:64(_if)
   175500    0.052    0.000    0.052    0.000 type.py:21(is_none)
    24000    0.047    0.000    0.047    0.000 env.py:27(define)
      100    0.044    0.000    0.045    0.000 {built-in method io.open}
    48000    0.043    0.000    0.054    0.000 type.py:30(is_quote_by)
      100    0.042    0.000    7.129    0.071 std.py:145(_load)
4300/4100    0.040    0.000    0.262    0.000 interp.py:171(quote_interp)
    41800    0.039    0.000    0.402    0.000 env.py:38(clean)
 1900/400    0.037    0.000    2.926    0.007 std.py:81(_let)
    96000    0.037    0.000    0.037    0.000 {method 'startswith' of 'str' objects}
     2600    0.032    0.000    0.099    0.000 std.py:34(_def)
        1    0.031    0.031    7.166    7.166 <string>:1(<module>)
      200    0.030    0.000    0.632    0.003 std.py:100(_while)
     8100    0.030    0.000    0.037    0.000 {built-in method _functools.reduce}
    48001    0.022    0.000    0.022    0.000 {method 'join' of 'str' objects}
     3700    0.022    0.000    0.022    0.000 std.py:200(_ge)
    27500    0.021    0.000    0.021    0.000 {method 'pop' of 'list' objects}
     4300    0.018    0.000    0.088    0.000 std.py:336(_dot)
     3000    0.018    0.000    0.271    0.000 std.py:119(_set)
    20400    0.016    0.000    0.467    0.000 env.py:42(cleanClosure)
     3000    0.016    0.000    0.016    0.000 env.py:14(set)
    19800    0.015    0.000    0.018    0.000 env.py:66(add)
    17300    0.015    0.000    0.020    0.000 type.py:33(is_func)
      100    0.015    0.000    0.016    0.000 {method 'read' of '_io.TextIOWrapper' objects}
     1400    0.013    0.000    0.022    0.000 std.py:349(_split)
     3700    0.012    0.000    0.013    0.000 std.py:192(_lt)
     7000    0.011    0.000    0.022    0.000 std.py:54(_fn)
     7500    0.010    0.000    0.013    0.000 func.py:5(__init__)
      100    0.009    0.000    0.040    0.000 std.py:295(_map)
     4900    0.007    0.000    0.007    0.000 std.py:176(_eq)
     4300    0.006    0.000    0.006    0.000 {built-in method builtins.getattr}
     4400    0.005    0.000    0.028    0.000 std.py:156(_add)
     1100    0.004    0.000    0.009    0.000 std.py:184(_gt)
     2000    0.004    0.000    0.004    0.000 std.py:162(<lambda>)
     6900    0.002    0.000    0.002    0.000 std.py:158(<lambda>)
     2000    0.002    0.000    0.010    0.000 std.py:160(_sub)
     1500    0.001    0.000    0.003    0.000 std.py:164(_mul)
      100    0.001    0.000    0.051    0.001 std.py:308(_reduce)
      300    0.001    0.000    0.022    0.000 std.py:272(_eval)
        1    0.001    0.001    7.135    7.135 test.py:7(<listcomp>)
     2000    0.001    0.000    0.001    0.000 env.py:82(addClosureGC)
     1500    0.001    0.000    0.001    0.000 std.py:166(<lambda>)
      100    0.001    0.000    0.001    0.000 {built-in method _codecs.utf_8_decode}
      100    0.000    0.000    0.001    0.000 codecs.py:318(decode)
      400    0.000    0.000    0.000    0.000 std.py:239(_shr)
      200    0.000    0.000    0.004    0.000 std.py:138(_apply)
     1400    0.000    0.000    0.000    0.000 {method '__getitem__' of 'list' objects}
      400    0.000    0.000    0.000    0.000 std.py:216(_neq)
      300    0.000    0.000    0.000    0.000 std.py:221(_bitand)
      100    0.000    0.000    0.000    0.000 codecs.py:308(__init__)
      100    0.000    0.000    0.000    0.000 std.py:59(_lazy)
      100    0.000    0.000    0.001    0.000 func.py:103(__call__)
      200    0.000    0.000    0.005    0.000 std.py:172(_mod)
      100    0.000    0.000    0.000    0.000 func.py:94(__init__)
      200    0.000    0.000    0.000    0.000 std.py:174(<lambda>)
      100    0.000    0.000    0.000    0.000 std.py:233(_shl)
      100    0.000    0.000    0.000    0.000 codecs.py:259(__init__)
24042
"""
