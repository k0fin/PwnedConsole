#!/usr/bin/python

import os
import sys
import re
import requests
import textwrap
import pwned_console_config

from time import sleep
from pypwned import *

def banner():
    os.system('clear')
    open_banner = open(pwned_console_config.default_banner, 'r')
    for banner_line in open_banner:
        print banner_line.rstrip()
    open_banner.close()

def description_parser(descr):
    if '<' or '>' in descr:
        descr = re.sub('<.*?>', '', descr)

    for tld in pwned_console_config.tld_strip_list:    
        if tld in descr:
            descr = descr.replace(tld,'').strip()

    if '.' in descr:
        descr = descr.replace('.','.\n').strip()
    if '&quot;' in descr:
        descr = descr.replace('&quot;','').strip()
    if "'" in descr:
        descr = descr.replace("'","").strip()
    if '&mdash;' in descr:
        descr = descr.replace('&mdash;','')
    descr = ''.join([x for x in descr if ord(x) < 128])
    return descr.strip()

def output_formatter(title,org,domain,count,data,sys_date,date,verif,descrip):
    descrip_dedent = textwrap.dedent(descrip).strip()
    descrip = textwrap.fill(descrip_dedent, width=50)

    breach_template = """
===========================================================
-----------------------------------------------------------
Breach Title       | {0:10}
Organization       | {1:10}
Domain             | {2:10}
Date               | {3:10}
System Storage Date| {4:10}
Accounts Breached  | {5:1}
Breach Verified    | {6:1}
-----------------------------------------------------------
-----------------------------------------------------------
< Breach Details >    
-----------------------------------------------------------
{7:1}
-----------------------------------------------------------
-----------------------------------------------------------
< Breach Data Types >
-----------------------------------------------------------
{8:1}
-----------------------------------------------------------
===========================================================
    """.format(title,org,domain,date,sys_date,count,verif,descrip, '| ' + '\n| '.join(data).upper())
    return breach_template

def json_parser(query_text):
    title = query_text['Title'].upper().strip()
    organization = query_text['Name'].strip()
    domain = query_text['Domain'].strip()
    breach_date = query_text['BreachDate']
    pwncount = query_text['PwnCount']
    verified = query_text['IsVerified']
    added_date = query_text['AddedDate']
    affected_data_types = query_text['DataClasses']
    description = description_parser(query_text['Description'].strip())
    stdout_report = output_formatter(title,organization,domain,pwncount,affected_data_types,added_date,breach_date,verified,description)
    return stdout_report

def all_breaches_account(account):
    api_query = getAllBreachesForAccount(email=account)
    for breach in range(0,len(api_query)):
        json_processor = json_parser(api_query[breach])
        print json_processor
        raw_input("[*]Press [ENTER] To Continue-")
    raw_input("[*]No More Records. Press [ENTER] To Return-")

    banner()
    breach_menu(account)

def all_breached_sites(account):
    api_query = getAllBreaches()
    for breach in range(0,len(api_query)):
        json_processor = json_parser(api_query[breach])
        print json_processor
        raw_input("[*]Press [ENTER] To Continue-")
    raw_input("[*]No More Records. Press [ENTER] To Return-")

    banner()
    breach_menu(account)

def single_breach(account):
    site = str(raw_input("[*]Site Name: "))
    if "." in site:
        site = site.split(".")[0].strip()
    api_query = getSingleBreachedSite(name=site)
    for breach in range(0,len(api_query)):
        json_processor = json_parser(api_query)
        print json_processor
        raw_input("[*]Press [ENTER] To Continue-")
    raw_input("[*]No More Records. Press [ENTER] To Return-")

    banner()
    breach_menu(account)

def all_data(account):
    api_query = getAllDataClasses()
    print "=" * 30
    for data in api_query:
        print "| {}".format(data)
    print "=" * 30
    raw_input("[*]Press [ENTER] To Return-")

    banner()
    breach_menu(account)

def all_pastes_account(account):
    if "@" not in account:
        print "[-]No email account loaded."
        raw_input("Press [ENTER] To Return-")

    else:
        api_query = getAllPastesForAccount(account=account)
        for paste in range(0,len(api_query)):
            
            source = api_query[paste]['Source']
            id = api_query[paste]['Id']
            title = api_query[paste]['Title']
            date = api_query[paste]['Date']
            count = api_query[paste]['EmailCount']
            url = "http://www.{}.com/{}".format(source.lower(),id)
            print '''
=====================================
Paste Details
-------------------------------------
Paste Source       | {}
Paste ID Number    | {}
Paste Title        | {}
Paste Date         | {}
Paste Breach Count | {}
Paste URL          | {}
-------------------------------------
=====================================
            '''.format(source,id,title,date,count,url)

            raw_input("Press [ENTER] To Continue-")
        raw_input("Completed. Press [ENTER] To Return-")

    banner()
    paste_menu(account)

def breach_menu(breach_account):
    print '[*]Account Loaded: {}'.format(breach_account)
    print '''
[ 1 ] | All Breaches For Account
[ 2 ] | All Breached Sites In System
[ 3 ] | Single Site Breach
[ 4 ] | All Data Classes In System
[ 5 ] | Back To Main Menu
    '''
    print ''
    breach_option = int(raw_input('Select An Option: '))
    
    if breach_option == 1:
        all_breaches_account(breach_account)
    elif breach_option == 2:
        all_breached_sites(breach_account)
    elif breach_option == 3:
        single_breach(breach_account)
    elif breach_option == 4:
        all_data(breach_account)
    elif breach_option == 5:
        banner()
        master_menu(breach_account)
    else:
        pass
        banner()
        breach_menu(breach_account)


def paste_menu(paste_account):
    print '[*]Account Loaded: {}'.format(paste_account)
    print '''
[ 1 ] | All Pastes For Account
[ 2 ] | Back To Main Menu
    '''
    print ''
    paste_option = int(raw_input('Select An Option: '))
    if paste_option == 1:
        all_pastes_account(paste_account)
    elif paste_option == 2:
        banner()
        master_menu(paste_account)
    else:
        pass
        banner()
        paste_menu(paste_account)

def switch_account(drop_account):
    print "[*]Current Account: ".format(drop_account)
    new_account = raw_input('[*]Switch Loaded Account To (Or Type "back" To Return): ')
    
    if new_account == "back" or new_account == "Back" or new_account == "BACK":
        banner()
        master_menu(drop_account)
    else: 
        return new_account

def master_menu(account):
        
    print '[*]Account Loaded: {}'.format(account)
    print '''
[ 1 ] | Breaches
[ 2 ] | Pastes
[ 3 ] | Switch Account
[ 4 ] | Exit
    '''
    print ''
    option = int(raw_input('Select An Option: '))
    if option == 1:
        banner()
        breach_menu(account)
    elif option == 2:
        banner()
        paste_menu(account)
    elif option == 3:
        banner()
        account_switch = switch_account(account)
        banner()
        master_menu(account_switch)
    elif option == 4:
        banner()
        print '[*]Goodbye!'
        sys.exit()
    else:
        pass
        banner()
        master_menu()

def main():
    try:
        loaded_account = sys.argv[1]
        banner()
        master_menu(loaded_account)

    except IndexError:
        banner()
        print pwned_console_config.index_error_message
        print pwned_console_config.usage_message
        sys.exit()

    except ValueError:
        banner()
        print pwned_console_config.value_error_message
        sleep(.5)
        banner()
        main()
main()
