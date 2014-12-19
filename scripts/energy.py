#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import sys, codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import lxml.html
import urllib
from lxml.html import fromstring

template_host = (
"""
define host {
       use                      generic-host
       host_name                hydroquebec_%(order)s
       alias                    %(alias)s
       check_command            check_dummy!0!OK
}
""")

template_service = (
"""
define service {
       use                      generic-service
       host_name                hydroquebec_%(order)s
       check_command            check_hydro_quebec!%(alias)s
       display_name             %(alias)s
       service_description      hydroquebec_%(order)s
       servicegroups            energy
       labels                   order_%(order)s
       action_url               %(url)s
}
""")

business_rule = (
"""
define host {
       use                            generic-host
       host_name                      energy
       alias                          energy
       check_command                  check_dummy!0!OK
}
define service {
       use                              generic-service
       host_name                        energy
       service_description              energy
       display_name                     Énergies
       notes                            Bilan des interruptions par région.
       check_command                    bp_rule!%(all_host)s
       business_rule_output_template    $(x)$
       servicegroups                    main
       icon_image                       fa-flash
}
""")

def chunks(l, n):
   """ Yield successive n-sized chunks from l.
   """
   for i in xrange(0, len(l), n):
      yield l[i : i + n]


def main():
   response = urllib.urlopen("http://pannes.hydroquebec.com/pannes/bilan-interruptions-service/#bis")
   page_source = response.read()
   root = lxml.html.fromstring(page_source)
   url_list = root.xpath('//td//@href')
   url_list.append("http://pannes.hydroquebec.com/pannes/bilan-interruptions-service/#bis")
   regions_list = root.xpath('//td//text()')
   regions_list = [r[0] for r in chunks(regions_list, 5)]
   regions_list[-1] = u"Across Québec"

   all_host = []

   for order in range(len(regions_list)):
       alias = regions_list[order]
       url = url_list[order]
       print template_host % {'order': order + 1, 'alias': alias}
       print template_service % {'order': order + 1, 'alias': alias, 'url': url}
       all_host.append('hydroquebec_%d,hydroquebec_%d' % (order + 1, order + 1))

   print business_rule % {'all_host': '&'.join(all_host)}

if __name__ == '__main__':
    main()
