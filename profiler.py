import cProfile

import test_interp

cProfile.run("test_interp.starttest()", sort="tottime")
