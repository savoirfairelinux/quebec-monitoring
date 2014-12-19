#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lxml.html
import urllib
from lxml.html import fromstring

template_host = (
"""
define host {
       use                      generic-host
       host_name                ski_%(order)s
       alias                    %(alias)s
       check_command            check_dummy!0!OK
}
""")

template_service = (
"""
define service {
       use                      generic-service
       host_name                ski_%(order)s
       check_command            check_ski_stations!%(alias)s
       display_name             ski - %(alias)s
       service_description      ski_%(order)s
       servicegroups            winter
       labels                   order_%(order)s
       action_url               %(url)s
}
""")

business_rule = (
"""
define host {
       use                            generic-host
       host_name                      winter
       alias                          winter
       check_command                  check_dummy!0!OK
}
define service {
       use                              generic-service
       host_name                        winter
       service_description              winter
       display_name                     Hiver
       notes                            Conditions de ski au Québec.
       check_command                    bp_rule!%(all_host)s
       business_rule_output_template    $(x)$
       servicegroups                    main
       icon_image                       fa-gift
}
""")


def get_region_list():
    response = urllib.urlopen("http://www.zoneski.com/vivelaneige/tableauqc2014-conditions.php")
    # Read html
    page_source = response.read()
    # Parse html/xml
    root = lxml.html.fromstring(page_source)
    row_list = root.xpath('//table[@id="conditions-table"]/tbody/tr')
    region_list = []

    for row in row_list:
        cells = row.getchildren()
        region = cells[2].text_content()
        if region not in region_list:
            region_list.append(region)

    region_list.append(u"Tout le Québec")

    return region_list

def main():
   region_list = get_region_list()
   url = "http://www.zoneski.com/vivelaneige/tableauqc.php#conditions"
   all_host = []

   for order in range(len(region_list)):
       alias = region_list[order].encode("utf-8")
       print template_host % {'order': order + 1, 'alias': alias}
       print template_service % {'order': order + 1, 'alias': alias, 'url': url}
       all_host.append('ski_%d,ski_%d' % (order + 1, order + 1))

   print business_rule % {'all_host': '&'.join(all_host)}

if __name__ == '__main__':
    main()
