# GUI Application automation and testing library
# Copyright (C) 2015 Intel Corporation
# Copyright (C) 2012 Michael Herrmann
# Copyright (C) 2010 Mark Mc Mahon
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place,
#    Suite 330,
#    Boston, MA 02111-1307 USA

"""pywinauto base test class"""


import unittest
try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

try:
    import nose
except ImportError:
    nose = None


SCREENSHOTMASK = "scr-{name}.jpg"


class PywinautoTestCases(unittest.TestCase):

    """
    Base class for pywinauto testing.
    Hold common setUp/tearDown actions for all the tests.
    """

    @property
    def _test_successful(self):

        """
        True if the test passed successfully.
        """
        if not hasattr(self, '_result'):
            return None

        if nose and isinstance(self._result, nose.proxy.ResultProxy):
            test_failures = filter(lambda i: i[0].test == self, self._result.failures)
            test_errors = filter(lambda i: i[0].test == self, self._result.errors)
        else:
            test_failures = filter(lambda i: i[0] == self, self._result.failures)
            test_errors = filter(lambda i: i[0] == self, self._result.errors)
        # test_expected_failures = filter(lambda i: i[0] == self,
        #                                self.__result.expectedFailures)
        # test_unexpected_successes = filter(lambda i: i == self,
        #                                    self.__result.unexpectedSuccesses)

        # if test_failures or test_errors or test_expected_failures or test_unexpected_successes:
        if test_failures or test_errors:
            return False
        else:
            return True

    @staticmethod
    def save_screenshot(name):

        """
        Save full screen image.
        """

        if ImageGrab:
            ImageGrab.grab().save(SCREENSHOTMASK.format(name=name), "JPEG")
        else:
            with open('ImageGrab'+name, 'w'):
                pass

    def run(self, result=None):

        """
        Grab the test case result object, to make possible check a test status
        in setUp/tearDown methods.
        """

        if result is not None:
            self._result = result
        return super(PywinautoTestCases, self).run(result)

    def setUp(self):

        """
        Default setUp actions for testing pywinauto.
        Should be explicitly specified in a subclass method via `super`.
        """
        pass

    def tearDown(self):

        """
        Default tearDown actions for testing pywinauto.
        Should be explicitly specified in a subclass method via `super`.
        To make the screen shots more helpful, use the `super` before the
        clearing actions.
        """

        if not self._test_successful:
            self.save_screenshot(self._testMethodName)
        else:
            with open('successful'+self._testMethodName, 'w'):
                pass
