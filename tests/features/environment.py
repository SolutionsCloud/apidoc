import tempfile
import shutil
from apidoc.object.config import Config


def after_scenario(context, scenario):
    shutil.rmtree(context.temp_dir)


def before_scenario(context, scenario):
    context.temp_dir = tempfile.mkdtemp()
    context.conf_files = []
    context.object_config = Config()
