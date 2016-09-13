import logging
import unittest

from rampage.sequence import Sequence, Step

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

class TestSequence(unittest.TestCase):
    def setUp(self):
        self.fail_3_times_count = 0

    def succeed_always(self, x, y='y'):
        LOG.info('succeed_always with x=%s, y=%s', x, y)
        return True

    def fail_always(self, x, y='y'):
        LOG.info('fail_always with x=%s, y=%s', x, y)
        raise RuntimeError('fail_always failed')

    def fail_3_times_then_succeed(self, x, y='y'):
        LOG.info('fail_3_times_then_succeed with x=%s, y=%s', x, y)
        if self.fail_3_times_count >= 3:
            return True
        else:
            self.fail_3_times_count += 1
            raise RuntimeError('fail_3_times_then_succeed failed %d times' %
                               self.fail_3_times_count)

    def test_all_success(self):
        seq = Sequence(1)
        seq.add_step(Step(self.succeed_always, 'xvalue1', y='yvalue1'))
        seq.add_step(Step(self.succeed_always, 'xvalue2', y='yvalue2'))
        seq.add_step(Step(self.succeed_always, 'xvalue3', y='yvalue3'))
        while not seq.is_complete():
            seq.run_step()

        self.assertEqual([True, True, True], [s.result for s in seq.steps])

    def test_second_fails(self):
        seq = Sequence(3)
        seq.add_step(Step(self.succeed_always, 'xvalue1', y='yvalue1'))
        seq.add_step(Step(self.fail_always, 'xvalue2', y='yvalue2'))
        seq.add_step(Step(self.succeed_always, 'xvalue3', y='yvalue3'))

        # first step succeeds
        seq.run_step()

        # second step fails
        seq.run_step()
        self.assertTrue(seq.steps[seq.curr_step].errors)
        
        # two retries
        seq.run_step()
        seq.run_step()

        # finally give up after 3 attempts
        with self.assertRaises(RuntimeError):
            seq.run_step()

    def test_second_fails_but_recovers(self):
        seq = Sequence(4)
        seq.add_step(Step(self.succeed_always, 'xvalue1', y='yvalue1'))
        seq.add_step(Step(self.fail_3_times_then_succeed, 'xvalue2',
                          y='yvalue2'))
        seq.add_step(Step(self.succeed_always, 'xvalue3', y='yvalue3'))
        
        # first step succeeds
        seq.run_step()

        # second step fails 3 times
        for i in xrange(1, 4):
            seq.run_step()
            num_errors = len(seq.steps[seq.curr_step].errors)
            self.assertEquals(i, num_errors)
       
        # still on step 1 (of 0,1,2), but this time we succeed
        self.assertEquals(1, seq.curr_step)
        seq.run_step()
        self.assertEqual([True, True, None], seq.all_results())

        # finish up
        seq.run_step()
        self.assertEqual([True, True, True], seq.all_results())

        self.assertEqual([0, 3, 0], [len(errors) for errors in seq.all_errors()])
