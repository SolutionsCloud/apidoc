from apidoc.object.source_raw import ObjectObject, ObjectArray, ObjectNumber, ObjectString, ObjectBool, ObjectReference, ObjectType, ObjectNone, ObjectDynamic, ObjectConst

from apidoc.factory.source.element import Element as ElementFactory

from apidoc.lib.util.cast import to_bool


class Object(ElementFactory):
    """ Object Factory
    """

    def create_from_name_and_dictionary(self, name, datas):
        """Return a populated object Object from dictionary datas
        """
        if "type" not in datas:
            raise ValueError("Missing type in object \"%s\"  \"%s\"." % (name, repr(datas)))

        str_type = str(datas["type"]).lower()
        if not str_type in ObjectObject.Types:
            type = ObjectObject.Types("type")
        else:
            type = ObjectObject.Types(str_type)

        if type is ObjectObject.Types.object:
            object = ObjectObject()
            object.properties = self.create_dictionary_of_element_from_dictionary("properties", datas)
        elif type is ObjectObject.Types.array:
            object = ObjectArray()
            if "items" in datas:
                object.items = self.create_from_name_and_dictionary("items", datas["items"])
            if "sample_count" in datas:
                object.sample_count = int(datas["sample_count"])
        elif type is ObjectObject.Types.number:
            object = ObjectNumber()
        elif type is ObjectObject.Types.string:
            object = ObjectString()
        elif type is ObjectObject.Types.bool:
            object = ObjectBool()
            if "sample" in datas:
                object.sample = to_bool(datas["sample"])
        elif type is ObjectObject.Types.reference:
            object = ObjectReference()
            if "reference" in datas:
                object.reference_name = str(datas["reference"])
        elif type is ObjectObject.Types.type:
            object = ObjectType()
            object.type_name = str(datas["type"])
        elif type is ObjectObject.Types.none:
            object = ObjectNone()
        elif type is ObjectObject.Types.dynamic:
            object = ObjectDynamic()
            if "items" in datas:
                object.items = str(datas["items"])
            if "sample" in datas:
                if isinstance(datas["sample"], dict):
                    object.sample = {}
                    for k, v in datas["sample"].items():
                        object.sample[str(k)] = str(v)
                else:
                    raise ValueError("A dictionnary is expected for dynamic\s object in \"%s\"" % name)
        elif type is ObjectObject.Types.const:
            object = ObjectConst()
            if "const_type" in datas:
                const_type = str(datas["const_type"])
                if not const_type in ObjectConst.Types:
                    raise ValueError("Const type \"%s\" unknwon" % const_type)
            else:
                const_type = ObjectConst.Types.string
            object.const_type = const_type
            if not "value" in datas:
                raise ValueError("Missing const value")
            object.value = datas["value"]

        self.set_common_datas(object, name, datas)
        object.type = type

        if "optional" in datas:
            object.optional = to_bool(datas["optional"])
        if "required" in datas:
            object.required = to_bool(datas["required"])

        return object
