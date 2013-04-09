ApiDoc's TODO
=============

Features
--------
* RunMode: The user can run the methods through his browser
* Diff: Provide a visual diff between versions
* Variable: Some parts of the sources can refered to variables defined in the source file or injected when the document is builded


Improvements
------------
* ScrollMemory: When user change the displayed version, keep the focus on the same method
* Logger: Replace print and other stdotu by a proper logger
* CrossPlateform:
    * Replace pyinotify by watchdog
* Reduce embedded size
    * Reduce (or eliminate) jquery
    * Reduce images size (amount of icones in the sprite)
    * Minimize CSS and javascripts files
    * Reduce HTML ouput (tab, class's names length)


Contributions
-------------
* Add Glyphicons, Bootstrap, Jquery and other external projet in the README file
* Provide a full INSTALL file with samples (install git + git clone)
* Provide a full documentation with all the possible cases (.md to embdded in gitorious wiki ? or .srt to use sphynx ?)
* Synchronise current "example" folder with documentation (previsous TODO)
* Upgrade and Implement BDD tests
