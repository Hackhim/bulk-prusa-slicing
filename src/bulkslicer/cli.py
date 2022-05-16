import click
import os
import subprocess


class BulkSlicer:
    def __init__(self, stls_path, gcodes_path, ini_path, slicer_path, threads):
        self.stls_path = stls_path
        self.gcodes_path = gcodes_path
        self.ini_path = ini_path
        self.slicer_path = slicer_path
        self.threads = threads

    def launch_slicing(self):
        self.bulk_slice()
        # if self.threads == 1:
        #    self.bulk_slice()
        # else:
        #    self.bulk_slice_threaded()

    def bulk_slice(self):
        stls = self._list_stls(self.stls_path)
        for stl in stls:
            stl_path = os.path.join(self.stls_path, stl)
            self._run_slicer(stl_path)

    # def bulk_slice_threaded(self):
    #    threads = []
    #    stls = self._list_stls(self.stls_path)
    #    for i in range(len(stls)):
    #        pass

    def _list_stls(self, directory):
        return [
            f for f in os.listdir(directory) if f.endswith('.stl')
        ]

    def _run_slicer(self, stl_path):
        proc = [
            self.slicer_path,
            '-g',
            '--output', self.gcodes_path,
            '--load', self.ini_path,
            stl_path
        ]
        subprocess.run(proc)


@click.command()
@click.option('--stls', '-s', 'stls_path', required=True,
              type=click.Path(dir_okay=True, readable=True, resolve_path=True))
@click.option('--gcodes', '-g', 'gcodes_path', required=True,
              type=click.Path(dir_okay=True, readable=True, resolve_path=True))
@click.option('--ini', '-i', 'ini_path', required=True,
              type=click.Path(dir_okay=True, readable=True, resolve_path=True))
@click.option('--slicer', 'slicer_path', envvar='SLICER_PATH', required=True,
              type=click.Path(file_okay=True, readable=True, resolve_path=True))
# @click.option('--threads', '-t', type=click.IntRange(1, 5), default=1)
def bulk_slice_command(stls_path, gcodes_path, ini_path, slicer_path, threads=1):
    bulk_slicer = BulkSlicer(stls_path, gcodes_path,
                             ini_path, slicer_path, threads)
    bulk_slicer.launch_slicing()


def main():
    bulk_slice_command()
