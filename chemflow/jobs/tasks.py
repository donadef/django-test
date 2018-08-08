from __future__ import absolute_import, unicode_literals
from celery import shared_task
from subprocess import call

@shared_task
def run_job(project, receptor_file, ligand_file, center_x, center_y, center_z, sf='plants', protocol='default'):
    call(["DockFlow", "-h"])

