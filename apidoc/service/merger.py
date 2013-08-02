from apidoc.lib.util.cast import to_boolean


class Merger():

    """Provide tool to merge elements
    """

    def merge_extends(self, target, extends, inherit_key="inherit", inherit=False):
        """Merge extended dicts
        """
        if isinstance(target, dict):
            if inherit and inherit_key in target and not to_boolean(target[inherit_key]):
                return
            if not isinstance(extends, dict):
                raise ValueError("Unable to merge: Dictionnary expected")
            for key in extends:
                if key not in target:
                    target[str(key)] = extends[key]
                else:
                    self.merge_extends(target[key], extends[key], inherit_key, True)
        elif isinstance(target, list):
            if not isinstance(extends, list):
                raise ValueError("Unable to merge: List expected")
            target += extends

    def merge_sources(self, datas):
        """Merge sources files
        """
        datas = [data for data in datas if data is not None]

        if len(datas) == 0:
            raise ValueError("Data missing")

        if len(datas) == 1:
            return datas[0]

        if isinstance(datas[0], list):
            if len([x for x in datas if not isinstance(x, list)]) > 0:
                raise TypeError("Unable to merge: List expected")
            base = []
            for x in datas:
                base = base + x
            return base

        if isinstance(datas[0], dict):
            if len([x for x in datas if not isinstance(x, dict)]) > 0:
                raise TypeError("Unable to merge: Dictionnary expected")
            result = {}
            for element in datas:
                for key in element:
                    if key in result:
                        result[key] = self.merge_sources([result[key], element[key]])
                    else:
                        result[key] = element[key]
            return result

        if len([x for x in datas if isinstance(x, (dict, list))]) > 0:
            raise TypeError("Unable to merge: List not expected")

        raise ValueError("Unable to merge: Conflict")

    def merge_configs(self, config, datas):
        """Merge configs files
        """
        if not isinstance(config, dict) or len([x for x in datas if not isinstance(x, dict)]) > 0:
            raise TypeError("Unable to merge: Dictionnary expected")

        for key, value in config.items():
            others = [x[key] for x in datas if key in x]
            if len(others) > 0:
                if isinstance(value, dict):
                    config[key] = self.merge_configs(value, others)
                else:
                    config[key] = others[-1]
        return config
