#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import sys, codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import urllib, json
from collections import defaultdict

try:
    from tokens import TOKENS
except ImportError:
    TOKENS = defaultdict(lambda: '')

def get_boroughs_list():
    # get list of all boroughs
    url = "http://infoneige.ca/vdm/stats.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    boroughs = data["avancement"]
    boroughs_list = []

    for i in boroughs:
        borough = i["arrondissment"].replace(' ', '')
        boroughs_list.append(borough)

    return boroughs_list

TRANSPORTS = {
    'Métro à Montréal': {
        'hostname': 'stm_metro',
        'command': 'check_stm_metro_montreal!1!3',
        'url': 'http://www.stm.info/en/info/service-updates/metro',
    },
#    'Vélos (Bixi) à Montréal: nombre de stations pleines ou vides': {
#        'hostname': 'bixi_mtl',
#        'command': 'check_bixi_montreal!http://montreal.bixi.com/data/bikeStations.xml!1!100',
#        'url': 'http://montreal.bixi.com',
#    },
    "AMT: nombre d'alertes": {
        'hostname': 'amt_trains',
        'command': 'check_amt_montreal!http://opendata.amt.qc.ca:2539/ServiceGTFSR/Alert.pb!%s!1!30' % TOKENS['AMT'],
        'url': 'http://amt.qc.ca/train/deux-montagnes.aspx',
    },

    "STQ: nombre d'alertes": {
        'hostname': 'stq_traversiers',
        'command': 'check_ferries!1!2',
        'url': 'https://www.traversiers.com/fr/accueil/',
    },

}

template = (
"""
define host {
       use                      generic-host
       host_name                %(hostname)s
       alias                    %(hostname)s
       check_command            check_dummy!0!OK
}
define service {
       use                      generic-service
       host_name                %(hostname)s
       display_name             %(name)s
       service_description      %(hostname)s
       check_command            %(command)s
       servicegroups            transports
       labels                   order_%(order)d
       action_url               %(url)s
}
""")

business_rule = (
"""
define host {
       use                            generic-host
       host_name                      transports
       alias                          transports
       check_command                  check_dummy!0!OK
}
define service {
       use                              template_bprule
       host_name                        transports
       display_name                     Transports
       service_description              transports
       notes                            Problèmes liés aux transports.
       # check_command                  bp_rule!g:group_banks
       check_command                    bp_rule!%(all_transports)s
       business_rule_output_template    $(x)$
       servicegroups                    main
       icon_image                       fa-bus
}
""")

def main():

    all_transports = []
    boroughs_list = get_boroughs_list()
    for index, borough in enumerate(boroughs_list):
        index += 1
        TRANSPORTS["déneigement - %s" % borough] = {
        'hostname': "deneigement_%s" % index,
        'command': 'check_snow_clearance!"%s"!70!30' % borough,
        'url': 'http://infoneige.ca/',
        }

    for order, (name, values) in enumerate(TRANSPORTS.iteritems()):
        all_transports.append('%s,%s' % (values['hostname'], values['hostname']))

        print template % {'name': name,
                          'hostname': values['hostname'],
                          'command': values['command'],
                          'url': values['url'],
                          'order': order + 1,
                          }

    all_transports = '&'.join(all_transports)
    print business_rule % {'all_transports': all_transports}


if __name__ == '__main__':
    main()
