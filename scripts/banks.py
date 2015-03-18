#!/usr/bin/env python
# -*- coding: utf-8 -*-

BANKS = {
    'RBC Banque Royale': {
        'protocol': 'https',
        'domain': 'www1.royalbank.com',
        'path': '/cgi-bin/rbaccess/rbunxcgi?F6=1&F7=IB&F21=IB&F22=IB&REQUEST=ClientSignin&LANGUAGE=FRENCH',
        },
    'TD Canada Trust': {
        'protocol': 'https',
        'domain': 'banquenetcpo.td.com',
        'path': '/waw/idp/login.htm?execution=e1s1',
        },
    'BDC': {
        'protocol': 'https',
        'domain':'connex.bdc.ca',
        'path': '/_LOGIN/BDCConnexlogin.aspx',
        },
    'CIBC': {
        'protocol': 'https',
        'domain': 'www.cibc.com',
        'path': '/ca/personal.html?int_id=HP_PersonalBanking',
        },
    'Banque de Montreal': {
        'protocol': 'https',
        'domain': 'www1.bmo.com',
        'path': '/onlinebanking/cgi-bin/netbnx/NBmain?product=6',
        },
    'Scotiabank': {
        'protocol': 'https',
        'domain': 'www2.scotiaonline.scotiabank.com',
        'path': '/online/authentication/authentication.bns',
        },
    'BNC': {
        'protocol': 'https',
        'domain': 'bvi.bnc.ca',
        'path': '/',
        },
    'Banque Laurentienne': {
        'protocol': 'https',
        'domain': 'blcweb.banquelaurentienne.ca',
        'path': '/BLCDirect/',
        },
    'Desjardins': {
        'protocol': 'https',
        'domain': 'accesd.desjardins.com',
        'path': '/fr/accesd/',
        },
    }

template = (
"""define host {
       use                      generic-host
       host_name                %(domain)s
       address                  %(domain)s
       alias                    %(domain)s
       check_command            check_dummy!0!OK
}
define service {
       use                      generic-service
       host_name                %(domain)s
       check_command            check_http2!%(url)s
       display_name             %(bank)s
       service_description      %(domain)s
       servicegroups            banks
       labels                   order_%(order)d
       action_url               %(url)s
}
""")

business_rule = (
"""
define host {
       use                            generic-host
       host_name                      banks
       alias                          banks
       check_command                  check_dummy!0!OK
}
define service {
       use                            template_bprule
       host_name                      banks
       service_description            banks
       servicegroups                  main
       display_name                   Banques
       notes                          Services en ligne des principales banques.
       check_command                  bp_rule!%(all_banks)s
       business_rule_output_template  $(x)$
       icon_image                     fa-university
}
""")



def main():
    # all_banks is a workaround while we wait for g:group_banks to work
    all_banks = []
    for order, (bank, values) in enumerate(BANKS.iteritems()):
        all_banks.append('%s,%s' % (values['domain'], values['domain']))
        url = values['protocol'] + '://' + values['domain'] + values['path']
        print template % {'bank': bank.replace('_', ' '),
                          'domain': values['domain'],
                          'order': order + 1,
                          'url': url}
    all_banks = '&'.join(all_banks)
    print business_rule % {'all_banks': all_banks}

if __name__ == '__main__':
    main()
