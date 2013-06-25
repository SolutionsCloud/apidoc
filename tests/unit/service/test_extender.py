import unittest

from apidoc.service.extender import Extender
from apidoc.service.merger import Merger


class TestParser(unittest.TestCase):

    def setUp(self):
        self.extender = Extender()

    def test_merger(self):
        self.assertIsInstance(self.extender.merger, Merger)

        self.extender.merger = "foo"
        self.assertEqual("foo", self.extender.merger)

        self.extender.merger = None
        self.assertIsInstance(self.extender.merger, Merger)

    def test_extends__init(self):
        self.extender.extends({}, [], ":", "e", "i", "r")

        self.assertEqual(":", self.extender.separator)
        self.assertEqual("e", self.extender.extends_key)
        self.assertEqual("i", self.extender.inherit_key)
        self.assertEqual("r", self.extender.removed_key)

    def test_extends__simple_extend(self):
        data = {
            "root": {
                "a": {"att1": 1, "att2": ["A"]},
                "b": {"ex": "a", "att2": ["B"]}
            }
        }

        expected = {
            "root": {
                "a": {"att1": 1, "att2": ["A"]},
                "b": {"att1": 1, "att2": ["B", "A"]}
            }
        }

        response = self.extender.extends(data, ["root.?"], ".", "ex")
        self.assertEqual(expected, response)

    def test_extends__extend_dont_override(self):
        data = {
            "root": {
                "a": {"att1": 1, "att2": 2},
                "b": {"att1": 3, "ex": "a"}
            }
        }

        expected = {
            "root": {
                "a": {"att1": 1, "att2": 2},
                "b": {"att1": 3, "att2": 2}
            }
        }

        response = self.extender.extends(data, ["root.?"], ".", "ex")
        self.assertEqual(expected, response)

    def test_extends__multiple_extend(self):
        data = {
            "root": {
                "a": {"att1": 1},
                "b": {"att2": 2},
                "c": {"ex": ["a", "b"]}
            }
        }

        expected = {
            "root": {
                "a": {"att1": 1},
                "b": {"att2": 2},
                "c": {"att1": 1, "att2": 2},
            }
        }

        response = self.extender.extends(data, ["root.?"], ".", "ex")
        self.assertEqual(expected, response)

    def test_extends__separator(self):
        data = {
            "root": {
                "a": {"att": 1},
                "b": {"ex": "a"}
            }
        }

        expected = {
            "root": {
                "a": {"att": 1},
                "b": {"att": 1}
            }
        }

        response = self.extender.extends(data, ["root:?"], ":", "ex")
        self.assertEqual(expected, response)

    def test_extends__deep(self):
        data = {
            "root": {
                "a": {
                    "sub": {
                        "c": {"att": 1},
                        "d": {"ex": "c"}
                    }
                },
                "b": {}
            }
        }

        expected = {
            "root": {
                "a": {
                    "sub": {
                        "c": {"att": 1},
                        "d": {"att": 1}
                    }
                },
                "b": {}
            }
        }

        response = self.extender.extends(data, ["root.?.sub.?"], ".", "ex")
        self.assertEqual(expected, response)

    def test_extends__deep_defined(self):
        data = {
            "root": {
                "a": {
                    "sub": {
                        "c": {"att": 1},
                        "d": {"ex": "b.c"}
                    }
                },
                "b": {
                    "sub": {
                        "c": {"att": 2},
                    }
                }
            }
        }

        expected = {
            "root": {
                "a": {
                    "sub": {
                        "c": {"att": 1},
                        "d": {"att": 2}
                    }
                },
                "b": {
                    "sub": {
                        "c": {"att": 2},
                    }
                }
            }
        }

        response = self.extender.extends(data, ["root.?.sub.?"], ".", "ex")
        self.assertEqual(expected, response)

    def test_extends__master_defined(self):
        data = {
            "root": {
                "a": {
                    "sub": {
                        "c": {"att": 1},
                        "d": {"ex": "c"},
                        "e": {"ex": "a.c"}
                    }
                },
                "b": {
                    "ex": "a",
                    "sub": {
                        "c": {"att": 2},
                    }
                }
            }
        }

        expected = {
            "root": {
                "a": {
                    "sub": {
                        "c": {"att": 1},
                        "d": {"att": 1},
                        "e": {"att": 1}
                    }
                },
                "b": {
                    "sub": {
                        "c": {"att": 2},
                        "d": {"att": 2},
                        "e": {"att": 1}
                    }
                }
            }
        }

        response = self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex")
        self.assertEqual(expected, response)

    def test_extends__inherit(self):
        data = {
            "root": {
                "a": {
                    "sub1": {"att1": 1},
                    "sub2": {"att2": 2}
                },
                "b": {
                    "ex": "a",
                    "sub2": {"in": "false"}
                }
            }
        }

        expected = {
            "root": {
                "a": {
                    "sub1": {"att1": 1},
                    "sub2": {"att2": 2}
                },
                "b": {
                    "sub1": {"att1": 1},
                    "sub2": {}
                }
            }
        }

        response = self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex", "in")
        self.assertEqual(expected, response)

    def test_extends__removed(self):
        data = {
            "root": {
                "a": {
                    "sub1": {"att1": 1},
                    "sub2": {"att2": 2}
                },
                "b": {
                    "ex": "a",
                    "sub2": {"re": "true"},
                    "sub3": [{"att3": 3, "re": "true"}, {"att3": 4, "re": "false"}]
                }
            }
        }

        expected = {
            "root": {
                "a": {
                    "sub1": {"att1": 1},
                    "sub2": {"att2": 2}
                },
                "b": {
                    "sub1": {"att1": 1},
                    "sub3": [{"att3": 4}]
                }
            }
        }

        response = self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex", "in", "re")
        self.assertEqual(expected, response)

    def test_extends__failed_recurcive(self):
        data = {
            "root": {
                "a": {
                    "ex": "a",
                }
            }
        }

        with self.assertRaises(ValueError):
            self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex")

    def test_extends__recurcive_heritance(self):
        data = {
            "root": {
                "a": {
                    "ex": ["b", "c"],
                    "att1": 1
                },
                "b": {
                    "ex": "a",
                    "att2": 2
                },
                "c": {
                    "att3": 3
                }
            }
        }
        expected = {
            "root": {
                "a": {
                    "att1": 1,
                    "att2": 2,
                    "att3": 3
                },
                "b": {
                    "att1": 1,
                    "att2": 2,
                    "att3": 3
                },
                "c": {
                    "att3": 3
                }
            }
        }

        response = self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex")
        self.assertEqual(expected, response)

    def test_extends__failed_missing(self):
        data = {
            "root": {
                "a": {
                    "ex": "b",
                }
            }
        }

        with self.assertRaises(ValueError):
            self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex")

    def test_extends__failed_format(self):
        data = {
            "root": {
                "a": {
                    "ex": "b",
                    "att": {
                        "sub": 2
                    }
                },
                "b": {
                    "att": 1,
                }
            }
        }

        with self.assertRaises(ValueError):
            self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex")

    def test_extends__failed_format2(self):
        data = {
            "root": {
                "a": {
                    "ex": "b",
                    "att": ["A"]
                },
                "b": {
                    "att": 1,
                }
            }
        }

        with self.assertRaises(ValueError):
            self.extender.extends(data, ["root.?", "root.?.sub.?"], ".", "ex")

    def test_clean_tags(self):
        data = {
            "root": {
                "a": {
                    "ex": ["b", "c"],
                    "att1": 1,
                    "removed": "e"
                },
                "b": {
                    "extends": "c",
                    "ex": "a",
                    "att2": 2
                },
                "c": {
                    "inherit": "d",
                    "att3": 3
                }
            }
        }
        expected = {
            "root": {
                "a": {
                    "ex": ["b", "c"],
                    "att1": 1
                },
                "b": {
                    "ex": "a",
                    "att2": 2
                },
                "c": {
                    "att3": 3
                }
            }
        }

        self.extender.extends({}, [])
        self.extender.clean_tags(data)
        self.assertEqual(expected, data)
