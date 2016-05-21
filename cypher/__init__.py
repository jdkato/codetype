# encoding=utf8
import sys

try:
    reload(sys)
except NameError:
    import imp
    imp.reload(sys)

sys.setdefaultencoding("utf8")
