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


SCREENSHOTMASK = "scr-{name}.png"


class PywinautoTestCase0(unittest.TestCase):

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
            test_failures = [failure for failure in self._result.failures
                             if failure[0].test == self]
            test_errors = [error for error in self._result.errors
                           if error[0].test == self]
        else:
            test_failures = [failure for failure in self._result.failures
                             if failure[0] == self]
            test_errors = [error for error in self._result.errors
                           if error[0] == self]

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
        return super(PywinautoTestCase, self).run(result)

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


class PywinautoTestCase2(unittest.TestCase):

    def __getattribute__(self, item):
        print(item)
        try:
            return super(PywinautoTestCase2, self).__getattribute__(item)
        except Exception as e:
            print('!!!exception %s' % type(e))
            raise


def screenshot_on_fail(cls):
    def creation(*args, **kwargs):
        instance = cls(*args, **kwargs)

        print(instance._testMethodName)

        return instance
    return creation


class PywinautoTestCase(unittest.TestCase):


    def _proxify(self, method_name):
        original = getattr(self, method_name)

        def proxy(*args, **kwargs):
            try:
                original_return = original(*args, **kwargs)
            except:
                if self._testMethodName == method_name:
                    # test body
                    name = method_name
                else:
                    name = "{test_name}_{method_name}".format(test_name=self._testMethodName,
                                                              method_name=method_name)
                if ImageGrab:
                    ImageGrab.grab().save(SCREENSHOTMASK.format(name=name), "PNG")
                raise
            else:
                return original_return

        setattr(self, method_name, proxy)

    def __init__(self, *args, **kwargs):
        super(PywinautoTestCase, self).__init__(*args, **kwargs)

        self._proxify(self._testMethodName)
        self._proxify('setUp')
        self._proxify('tearDown')



