
import logging
import multiprocessing


class ProcessManager(object):
    def __init__(self):
        self._jobs = {}

    def add_job(self, tag, func):
        """Add job to list of jobs in ProcessManger

        Parameters
        ----------
        tag: str
            Must be unique name for the job
        func: callable
            Function that will be executed
        """

        if self._jobs.get(tag, None):
            raise Exception('Job with such tag already exists')

        self._jobs[tag] = {
            'func': func,
            'process': None
        }

        logging.info('Added new job. Tag: %s; function name: %s',
                     tag, func.__name__)

        return self._jobs[tag]

    def execute_job(self, tag, args=(), kwargs={}):
        """Execute job in separate process

        Parameters
        ----------
        tag: str
            Unique tag of job
        args: tuple of any
            Positional arguments for func
        kwargs: dict of any
            Keyworded args for func
        """

        job = self._jobs.get(tag, None)

        if not job:
            raise Exception('No such job')

        if job['process'] and job['process'].is_alive():
            job['process'].terminate()

        job['process'] = multiprocessing.Process(
            target=job['func'], args=args, kwargs=kwargs)
        job['process'].start()

        logging.info('Executed job: %s', tag)

        return job


if __name__ == '__main__':
    import time

    def x():
        for i in range(0, 10**4):
            print(i)

    pm = ProcessManager()

    pm.add_job('printer', x)
    pm.execute_job('printer')  # start executing job

    time.sleep(2)
    pm.execute_job('printer')  # this will terminate first job and run over
