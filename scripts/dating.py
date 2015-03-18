#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATING = {
    'quebecrencontres.com': {
        'hostname': 'quebecrencontres.com',
        'address': '68.71.41.131',
        'display_name': 'Quebecrencontres.com',
        'command': 'check_quebecrencontrescom',
    },
    'reseaucontact.com': {
        'hostname': 'reseaucontact.com',
        'address': '198.178.155.41',
        'display_name': 'Reseaucontact.com',
        'command': 'check_reseaucontactcom',
    }
}

template = (
"""
define host {
       use                      generic-host
       host_name                %(hostname)s
       alias                    %(hostname)s
       address                  %(address)s
       check_command            check_dummy!0!OK
}
define service {
       use                      generic-service
       host_name                %(hostname)s
       display_name             %(display_name)s
       service_description      %(hostname)s
       check_command            %(command)s
       servicegroups            dating
       labels                   order_%(order)d
       action_url               %(url)s
}

""")

business_rule = (
"""
define host {
       use                            generic-host
       host_name                      dating
       alias                          dating
       check_command                  check_dummy!0!OK
}
define service {
       use                              template_bprule
       host_name                        dating
       service_description              dating
       display_name                     Rencontres
       notes                            Sites de rencontres et leur nombre d'usagers.
       check_command                    bp_rule!%(all_dating)s
       business_rule_output_template    $(x)$
       servicegroups                    main
       icon_image                       fa-heart
}

""")



def main():
    all_dating = []
    for order, (name, values) in enumerate(DATING.iteritems()):
        all_dating.append('%s,%s' % (values['hostname'], values['hostname']))
        print template % {'display_name': values['display_name'],
                          'hostname': values['hostname'],
                          'command': values['command'],
                          'address': values['address'],
                          'order': order + 1,
                          'url': 'http://' + values['hostname'],
                          }
    
    all_dating = '&'.join(all_dating)
    print business_rule % {'all_dating': all_dating}

if __name__ == '__main__':
    main()
