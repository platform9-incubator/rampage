# pylint: disable=broad-except

import logging
import traceback

LOG = logging.getLogger(__name__)

class Step(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.errors = []

    def run(self):
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.errors.append({'exception': e,
                                 'traceback': traceback.format_exc()})
    def latest_error(self):
        return self.errors[-1]

    def __repr__(self):
        return '%s(%s, %s)' % \
               (self.func.__name__,
                ', '.join(self.args),
                ', '.join(['%s=%s' % i for i in self.kwargs.iteritems()]))

class Sequence(object):
    def __init__(self, max_step_failures):
        self.steps = []
        self.curr_step = 0
        self.max_step_failures = max_step_failures

    def add_step(self, step):
        self.steps.append(step)

    def run_step(self):
        step = self.steps[self.curr_step]
        if len(step.errors) >= self.max_step_failures:
            raise RuntimeError('Step %s failed %s times' % (step,
                               self.max_step_failures))
        step.run()
        if step.result:
            LOG.info('Completed step %s', step)
            self.curr_step += 1
        else:
            LOG.info('Step %s failed %d times so far', step, len(step.errors))

    def is_complete(self):
        return self.curr_step >= len(self.steps)

    def all_errors(self):
        return [s.errors for s in self.steps]
    
    def all_results(self):
        return [s.result for s in self.steps]
