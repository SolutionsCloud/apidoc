import tempfile
import shutil


def before_all(context):
    context.temp_dir = tempfile.mkdtemp()


def after_all(context):
    shutil.rmtree(context.temp_dir)


def before_scenario(context, scenario):
    context.conf_files = []
