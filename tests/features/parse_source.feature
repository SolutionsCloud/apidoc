Feature: Source config parsing

    Scenario: Parse an empty file
        Given a "yaml" source file containing
            """
            configuration:
              title: a
            """
         when a source_factory load this file
         then the root contains "0" versions
         then the root contains "0" method's categories
         then the root contains "0" type's categories
         then the root contains "0" methods
         then the root contains "0" types

    Scenario: common file with method
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
            """
         when a source_factory load this file
         then the root contains "1" versions
         then the root contains "1" method's categories
         then the root contains "1" methods

    Scenario: Use a default method category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    url: /
            """
         when a source_factory load this file
         then the root contains "1" versions
         then the root contains "1" method's categories
         then the root contains "1" methods

    Scenario: Share the same method category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    category: b
                  c:
                    category: b
            """
         when a source_factory load this file
         then the root contains "1" versions
         then the root contains "1" method's categories
         then the root contains "2" methods

    Scenario: Common file with type
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      b:
                        type: a
                types:
                  a:
                    primary: string
                    category: b
            """
         when a source_factory load this file
         then the root contains "1" versions
         then the root contains "1" type's categories
         then the root contains "1" types

    Scenario: Use default type category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      b:
                        type: a
                types:
                  a:
                    primary: string
                    url: /
            """
         when a source_factory load this file
         then the root contains "1" versions
         then the root contains "1" type's categories
         then the root contains "1" types

    Scenario: Share the same type category
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    request_headers:
                      b:
                        type: a
                      c:
                        type: c
                types:
                  a:
                    primary: string
                    category: b
                  c:
                    primary: string
                    category: b
            """
         when a source_factory load this file
         then the root contains "1" versions
         then the root contains "1" type's categories
         then the root contains "2" types

    Scenario: Ignore unused types
        Given a "yaml" source file containing
            """
            versions:
              v1:
                methods:
                  a:
                    uri: /
                types:
                  a:
                    primary: string
                    category: b
            """
         when a source_factory load this file
         then the root contains "1" versions
         then the root contains "0" type's categories
         then the root contains "0" types

