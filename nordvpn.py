#! /bin/python3
import glob
import argparse
from argparse import RawTextHelpFormatter
import subprocess
import sys
import os
import os.path
import random
import json
from urllib.request import Request, urlopen
import shutil
import textwrap

country_args= ['AL','AR','AU','AT','AZ','BE','BA','BR','BG','CA','CL','CR','HR','CY','CZ','DK','EG','EE','FI','FR','GE',
               'DE','GR','HK','HU','IS','IN','ID','IE','IL','IT','JP','LV','LU','MK','MY','MX','MD','NL','NZ','NO','PL',
               'PT','RO','RU','RS','SG','SK','SI','ZA','KR','ES','SE','CH','TW','TH','TR','UA','AE','GB','US','VN']

parser=argparse.ArgumentParser(description='''Just a simple yet better openvpn manager for NordVPN''', formatter_class=RawTextHelpFormatter)

parser.add_argument('--status', help='Allows you to double check if you are still connected to a VPN', action='store_true')

parser.add_argument('--update', help='Downloads new server list from NordVPN and updates all ovpn_tvp & ovpn_udp files in /etc/openvpn/*', action='store_true')

parser.add_argument('-p', help='Specifies to use protocol TCP or UDP with your vpn server. Example: "nordvp -rp udp" to use a random UDP server.', choices=['tcp','udp'],metavar='')

parser.add_argument('-r', help='Uses a random server within specified protocol (Optionaly use with args -p and -c to protocol and country.)', action='store_true')

parser.add_argument('--recommend', help='Get\'s a recommended server based on your latitude & longitude when a country is specified it get\'s server from said country', action='store_true')

parser.add_argument( '--exit', help='pgreps for openvpn and kill\'s the instance.', action='store_true')

parser.add_argument('--password', help='Uses openvpn\'s default password managment, if used your password will be stored in /etc/openvpn/nordpasswd', action='store_true')

parser.add_argument('--adv_ovpn', type=str, help='''If you are familiar w/ openvpn\'s more advanced feature\'s
use this to append an additional agument
to the end of the current working ovpn file.
All changes will be reset at the end of your session.
Warning!! This takes a whole string and appends it to
your current server config file regardless if it is a valid command
''', metavar='')

parser.add_argument('-c', choices=country_args,help= textwrap.dedent('''Please choose a country and use the abbreviation as the argument. (Please use uppercase)

Albania		    :	AL
Argentina	    :	AR 
Australia	    :   AU 
Austria		    :	AT 
Azerbaijan	    :	AZ 
Belgium		    :	BE 
Bosnia               :   BA 
Brazil		    :	BR 
Bulgaria             :	BG 
Canada		    :	CA 
Chile		    :	CL
Costa Rica	    :	CR 
Croatia		    :	HR 
Cyprus		    :	CY 
Czech Republic       :	CZ 
Denmark		    :	DK 
Egypt		    :	EG 
Estonia		    :	EE 
Finland		    :	FI 
France		    :	FR 
Georgia		    :	GE 
Germany		    :	DE 
Greece		    :	GR 
Hong Kong	    :	HK 
Hungary		    :	HU 
Iceland		    :	IS 
India		    :	IN 
Indonesia	    :	ID 
Ireland		    :	IE 
Israel		    :	IL 
Italy		    :	IT 
Japan		    :	JP 
Latvia		    :	LV 
Luxembourg	    :	LU 
Macedonia	    :	MK 
Malaysia             :	MY 
Mexico		    :	MX 
Moldova		    :	MD 
Netherlands	    :	NL 
New Zealand	    :	NZ 
Norway		    :	NO 
Poland		    :	PL 
Portugal             :	PT 
Romania		    :	RO 
Russia		    :	RU 
Serbia		    :	RS 
Singapore	    :	SG 
Slovakia             :	SK 
Slovenia             :	SI 
South Africa         :	ZA 
South Korea	    :	KR 
Spain		    :	ES 
Sweden		    :	SE 
Switzerland	    :	CH 
Taiwan		    :	TW 
Thailand             :	TH 
Turkey               :	TR 
Ukraine              :	UA 
UAE                  :	AE 
United Kingdom       :	GB 
United States        :	US 
Vietnam              :	VN

Example: "nordvpn -rc US" for a random server  United States

'''), metavar='')

