#!/usr/bin/env python
# -*- coding: utf-8 -*-

DNS = {
    # Cogeco Cable (Trois-rivieres) 
    'cogeco.ca': ['205.151.69.200','205.151.68.200'],
    
    # Videotron.CA 
    'videotron.ca': ['205.151.222.250', '205.151.222.251'],
    
    # Colbanet
    'colba.net': ['69.28.239.8', '69.28.239.9'],
    }

template_host = (
"""
define host {
       use                      generic-host
       host_name                %(host)s
       address                  %(host)s
       alias                    %(host)s
       check_command            check_dummy!0!OK
}
""")

template_service = (
"""
define service {
       use                      generic-service
       host_name                %(host)s
       check_command            check_dig_service!%(ip)s!www.gouv.qc.ca
       display_name             %(host)s (%(ip)s)
       service_description      %(ip)s
       servicegroups            dns
       labels                   order_%(order)d
}
""")

business_rule = (
"""
define host {
       use                            generic-host
       host_name                      dns
       alias                          dns
       check_command                  check_dummy!0!OK
}
define service {
       use                              template_bprule
       host_name                        dns
       service_description              dns
       display_name                     DNS
       notes                            Principaux serveurs DNS.
       check_command                    bp_rule!%(all_dns)s
       business_rule_output_template    $(x)$
       servicegroups                    main
       icon_image                       fa-sitemap
}
""")


def main():
    all_dns = []
    order = 1
    for host, ips in DNS.iteritems():
        print template_host % {'host': host}
        for ip in ips:
            print template_service % {'host': host, 'ip': ip, 'order': order}
            all_dns.append('%(host)s,%(ip)s' % {'host': host, 'ip': ip})
            order += 1
    print business_rule % {'all_dns': '&'.join(all_dns)}
        

if __name__ == '__main__':
    main()
