from __future__ import absolute_import, unicode_literals
from celery import shared_task
import subprocess

from .models import Job


@shared_task()
def run_dock(workdir, project, protocol, receptor_file, ligand_file, center_x, center_y, center_z, sf):
    # job = Job.objects.filter(project_name=project, protocol_name=protocol, state='PENDING')[0]
    # job.state = 'RUNNING'
    # job.save()
    command = "echo 'y' | DockFlow -p " + project + \
              " --protocol " + protocol + \
              " -r " + receptor_file + \
              " -l " + ligand_file + \
              " --center " + center_x + " " + center_y + " " + center_z + \
              " -sf " + sf
    print(command)
    subprocess.check_call(command, cwd=workdir, shell=True)


@shared_task()
def run_score(workdir, project, protocol, receptor_file, ligand_file, center_x, center_y, center_z, sf):
    # job = Job.objects.filter(project_name=project, protocol_name=protocol, state='PENDING')[0]
    # job.state = 'RUNNING'
    # job.save()
    command = "echo 'y' | ScoreFlow -p " + project + \
              " --protocol " + protocol + \
              " -r " + receptor_file + \
              " -l " + ligand_file + \
              " --center " + center_x + " " + center_y + " " + center_z + \
              " -sf " + sf
    subprocess.check_call(command, cwd=workdir, shell=True)


@shared_task()
def postprocess_dock(workdir, project, protocol, receptor_file, ligand_file, center_x, center_y, center_z, sf):
    command = "DockFlow -p " + project + \
              " --protocol " + protocol + \
              " -r " + receptor_file + \
              " -l " + ligand_file + \
              " -sf " + sf + \
              """ --postprocess <<EOF
y
y
EOF
"""
    subprocess.check_call(command, cwd=workdir, shell=True)


@shared_task()
def postprocess_score(workdir, project, protocol, receptor_file, ligand_file, center_x, center_y, center_z, sf):
    command = "ScoreFlow -p " + project + \
              " --protocol " + protocol + \
              " -r " + receptor_file + \
              " -l " + ligand_file + \
              " -sf " + sf + \
              " --postprocess"
    subprocess.check_call(command, cwd=workdir, shell=True)

