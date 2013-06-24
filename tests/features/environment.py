import tempfile
import shutil
from apidoc.object.config import Config


def before_all(context):
    context.temp_dir = tempfile.mkdtemp()


def after_all(context):
    shutil.rmtree(context.temp_dir)


def before_scenario(context, scenario):
    context.conf_files = []
    context.object_config = Config()
