import os
import json
import yaml


class Parser():

    """Provide tools to parse files
    """
    def load_from_file(self, file_path, format=None):
        """Return dict from a file config
        """
        if format is None:
            base_name, file_extension = os.path.splitext(file_path)
            if file_extension in (".yaml", ".yml"):
                format = "yaml"
            elif file_extension in (".json"):
                format = "json"
            else:
                raise ValueError("Config file \"%s\" undetermined" % file_extension)

        if format == "yaml":
            return yaml.load(open(file_path), Loader=yaml.CSafeLoader if yaml.__with_libyaml__ else yaml.SafeLoader)
        elif format == "json":
            return json.load(open(file_path))
        else:
            raise ValueError("Format \"%s\" unknwon" % format)

    def load_all_from_directory(self, directory_path):
        """Return a list of dict from a directory containing files
        """
        datas = []
        for root, folders, files in os.walk(directory_path):
            for f in files:
                datas.append(self.load_from_file(os.path.join(root, f)))

        return datas
