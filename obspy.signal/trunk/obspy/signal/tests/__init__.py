# -*- coding: utf-8 -*-

from obspy.signal import invsim, trigger, util
from obspy.signal.tests import test_invsim, test_filter, test_rotate, \
    test_trigger, test_util, test_cpxtrace
import doctest
import unittest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_invsim.suite())
    try:
        suite.addTest(doctest.DocTestSuite(invsim))
        suite.addTest(doctest.DocTestSuite(trigger))
        suite.addTest(doctest.DocTestSuite(util))
    except:
        pass
    suite.addTest(test_filter.suite())
    suite.addTest(test_rotate.suite())
    suite.addTest(test_trigger.suite())
    suite.addTest(test_util.suite())
    suite.addTest(test_cpxtrace.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
