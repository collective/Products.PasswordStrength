# -*- coding: utf-8 -*-
from Products import PasswordStrength

import os
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestNamespace(unittest.TestCase):

    def test_pep420_sibling_not_hidden(self):
        """A PEP 420 portion of the namespace imports when this package comes first on sys.path."""
        src = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(PasswordStrength.__file__))))
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        os.mkdir(os.path.join(tmp, "Products"))
        open(os.path.join(tmp, "Products", "pep420_sibling.py"), "w").close()
        if sys.version_info[0] < 3:  # Python 2 has no PEP 420: its portions need an __init__
            open(os.path.join(tmp, "Products", "__init__.py"), "w").close()
        code = "import sys; sys.path[:0] = [%r, %r]; import Products.pep420_sibling" % (src, tmp)
        subprocess.check_call([sys.executable, "-S", "-c", code])
