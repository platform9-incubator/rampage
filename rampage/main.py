import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format=('%(asctime)s %(name)-12s ' +
                            '%(levelname)-8s %(message)s'),
                    datefmt='%m-%d %H:%M')

from rampage.sequences.simple_vm import SimpleVmSequence

def main():
    seq = SimpleVmSequence(5)
    while not seq.is_complete():
        seq.run_step()

if __name__ == '__main__':
    sys.exit(main())
