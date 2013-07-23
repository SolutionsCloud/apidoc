TODO List
=========

Features
--------

* RunMode: The end user can run the methods through his browser
* Simplify Sources: When the API have only one version or only one section, The keys version and section could be ommited in sources files
* Using different version of source's schema
* Method templating: Methods are based on template who define what's will be used in the description. Ie. Json-rpc template will simplify request_body/response_body and provide a real errors cases
* Multiple responses: Provide a way for a request to have differents responses (like inheritances, or simplfyed/advanced responses....)
* Some methods does not reply always in json (in oAuth process for example)


Improvements
------------

* Reduce embedded size
    * Reduce (or eliminate) jquery
    * Minimize CSS and javascripts files


DONE
----

* Replace pyinotify because it's not compatible with MacOS
* Replace prints by a logger
* Add Glyphicons, Bootstrap, Jquery and other external projet in the README file
* Provide a full description to install ApiDoc (install git + git clone + virtualenv...)
* When the user changes the displayed version, keep the focus on the same position relative to the active method
* Add keyboard's shortcut handler to simplify navigation
* Define filters in config files to choose the sections and/or the versions which should not be displayed
* Implement a diff mode
* Source files refere to variables inject in command arguments or in config file
* Add a default message in responses codes
* Unused types and namespace are no longer displayed
* Replace icons by font
* Provide a full documentation with all the possible cases
* Provide a sample of a real API (paypal)
* namespaces and section are renamed into category
* Add a const type in objets
* Add a schema validator
* Add a enum type in objects
* Types as managed like real objects
* Request parameters, request headers et response codes can be defined as generoc. They will be displayed in an other color
* It is no longer necessary to stipulate query string parameters in URI.
* Adding Font SourceCodePro in project
* Adding a new componant "without"
* Adding a new config option "layout"
* Adding an option "no validate" to skip the json-schema validation