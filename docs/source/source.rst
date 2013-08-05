.. _source-page:

Source's File Format
====================

ApiDoc uses source file(s) to generate the documentation. The format of the source file can be `YAML` or `JSON`, the extension of the files must be repectively `.yaml` (or `.yml`) or `.json`

This is a basic sample of a config file

.. code-block:: yaml

   configuration:
     title: Hello API
     description: An API dedicated to the hello service
     uri: ${base_url}
   categories:
     Display:
       description: Display messages
     Config:
       description: Configure the application
   versions:
     v1.0:
       methods:
         Hello:
           category: Display
           uri: /
           description: Say hello
           response_body:
             type: string
             sample: Hello
         HelloName:
           category: Display
           uri: /{name}
           request_parameters:
             name:
               type: string
               description: Name of the user
           request_headers:
             Accept:
               type: mimeType
               description: List of accepted MimeTypes
               sample: text/plain
           response_body:
             type: string
             sample: Hello my_name
         ConfigHello:
           category: Config
           uri: /
           method: PUT
           description: Configure the hello method
           request_body:
             type: object
             properties:
               language:
                   type: string
                   sample: "fr"
           response_body:
             type: boolean
       types:
         mimeType:
           item:
             type: string
             sample: application/json
           format:
             pretty: type/sous-type
     v2.O:
       status: beta
       display: false

All elements are optional, but a least one displayable method is required.

configuration
-------------

The `configuration` contains major information of your documentation.