parser.parse_args()

args=parser.parse_args()


if len(sys.argv)==1:
    # display help message when no args are passed.
    parser.print_help()
    sys.exit(1)

startup_art = '''
 _   _               _ _      _ _____  _   _
| \ | |             | \ \    / /  __ \| \ | |
|  \| | ___  _ __ __| |\ \  / /| |__) |  \| |
| . ` |/ _ \| '__/ _` | \ \/ / |  ___/| . ` |
| |\  | (_) | | | (_| |  \  /  | |    | |\  |
|_| \_|\___/|_|  \__,_|   \/   |_|    |_| \_|
         A Better NordVPN manager
'''
print(startup_art)



cwdir = os.getcwd()
ovpndir = '/etc/openvpn/ovpn_tcp/'
country_id = None
serverselect = None
tmpfile = '/tmp/nordvpn/temp.ovpn'
wtime = 30  # wait time while letting ovpn connect to server
hc_country_id = {'AL': 2, 'AR': 10, 'AU': 13, 'AT': 14, 'AZ': 15, 'BE': 21, 'BA': 27, 'BR': 30, 'BG': 33,
                 'CA': 38, 'CL': 43, 'CR': 52, 'HR': 54, 'CY': 56, 'CZ': 57, 'DK': 58, 'EG': 64, 'EE': 68,
                 'FI': 73, 'FR': 74, 'GE': 80, 'DE': 81, 'GR': 84, 'HK': 97, 'HU': 98, 'IS': 99, 'IN': 100,
                 'ID': 101, 'IE': 104, 'IL': 105, 'IT': 106, 'JP': 108, 'LV': 119, 'LU': 126, 'MK': 128, 'MY': 131,
                 'MX': 140, 'MD': 142, 'NL': 153, 'NZ': 156, 'NO': 163, 'PL': 174, 'PT': 175, 'RO': 179, 'RU': 180,
                 'RS': 192, 'SG': 195, 'SK': 196, 'SI': 197, 'ZA': 200, 'KR': 114, 'ES': 202, 'SE': 208, 'CH': 209,
                 'TW': 211, 'TH': 214, 'TR': 220, 'UA': 225, 'AE': 226, 'GB': 227, 'US': 228, 'VN': 234,}

##---------------------------------------------------------------------------------------------------------------------


def main():
    if args.status:
        status()
    if args.exit:
        exit()
    if args.update:
        update()
    print('Setting up server for you...............................................................................')
    if args.c:
        country_code()
    if args.p:
        protocol()
    if args.r:
        randomserver()
    if args.recommend:
        recommend()
    if args.recommend or args.r == True:
        settmp()
    else:
        pass
    if args.password:
        if args.recommend or args.r == True:
            passwd()
        else:
            passwd()
            sys.exit()
    if args.adv_ovpn:
        adv_ovpn()
    print('Checking IP.............................................................................................')
    ipcheck()
    pre_ip = [ipcheck.ip, ipcheck.location, ipcheck.isp, str(ipcheck.status)]
    runovpn=subprocess.Popen(['openvpn',tmpfile])  # This run's openvpn
    try:
        runovpn.wait(wtime)
    except:
        pass
    ipcheck()
    post_ip = [ipcheck.ip, ipcheck.location, ipcheck.isp, str(ipcheck.status)]

    if post_ip[3] is 'True':
        print('\n')
        print('Your old IP address was ' + pre_ip[0] + ' located in ' + pre_ip[1] + ' hosted by ' + pre_ip[2])
        print('Your new IP address is ' + post_ip[0] + ' located in ' + post_ip[1] + ' hosted by' + post_ip[2])
        print('\n')
        print('To disconnect from your VPN run \'sudo ./nordvpn.py --exit\'')
    else:
        print('SOMETHING WENT WRONG, YOU ARE NOT PROTECTED!!!')


    shutil.rmtree('/tmp/nordvpn/')
