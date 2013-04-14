ApiDoc's TODO
=============

Features
--------
* RunMode: The end user can run the methods through his browser
* Diff: Provide a visual diff between versions
* Variable: Some parts of the sources can refered to variables defined in the source file or injected when the document is builded
* Filter: Define in config files (or in command line arguments) the sections and/or the versions who should not be displayed
* Simplify Sources: When the API have only one version or only one section, The keys version and section could be ommited in sources files


Improvements
------------
* Remove types/namespace who are not used in displayed methods
* Check the maximum of potentiel problems in analyse part. Actualy, some verifications are asserted in rendering stage.
* Reduce embedded size
    * Reduce (or eliminate) jquery
    * Reduce images size (amount of icones in the sprite)
    * Minimize CSS and javascripts files
    * Reduce HTML ouput (tab, class's names length)


Contributions
-------------
* Provide a full documentation with all the possible cases (.md to
 embdded in gitorious wiki ? or .srt to use sphynx ?)
* Synchronise current "example" folder with documentation (previsous TODO)
* Provide real examples with paypal, dropbox, or twitter
* Upgrade and Implement BDD tests


DONE
====
* Replace pyinotify because it's not compatible with MacOs
* Replace prints by a logger
* Add Glyphicons, Bootstrap, Jquery and other external projet in the README file
* Provide a full description to install ApiDoc (install git + git clone + virtualenv...)
* When user change the displayed version, keep the focus on the same position relative to the active method
* Add keyboard's shortcut handler to simplify navigation