* uri: Common URI of your API (ie: https://api.sfr.com/service/)
* title: The name of your API. It will be displayed in the title tag, and in the header of the documentation
* description: A description of your API. It will be displayed under the title in the header of the documentation

sample:

.. code-block:: yaml

   configuration:
     title: Hello API
     description: An API dedicated to the hello service
     uri: https://api.sfr.com/services/hello

versions
--------

This element contains a dictionary of versions. Each version is associated with a key which is the name of the version. At least one version is required.

* display: Boolean Defining if the version is displayed or not.
* label: The label of the version who will be display in the documentation.
* uri: Completes the URI of the element `configuration`.
* major: Major part of the version number.
* minor: Minor part of the version number.
* status (`current`, `beta`, `deprecated`, `draft`): Status of the version.
* methods: List of methods contained in the version (see :ref:`source-page-methods`).
* types: List of types contained in the version (see :ref:`source-page-types`).
* references: List of references contained in the version (see :ref:`source-page-references`).

sample:

.. code-block:: yaml

   versions:
     v1.0:
       display: true
       label: Version 1
       uri: /v1
       major: 1
       minor: 0
       status: current
       methods:
         ...
     v2.0:
       display: false
       uri: /v2
       major: 2
       minor: 0
       status: beta
       methods:
         ...

categories
----------

This element contains a dictionary of categories; a category is a kind of folder in the rendered documentation. Each category is associated to a key which is the name of the category. This elements is not required. A method (or a type) can have an attribute category which does not exist in this dictionnary. But this element allows you to configure the category by giving a description or a priority order.

* display: Boolean defining if the category is displayed or not
* label: The label of the category who will be display in the documentation
* description: A description of the category. It will be dislayed under the name of the category
* order: A number used to sort the categories and define in which order they will be displayed. Default value is 99. When two categories have the same order, they will be sorted alphabetically by name.

sample:

.. code-block:: yaml

   categories:
     Common:
       display: false
       description: a helper section use for extension
     Version:
       description: List the version of the API
       order: 1
     Authentication:
       label: Authentication + Logout
       description: How to login and logout the client

.. _source-page-methods:

methods
-------

This element contains a dictionary of methods. Each method is associated with a key which is the name of the method. At least one method is required.

* label: The label of the method who will be display in the documentation.
* description: A description of the method. It will be dislayed under the name of the method.
* uri: Endpoint of the method based on the URI found in `configuration` and `version`. Parameters are declared between curly bracket.
* method (`get`, `post`, `put`, `delete`, `head`, `http`): Type of method used in this endpoint (default `get`).
* code: Normal code returned by the method (default `200`). This information will be displayed in the sample generated in the documentation.
* request_parameters: List of parameters sent in the URI of the method (see :ref:`source-page-request_parameters`).
* request_headers: List of parameters sent in the headers of the method (see :ref:`source-page-request_headers`).
* request_body: Request object sent in the body of the method (see :ref:`source-page-request_body`).
* response_codes: List of codes received in the headers of the method (see :ref:`source-page-response_codes`).
* response_body: Response object received in the body of the method (see :ref:`source-page-response_body`).
* category: The name of the category to which the method belongs.

sample:

.. code-block:: console

   methods:
     Hello:
       label: Echo
       uri: /hello-{name}.json
       method: get
       code: 200
       description: Say hello
       request_parameters:
         ...
       request_headers:
         ...
       request_body:
         ...
       response_codes:
         ...
       response_body:
         ...

.. _source-page-request_parameters:

request_parameters
^^^^^^^^^^^^^^^^^^

This element contains a dictionary of query parameters contained in the URI. Each parameter is associated with a key which is the name of the parameter. If a parameter is defined in this elements but is not on the URI, it will not be displayed. This can be usefull when you use extensions. The parameters will be displayed in the same order as they appear in the URI

* type: Type of the parameter (see :ref:`source-page-types`).
* description: A description of the parameter.
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* sample: A sample value which will be displayed in the sample fieldset.
* generic: If true, the parameter will be displayed in an other color. Default False.

sample:

.. code-block:: yaml

   request_parameters:
     name:
       type: string
       description: Name of the user
       optional: false
       sample: John Doe
       generic: false
     language:
       type: string
       description: Language of the response
       optional: true
       sample: fr
       generic: true

.. _source-page-request_headers:

request_headers
^^^^^^^^^^^^^^^

This element contains a dictionary of header parameters expected by the method. Each parameter is associated with a key which is the name of the parameter.

* type: Type of the parameter (see :ref:`source-page-types`).
* description: A description of the parameter.
* optional: A boolean indicated if the parameter is compulsory or optional.
* sample: A sample value which will be displayed in the sample fieldset.
* generic: If true, the parameter will be displayed in an other color. Default False.

sample:

.. code-block:: yaml

   request_headers:
     Accept:
       type: mimeType
       description: List of accepted MimeTypes
       sample: text/plain
       optional: true
       generic: true
     X-Auth-Token:
       type: string
       description: Authentification token

.. _source-page-request_body:

request_body
^^^^^^^^^^^^

This element contains an object which represents the raw content sent in the body of the request (see :ref:`source-page-Objects`).

sample:

.. code-block:: yaml

   request_body
       type: object
       description: Root envelope
       properties:
           login:
               type: string
           password:
               type: string

.. _source-page-response_codes:

response_codes
^^^^^^^^^^^^^^

This element contains a list of reponse codes returned by the method.

* code: The numeric code returned in the response
* message: A message associated to the response. When omitted, the default message associated with the code will be used
* description: A description of the response
* generic: If true, the parameter will be displayed in an other color. Default False

sample:

.. code-block:: yaml

   response_codes:
     - code: 400
       message: Bad name format
       description: The resource name is not correct
     - code: 404
       message: Resource not found
       generic: true

.. _source-page-response_body:

response_body
^^^^^^^^^^^^^

This element contains an object which represents the response received in the body of the response (see :ref:`source-page-Objects`).

sample:

.. code-block:: yaml

   request_body
       type: array
       description: List of users
       items:
           type: object
           properties:
               name:
                   type: string
                   description: Name of the user
               role:
                   type: CustomRole
                   description: Role of the user

.. _source-page-types:

types
-----

This element contains a dictionary of types used by other elements. Each reference is associated with a key which is the name of the type.
When a type is declared but never used, a warning will be fired in the logs and the type will not be displayed.

* category: The name of the category to which the type belongs.
* description: A description of the type.
* item: The content of the type (see :ref:`source-page-Objects`).
* format: Some representations of the type.
    * pretty: A well formated representation of the type.
    * advanced: A technically accurate representation of the type.

sample:

.. code-block:: yaml

   types:
     mimeType:
       category: Common
       description: A mime type
       item:
         type: string
         sample: application/json
       format:
         pretty: type/sous-type
         advanced: [a-z]\/[a-z]
     languages:
       category: Lists
       description: List of supported language
       item:
         type: enum
         values:
         - en
         - fr
         descriptions:
           en:
             description: English
           fr:
             description: Français

.. _source-page-references:

references
----------

This element contains a dictionary of references used by objects. Each reference is associated with a key which is the name of the reference.
The reference is not displayed directly, it is a complex object which could be used in other elements.

sample:

.. code-block:: yaml

   methods:
     listComments:
       ...
       response_body:
         type: array
         items:
           type: reference
           reference: comment
   reference:
     comment:
       type: object
       properties:
         owner:
           type: reference
           reference: user
         message:
           type: string
         date:
           type: string
     user:
       type: object
       name:
         type: string
       language:
         type: string

.. _source-page-Objects:

Objects
-------

In the bodies of types, requests and responses you can define a complex object using basic elements. These elements (defined below) contain always a keyword "type" which defines the type of the element.
The known types, are `object`, `array`, `dynamic`, `boolean`, `none`, `string`, `number`, `integer`, `reference`, `const`, `enum`. If the type is not in this list, ApiDoc will look in the elements declared in the `types` section (see :ref:`source-page-types`).
Each elements contains an attribute `optional` indicating if the element is compulsory or optional. They also contains an attribute `constraints` containing a dictionnary constraints. Some constraints are predefined depending of the type of the element, but it"s also possible to define custom constraints (a reference to yout business model for example). No check will be applied on sample according to these constraints, they only will be display in a popover in the rendered documentation. These constraints are derived from `Json Schema <http://json-schema.org/>`_


String
^^^^^^

The object String defines a string.

* description: A description of the string
* sample: A sample value which will be displayed in the sample fieldset.
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * maxLength: A positive integer is expected.
  * minLength: A positive integer is expected.
  * pattern: A string is expected. It who should be a regular expression, according to the ECMA 262 regular expression dialect.
  * format: A string is expteced. It must be one of the values ​​found in this list (date-time, email, hostname, ipv4, ipv6, uri).
  * enum: An array of string is expected.
  * default: A string is expected.
  * everything else: A string is expected

sample:

.. code-block:: yaml

   name:
       type: string
       description: Name of the user
       sample: John Doe
       constraints:
           minLength: 1
           maxLength: 32

Number
^^^^^^

The object Number defines a numeric value with optionals decimals.

* description: A description of the number
* sample: A sample value which will be displayed in the sample fieldset.
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * multipleOf: A number is expected.
  * maximum: A number is expected.
  * exclusiveMaximum: A boolean is expected.
  * minimum: A number is expected.
  * exclusiveMinimum: A boolean is expected.
  * enum: An array of number is expected.
  * default: A number is expected.
  * everything else: A string is expected

sample:

.. code-block:: yaml

   price:
       type: number
       description: Price in dollars
       sample: 20.3
       constraints:
           maximum: 0
           multipleOf: 0.01

Integer
^^^^^^^

The object Integer defines a numeric value without decimal.

* description: A description of the number
* sample: A sample value which will be displayed in the sample fieldset.
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * multipleOf: A integer is expected.
  * maximum: A integer is expected.
  * exclusiveMaximum: A boolean is expected.
  * minimum: A integer is expected.
  * exclusiveMinimum: A boolean is expected.
  * enum: An array of integer is expected.
  * default: A integer is expected.
  * everything else: A string is expected

sample:

.. code-block:: yaml

   age:
       type: number
       description: Age of the user
       sample: 20
       constraints:
           maximum: 0

Boolean
^^^^^^^

The object Boolean defines a boolean.

* description: A description of the boolean
* sample: A sample value which will be displayed on the sample fieldset.
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * default: A boolean is expected.
  * everything else: A string is expected

sample:

.. code-block:: yaml

   is_default:
       type: boolean
       description: Define if the group is the default group
       sample: false
       constraints:
           default: false

None
^^^^

The object None defines an empty object. Sometime used in a request when a key is compulsory but no value is expected.

* description: A description of the object
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * everything: A string is expected

sample:

.. code-block:: yaml

   reboot:
     type: none
     description: Set this key if you want reboot your server
     constraints:
       compulsory: yes

Const
^^^^^

The object Const defines an constant property. Sometime used in a request like the property "method" in Json-RPC.

* description: A description of the object
* cont_type: A scalar type of the constant (allowed values are `string`, `number`, `integer`, `boolean`). If undefined `string` will be used
* value: The value associated to the property
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * everything: A string is expected

sample:

.. code-block:: yaml

   method:
     type: const
     description: Json-RPC method name
     const_type: string
     value: "find"
     constraints:
        required: authenticated user

Enum
^^^^

The object Enum defines a list a availables values. When this object is the primary object of an type (see :ref:`source-page-types`) the values with there descriptions will be displayedin the Type section.

* description: A description of the object
* values: An array of values
* descriptions: A dictionnary of description for each value
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * everything: A string is expected

sample:

.. code-block:: yaml

   httpMethods:
     type: enum
     description: List of Http methods used in Rest
     values:
     - GET
     - POST
     - PUT
     - DELETE
     descriptions:
       GET: Like select
       POST: Like insert
       PUT: Like update
       DELETE: Like delete
     sample: GET
     constraints:
        required: authenticated user

Object
^^^^^^

The object Object defines a complex object containing a dictionnary of properties. Each property is associated with a key which is the name of the property.

* description: A description of the object
* properties: List of properties of the object
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * maxProperties: A positive integer is expected.
  * minProperties: A positive integer is expected.
  * everything else: A string is expected

sample:

.. code-block:: yaml

   element:
     type: object
     description: User to update
     properties:
       name:
         type: string
         description: New name of the user
     constraints:
        required: authenticated user

Array
^^^^^

The object Array defines an array of objects.

* description: A description of the array
* items: A representation of the items contained in the array
* sample_count: Number of items to display in the sample fieldset
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * maxItems: A positive integer is expected.
  * minItems: A positive integer is expected.
  * uniqueItems: A boolean is expected.
  * everything else: A string is expected

sample:

.. code-block:: yaml

   elements:
     type: array
     description: List of users
     items:
       type: object
       properties:
         name:
           type: string
           description: New name of the user
     constraints:
        maxItems: 10

Reference
^^^^^^^^^

The object Reference defines a reference to a referenced object.
Reference is the only one elements who does not have constraints. This constraints are defined in the refererenced item.

* reference: Name of the reference
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.

sample:

.. code-block:: yaml

   user:
     type: reference
     reference: GenericUser

Dynamic
^^^^^^^

The object Dynamic defines a special object where the key, which must be a string, is dynamic.

* description: A description of the array
* items: A representation of the items contained in the object
* sample: A sample value which will be displayed on the sample fieldset.
* optional: A boolean indicating if the parameter is compulsory or optional. Default False.
* constraints: A dictionary of constraints
  * maxItems: A positive integer is expected.
  * minItems: A positive integer is expected.
  * everything else: A string is expected

sample:

.. code-block:: yaml

   metadatas:
       type: dynamic
       description: A list of key/value to store what you want
       item: string


Customizations
--------------

.. _source-page-variable:

Variables
^^^^^^^^^

Variables can be provided by command line arguments or in the config file (see :ref:`config-page-input`).
Each value of the source file can be (or contain) a variable.


Sample using a variable string context:

.. code-block:: yaml

   configuration:
     title: ${applicationName}
     description: Official documentation of ${applicationName}

Sample using a variable to set a boolean:

.. code-block:: yaml

   categories:
     MyExperiments:
       display: ${displayExperimentals}

Sample using a variable used in extends context:

.. code-block:: yaml

   versions:
     v1:
       ...
     v2:
       extends: ${officialVersion}

Extends
-------

ApiDoc provides a way to simplfy source files writing by using an extends system. You can extend your `versions`, `categories`, `methods`, `types` and `references`.
To extend an element you only have to specify the name of referenced elements with `extends: referenced_name`. The referenced name is always of the same type as your elements (a `version` extends a `version`, a `method` extends a `method`, etc...). If the referenced element is a sibling of the current element, you can just specify its name, if the reference does not belong to the same parent, you must then specify the name of the parent followed by a `/`. For exemple, if your methods A and B belong to different versions you must use `extends: version_of_b/method_b` for method A to extend method B.
Extensions are recursive, but you can break recursion on any element by using `inherit: false` and you can remove an element with `removed: true`.

Sample using an extension on the version:

.. code-block:: yaml

   versions:
     v1:
       ...
     v2:
       extends: v1

Sample using an extension on a method with relative path and absolute path:

.. code-block:: yaml

   versions
     v1:
       methods:
         Request:
           ...
         AuthentificatedRequest:
           extends: Request
     v2:
       methods:
         Login:
           extends: v1/Request

Sample using an extension where the method ListClientWithDetails extends ListClients but not for the response_body which is redefined:

.. code-block:: yaml

   methods:
     ListClients:
       ...
     ListClientWithDetails:
       extends: ListClients
       response_body:
         inherit: false
       ...

Sample using an extension where the section SessionAuthentification extends FormAuthentification but the content of the body of the method Login is removed:

.. code-block:: yaml

   methods:
     Login:
       request_body:
         type: object
         properties:
           login:
             type: string
           password:
             type: string
     SSO:
       extends: Login
       request_parameters:
         token_id:
           type: string
       request_body:
         removed: true

You can extend multiple elements by providing an list of extensions.

.. code-block:: yaml

   Methods:
     Authentificated:
       request_header:
         X-Auth-Token:
           type: string
     Paginated:
       request_parameter:
         index:
           type: integer
         limit:;
           type: integer
     Customers:
       extends:
         - Authentificated
         - Paginated