##---------------------------------------------------------------------------------------------------------------------


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                                         "(or 'y' or 'n').\n")

# Thank you http://code.activestate.com/recipes/577058/


##---------------------------------------------------------------------------------------------------------------------


def country_code():

    global country_id, hc_country_id
    print('Retrieving list of country\'s and respective code\'s ................................... Total size 146KB')
    data_file = Request('https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_countries', headers={'User-Agent': 'Mozilla/5.0'})
    data_item = urlopen(data_file).read()
    data_json = json.loads(data_item.decode('utf-8'))

    for n in range(62):
        if args.c == data_json[n]['code']:
            country_id = data_json[n]['id']
        else:
            n +=1
#    for n in range(62):
#        hc_country_id.update({data_json[n]['code']: data_json[n]['id']})
#        n += 1
#    set(hc_country_id)

##---------------------------------------------------------------------------------------------------------------------


def update():
    choice = query_yes_no('Remove all current ovpn files and start fresh?(y) Or amend current files?(n)')
    os.chdir('/etc/openvpn/')
    if choice is True:
        for f in glob.glob('ovpn*'):
            try:
                shutil.rmtree(f, ignore_errors=True)
                os.remove(f)
            except:
                pass
#        subprocess.call(['rm', '-rf', 'ovpn.zip', 'ovpn.zip.1', 'ovpn.zip.2', 'ovpn_udp', 'ovpn_tcp'])
        subprocess.call(['wget', 'https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip'])
        subprocess.call(['unzip','ovpn.zip'])
    elif choice is False:
        for f in glob.glob('ovpn*'):
            try:
                shutil.rmtree(f, ignore_errors=True)
                os.remove(f)
            except:
                pass
#        subprocess.call(['rm', '-f', 'ovpn.zip'])
        subprocess.call(['wget', 'https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip'])
        subprocess.call(['unzip', 'ovpn.zip'])
    else:
        print('update failed!')

    os.chdir(cwdir)
    sys.exit()
##---------------------------------------------------------------------------------------------------------------------


def protocol():
    global ovpndir
    if args.p == 'tcp':
        # Do nothing, the default directory is '/etc/openvpn/ovpn_tcp/'
        ovpndir = '/etc/openvpn/ovpn_tcp/'
        print('directory set to ' + ovpndir)
    elif args.p == 'udp':
        ovpndir='/etc/openvpn/ovpn_udp/'
        print('directory set to ' + ovpndir)
    else:
        print('Please specify tcp or udp when using -p')
        exit()
##---------------------------------------------------------------------------------------------------------------------


def randomserver():
    global serverselect
    os.chdir(ovpndir)
    if args.c:
        cstring = os.popen('ls |grep '+args.c.lower()).read()
        clist = cstring.split()
        serverselect = random.choice(clist)
    else:
        serverselect = random.choice(os.listdir(ovpndir))
    os.chdir(cwdir)
##---------------------------------------------------------------------------------------------------------------------


def recommend():
    global serverselect
    if  country_id != None:
        print('Fetching recommended server based on the country you selected ........................ Total size 13KB')
        data_file = Request('https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations&filters={%22country_id%22:' + str(country_id) + ',%22servers_groups%22:[11]}', headers={'User-Agent': 'Mozilla/5.0'})
        data_item = urlopen(data_file).read()
        data_json = json.loads(data_item.decode('utf-8'))
        serverselect = data_json[0]['hostname']
    elif country_id == None:
        print('Fetching recommended server based on your location ................................... Total size 13KB')
        data_file = Request('https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations',headers={'User-Agent': 'Mozilla/5.0'})
        data_item = urlopen(data_file).read()
        data_json = json.loads(data_item.decode('utf-8'))
        serverselect = data_json[0]['hostname']
    else:
        print('error getting a reccommended server from Nordvpn.com')

    if ovpndir == '/etc/openvpn/ovpn_tcp/':
        serverselect = serverselect + '.tcp.ovpn'
    elif ovpndir == '/etc/openvpn/ovpn_udp/':
        serverselect = serverselect + '.udp.ovpn'
    else:
        print('error in setting ovpn directory')

