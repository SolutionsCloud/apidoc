
import os
import sys
import shutil

from distutils.cmd import Command
from setuptools.command.test import test

class ApiDocTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

class Resource(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        resource_dir = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'apidoc',
                'template',
                'resource'
            )
        )

        resource_src_dir = os.path.realpath(os.path.join(resource_dir, 'src'))
        resource_src_js_dir = os.path.realpath(os.path.join(resource_src_dir, 'js'))
        resource_src_css_dir = os.path.realpath(os.path.join(resource_src_dir, 'css'))
        resource_src_less_dir = os.path.realpath(os.path.join(resource_src_dir, 'less'))
        resource_js_dir = os.path.realpath(os.path.join(resource_dir, 'js'))
        resource_css_dir = os.path.realpath(os.path.join(resource_dir, 'css'))

        os.system("wget --post-data='css=%s&js=%s' -O '/tmp/bootstrap.zip' %s" % (
            '["reset.less","scaffolding.less","grid.less","layouts.less","type.less","code.less","tables.less","forms.less","navs.less","navbar.less","tooltip.less","popovers.less","modals.less","wells.less","close.less","utilities.less","component-animations.less","responsive-utilities.less","responsive-767px-max.less","responsive-768px-979px.less","responsive-1200px-min.less","responsive-navbar.less"]',
            '["bootstrap-transition.js","bootstrap-modal.js","bootstrap-scrollspy.js","bootstrap-tooltip.js","bootstrap-popover.js","bootstrap-affix.js"]',
            'http://bootstrap.herokuapp.com'
        ))

        assert os.path.exists('/tmp/bootstrap.zip'), 'Downloaded bootstrap zip not found'

        try:
            os.system('unzip /tmp/bootstrap.zip -d /tmp/apidoc-bootstrap')

            shutil.move('/tmp/apidoc-bootstrap/js/bootstrap.min.js', '%s/bootstrap.min.js' % resource_src_js_dir)
            shutil.move('/tmp/apidoc-bootstrap/css/bootstrap.min.css', '%s/bootstrap.min.css' % resource_src_css_dir)
        finally:
            os.remove('/tmp/bootstrap.zip')
            shutil.rmtree('/tmp/apidoc-bootstrap')

        os.system('wget -O "%s" "%s"' % ('%s/jquery.min.js' % resource_src_js_dir, 'http://code.jquery.com/jquery-2.0.3.min.js'))
        assert os.path.exists('%s/mousetrap.min.js' % resource_src_js_dir), 'Downloaded jquery file not found'

        os.system('wget -O "%s" "%s"' % ('%s/mousetrap.min.js' % resource_src_js_dir, 'http://cdn.craig.is/js/mousetrap/mousetrap.min.js'))
        assert os.path.exists('%s/mousetrap.min.js' % resource_src_js_dir), 'Downloaded mousetrap file not found'

        os.system('lessc -x "%s/apidoc.less" "%s/apidoc.css"' % (resource_src_less_dir, resource_src_css_dir))

        for folder in  [resource_css_dir, resource_js_dir]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        self._compress("css", ["%s/bootstrap.min.css" % resource_src_css_dir, "%s/apidoc.css" % resource_src_css_dir, "%s/font.css" % resource_css_dir], "%s/combined.css" % resource_css_dir)
        assert os.path.exists('%s/combined.css' % resource_css_dir), 'Combined css file not found'

        self._compress("css", ["%s/bootstrap.min.css" % resource_src_css_dir, "%s/apidoc.css" % resource_src_css_dir, "%s/font-embedded.css" % resource_css_dir], "%s/combined-embedded.css" % resource_css_dir)
        assert os.path.exists('%s/combined-embedded.css' % resource_css_dir), 'Combined embedded css file not found'

        self._compress("js", ["%s/jquery.min.js" % resource_src_js_dir, "%s/bootstrap.min.js" % resource_src_js_dir, "%s/mousetrap.min.js" % resource_src_js_dir, "%s/apidoc.js" % resource_src_js_dir], "%s/combined.js" % resource_js_dir)
        assert os.path.exists('%s/combined.js' % resource_js_dir), 'Combined js file not found'

    def _merge_files(self, input_files, output_file):
        """Combine the input files to a big output file"""
        # we assume that all the input files have the same charset
        with open(output_file, mode='wb') as out:
            for input_file in input_files:
                out.write(open(input_file, mode='rb').read())

    def _compress(self, format, input_files, output_file):
        import yuicompressor, subprocess, tempfile

        handle, merged_filename = tempfile.mkstemp(prefix='minify')
        os.close(handle)
        try:
            self._merge_files(input_files, merged_filename)

            os.system('java -jar %s --type %s -o %s --charset utf-8 %s' % (yuicompressor.get_jar_filename(), format, output_file, merged_filename))
        finally:
            os.remove(merged_filename)