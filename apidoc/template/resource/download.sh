#!/usr/bin/env bash

BOOTSTRAP="http://bootstrap.herokuapp.com"
JQUERY="http://code.jquery.com/jquery-2.0.3.min.js"
MOUSETRAP="http://cdn.craig.is/js/mousetrap/mousetrap.min.js"

CSS='["reset.less","scaffolding.less","grid.less","layouts.less","type.less","code.less","tables.less","forms.less","navs.less","navbar.less","tooltip.less","popovers.less","wells.less","utilities.less","responsive-utilities.less","responsive-767px-max.less","responsive-768px-979px.less","responsive-1200px-min.less","responsive-navbar.less"]'
JS='["bootstrap-scrollspy.js","bootstrap-tooltip.js","bootstrap-popover.js","bootstrap-affix.js"]'

BASEDIR=$(dirname $0)

# Get customized bootstrap
getBootstrap()
{
    echo "downloading bootstrap"
    wget --post-data="css=$CSS&js=$JS" -O "bootstrap.zip" $BOOTSTRAP

    echo "extracting bootstrap"
    unzip bootstrap.zip -d /tmp/apidoc-bootstrap

    echo "moving bootstrap"
    mv /tmp/apidoc-bootstrap/js/bootstrap.min.js $BASEDIR/js/bootstrap.min.js
    mv /tmp/apidoc-bootstrap/css/bootstrap.min.css $BASEDIR/css/bootstrap.min.css

    echo "cleaning bootstrap"
    rm bootstrap.zip
    rm -rf /tmp/apidoc-bootstrap
}

# Get jquery
getJquery()
{
    echo "downloading jquery"
    wget -O "jquery.min.js" $JQUERY

    echo "moving jquery"
    mv jquery.min.js $BASEDIR/js/jquery.min.js
}

# Get jquery
getMousetrap()
{
    echo "downloading mousetrap"
    wget -O "mousetrap.min.js" $MOUSETRAP

    echo "moving mousetrap"
    mv mousetrap.min.js $BASEDIR/js/mousetrap.min.js
}


echo ""

getBootstrap
getJquery
getMousetrap