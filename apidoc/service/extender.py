from copy import deepcopy

from apidoc.service.merger import Merger

from apidoc.lib.util.decorator import add_property
from apidoc.lib.util.cast import to_boolean


@add_property("merger", Merger)
class Extender():

    """Provide tool to managed extentions
    """

    def extends(self, datas, paths, separator="/", extends_key="extends", inherit_key="inherit", removed_key="removed"):
        """Extend a dict with configurations defined in path
        """
        self.datas = deepcopy(datas)
        self.paths = paths
        self.separator = separator
        self.extends_key = extends_key
        self.inherit_key = inherit_key
        self.removed_key = removed_key

        for path in paths:
            self.current_path = path
            self.extend_path(self.datas, path)

        self.datas = self.delete_removed(self.datas)
        self.clean_tags(self.datas)

        return self.datas

    def extend_path(self, datas, path, keys=[]):
        """Extend a dict for a specific path
        """
        (key, dot, next_path) = path.partition(self.separator)

        if key == "":
            self.apply_extends(datas, keys)
            return
        if key == "?":
            for (key_element, element) in datas.items():
                self.extend_path(element, next_path, keys + [key_element])
        elif key not in datas:
            return
        else:
            self.extend_path(datas[key], next_path, keys)

    def apply_extends(self, target, keys):
        """Apply a "extend" property in a dict
        """
        if not isinstance(target, (list, dict)) or self.extends_key not in target or not target[self.extends_key]:
            return

        if not isinstance(target[self.extends_key], list):
            target[self.extends_key] = [target[self.extends_key]]

        while len(target[self.extends_key]) > 0:
            extends_path = target[self.extends_key][0]
            target[self.extends_key].remove(extends_path)
            extends_path_part = extends_path.split(self.separator)
            path = self.get_location_from_keys(keys[0:len(keys) - len(extends_path_part)] + extends_path_part)
            self.merge(target, path, keys)

    def get_location_from_keys(self, keys):
        """Return a location by replacing ? in path by keys
        """
        full_extends_path_buffer = []
        full_extends_path = []
        key_index = 0
        for key in self.current_path.split(self.separator):
            if key == "?":
                full_extends_path += full_extends_path_buffer + [keys[key_index]]
                full_extends_path_buffer = []
                key_index += 1
            else:
                full_extends_path_buffer.append(key)

        return self.separator.join([str(x) for x in full_extends_path])

    def get_keys_from_location(self, location):
        """Return keys from a location
        """
        keys = []
        splited_location = location.split(self.separator)
        key_index = 0
        for key in self.current_path.split(self.separator):
            if key == "?":
                keys.append(splited_location[key_index])
            key_index += 1

        return keys

    def merge(self, target_datas, extend_location, keys):
        """Merge the source datas (located by extend_location) with target_datas
        """
        path = self.get_location_from_keys(keys)

        if extend_location == path:
            raise ValueError("Recucive inclusion in\"%s\"" % extend_location)
        source_datas = self.get_datas(extend_location)
        source_keys = self.get_keys_from_location(extend_location)

        self.apply_extends(source_datas, source_keys)

        self.merger.merge_extends(target_datas, deepcopy(source_datas), self.inherit_key)

    def get_datas(self, extend_location):
        """Retrieve datas from location
        """
        root = self.datas
        for key in extend_location.split(self.separator):
            if key not in root:
                raise ValueError("Unable to find the key \"%s\" in \"%s\"" % (key, extend_location))
            else:
                root = root[key]
        return root

    def delete_removed(self, datas):
        """Delete sub properties flagged as removed
        """
        if isinstance(datas, dict):
            if self.removed_key in datas and to_boolean(datas[self.removed_key]):
                return None

            new_datas = {}
            for key in datas:
                cleaned = self.delete_removed(datas[key])
                if cleaned is not None:
                    new_datas[key] = cleaned

            return new_datas
        elif isinstance(datas, list):
            new_datas = []
            for item in datas:
                cleaned = self.delete_removed(item)
                if cleaned is not None:
                    new_datas.append(cleaned)
            return new_datas
        else:
            return datas

    def clean_tags(self, datas):
        """Remove temporary tags
        """
        if isinstance(datas, dict):
            if self.removed_key in datas:
                del(datas[self.removed_key])
            if self.inherit_key in datas:
                del(datas[self.inherit_key])
            if self.extends_key in datas:
                del(datas[self.extends_key])
            for key in datas:
                self.clean_tags(datas[key])
        elif isinstance(datas, list):
            for item in datas:
                self.clean_tags(item)
