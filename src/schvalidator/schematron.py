#
# Copyright (c) 2016 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

from .exceptions import ProjectFilesNotFoundError
from .log import log, role2level, schlog
from lxml import etree
from lxml.isoschematron import Schematron
import os

# Common namespaces
NS = dict(svrl="http://purl.oclc.org/dsdl/svrl",
          xs="http://www.w3.org/2001/XMLSchema",
          sch="http://www.ascc.net/xml/schematron",
          iso="http://purl.oclc.org/dsdl/schematron",
          d="http://docbook.org/ns/docbook"
          )


class NSElement(object):
    def __init__(self, namespace, prefix=None):
        self.ns = namespace
        self.prefix = prefix

    def __call__(self, name):
        return etree.QName(self.ns, name)

    def __getattr__(self, name):
        return self(name)

    def __repr__(self):
        if self.prefix is None:
            result = "%s(%s)" % (self.__class__.__name__, self.ns)
        else:
            result = "%s(%s=%s)" % (self.__class__.__name__,
                                    self.prefix,
                                    self.ns
                                    )
        return result

svrl = NSElement(NS['svrl'])


def validate_sch(schema, xmlfile, phase=None, xmlparser=None):
    """Validate XML with Schematron schema
    """
    if xmlparser is None:
        # Use our default XML parser:
        xmlparser = etree.XMLParser(encoding="UTF-8",
                                    no_network=True,
                                    )
    doctree = etree.parse(xmlfile, parser=xmlparser)
    log.info("Schematron validation with file=%r, schema=%r, phase=%r",
             xmlfile, schema, phase)
    schematron = Schematron(file=schema,
                            phase=phase,
                            store_report=True,
                            store_xslt=True)
    result = schematron.validate(doctree)
    log.info("=> Validation result was: %s", result)
    return result, schematron


def check_args(args):
    """Checks the arguments for consistency"""
    log.info("Consistency check for args: %s", args)

    for f in [args['XMLFILE'], args['--schema']]:
        if not os.path.exists(f):
            raise ProjectFilesNotFoundError("File not found", f)


def extractrole(fa):
    """Try to extract ``role`` attributes either in the ``svrl:failed-assert''
       or in the preceding sibling ``svrl:fired-rule`` element.

    :param fa: the current `svrl:failed-assert`` element
    :return: attribute value of ``role``, otherwise None if not found
    :rtype: str
    """
    try:
        role = list(fa.itersiblings(svrl('fired-rule').text,
                                    preceding=True)
                    )[0].attrib.get('role')
    except IndexError:
        role = None

    # Overwrite with next role, if needed
    role = role if fa.attrib.get('role') is None \
                else fa.attrib.get('role')
    return role


def process_result_svrl(report):
    """Process the report tree

    :param report: tree of :class:`lxml.etree._XSLTResultTree`
    """

    for idx, fa in enumerate(report.iter(svrl("failed-assert").text), 1):
        text = fa[0].text.strip()
        loc = fa.attrib.get('location')

        # The ``role`` attribute contains contains the log level
        level = role2level(extractrole(fa))

        schlog.log(level,
                   "Message %i\n"
                   "\tLocation: %r\n"
                   "\t%s\n"
                   "%s",
                   idx, loc, text, "-"*20)


def process(args):
    """Process the validation and the result
    """
    check_args(args)
    result, schematron = validate_sch(args['--schema'],
                                      args['XMLFILE'],
                                      phase=args['--phase'],
                                      )
    reportfile = args['--report']

    if not result:
        if reportfile is not None:
            report.write(reportfile,
                         pretty_print=True,
                         encoding="unicode",
                         )
            log.info("Wrote Schematron validation report to %r", reportfile)
        else:
            schlog.debug(report)
        process_result_svrl(schematron.validation_report)

        schlog.fatal("Validation failed!")
        return 200
    else:
        if reportfile:
            root = etree.XML("""<svrl:schematron-output
                xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:sch="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:d="http://docbook.org/ns/docbook"
                schemaVersion=""/>""").getroottree()
            root.write(reportfile, pretty_print=True, encoding="unicode")

        schlog.info("Validation was successful")
    return 0