##---------------------------------------------------------------------------------------------------------------------


def passwd():
    global ovpndir, serverselect, tmpfile,wtime
    if  os.path.isfile('/etc/openvpn/nordpasswd') == True:
        with open(tmpfile, 'a') as file:
            file.write('auth-user-pass /etc/openvpn/nordpasswd')
    elif os.path.isfile('/etc/openvpn/nordpasswd') == False:
        with open('/etc/openvpn/nordpasswd', 'w') as file:
            inputuser = input('Please enter username:')
            file.write(inputuser)
            file.write('\n')
            inputpw = input('Please enter password:')
            file.write(inputpw)
        with open(tmpfile, 'a') as file:
            file.write('auth-user-pass /etc/openvpn/nordpasswd')
    else:
        print('Fail to set password')
    wtime = 10  # reduce wait time when password is used
##---------------------------------------------------------------------------------------------------------------------


def ipcheck():
    '''
    ipcheck call's out to NordVPN and downloads a json file.
    Then parses out ip, location, isp, and if you are connected to an VPN
    '''
    ip_url = Request('https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data', headers={'User-Agent': 'Mozilla/5.0'})
    ip_page = urlopen(ip_url).read()
    ip_data = json.loads(ip_page.decode('utf-8'))

    ipcheck.ip = ip_data['ip']
    ipcheck.location = ip_data['location']
    ipcheck.isp = ip_data['isp']
    ipcheck.status = ip_data['status']
##---------------------------------------------------------------------------------------------------------------------



def exit():
    devnull = open('/dev/null', 'w')
    test = subprocess.call('pgrep openvpn', shell=True, stdout=devnull)
    if test < 1:
        print('No don\'t go! Okay fine. Good bye...')
        cmd = 'pgrep openvpn|xargs kill'
        subprocess.call(cmd,shell=True, stdout=devnull)
    else:
        print('Doesn\'t seem Openvpn is running, so I can\'t close it.')
    if os.path.isdir('/tmp/nordvpn/') == True:
        shutil.rmtree('/tmp/nordvpn/')
    sys.exit()
##---------------------------------------------------------------------------------------------------------------------



def settmp():
    '''
    settmp sets up a temporary folder and file at /tmp/nordvpn/temp.ovpn to enable

    amending ovpn files so as to not permanently change them.

    passwd and adv_ovpn both amend the working ovpn file.

    main and exit both remove temp files.
    '''
    global ovpndir,serverselect
    if os.path.isdir('/tmp/nordvpn/') == True:
        shutil.copy(ovpndir+serverselect, tmpfile)
    else:
        os.mkdir('/tmp/nordvpn/')
        shutil.copy(ovpndir+serverselect, tmpfile)
##---------------------------------------------------------------------------------------------------------------------



def adv_ovpn():
    with open(tmpfile, 'a') as file:
        file.write('\n' + args.adv_ovpn)
# If you use 'daemon' IP check will always come back false, but
# deamon is unnecessary since normal use detaches the terminal
##---------------------------------------------------------------------------------------------------------------------


def status():
    ipcheck()
    status_check = [ipcheck.ip, ipcheck.location, ipcheck.isp, str(ipcheck.status)]
    if status_check[3] is 'True':
        print('You are currently protected')
        print('Your exiting IP is ' + status_check[0])
        print('Located in ' + status_check[1])
    elif status_check[3] is 'False':
        print('YOU ARE NOT PROTECTED!')
        print('Your IP is reporting back as ' + status_check[0])
        print('Located in ' + status_check[1])
    else:
        print('Failed to retrieve IP data')
    sys.exit()


main()
