#!/usr/bin/python


# Config for banners
#----------------------------------------------------------------------
banners_path = 'banners/'
default_banner = '{}pwned_console_default.banner'.format(banners_path)
#----------------------------------------------------------------------

# List for storing TLD values to strip within description text
#----------------------------------------------------------------------
tld_strip_list = ['.com','.net','.org','.edu','.int','.co','.uk','.cn','.ru','.se','.ca','.gov','.biz','.be','.asia','.su','.cm','.is']
#----------------------------------------------------------------------

# Error message values
#----------------------------------------------------------------------
index_error_message = "[-]Missing argument."
value_error_message = "[-]Option not allowed."
usage_message = "[*]Usage: python pwnconsole.py <email_addr/account_name>"
http_not_found = "404 - Not found - the account could not be found and has therefore not been pwned"
http_not_found_breach = "[*]No Breach Data Available For Account."
http_not_found_paste = "[*]No Pastes Available For Account."
