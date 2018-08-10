from __future__ import absolute_import, unicode_literals
from celery import shared_task
import subprocess

@shared_task()
def run_dock(workdir, project, protocol, receptor_file, ligand_file, center_x, center_y, center_z, sf):
    command = "echo 'y' | DockFlow -p " + project + \
              " --protocol " + protocol + \
              " -r " + receptor_file + \
              " -l " + ligand_file + \
              " --center " + center_x + " " + center_y + " " + center_z + \
              " -sf " + sf
    subprocess.check_call(command, cwd=workdir, shell=True)

@shared_task()
def run_score(project, protocol, receptor_file, ligand_file, center_x, center_y, center_z, sf):
    call(["ScoreFlow", "-h"])
