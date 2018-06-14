Couldn't find a solution I liked, to manage NordVPN from the command line, so I made this.
It still need's a lot of work, but main funcationality I believe is done.

This is my first script/program, as such I'm sure it's not very pythonic and there are better ways of doing things.So 
I would love your feed back and corrections.

I currently have a three year subcription to NordVPN so I will try and keep this up to date at lest that long.

Obviously Openvpn must be run as root so Sudo is required to run the script.
So I would recommend looking though it and seeing if it does what you think it should.

Dependencies are: python3, openvpn, wget(will probably remove at a later date), unzip, pgrep and kill







    Just a simple yet better openvpn manager for NordVPN

    optional arguments:
    -h, --help   show this help message and exit

    --status     Allows you to double check if you are still connected to a VPN
  
    --update     Downloads new server list from NordVPN and updates all ovpn_tvp & ovpn_udp files in /etc/openvpn/*

    -p           Specifies to use protocol TCP or UDP with your vpn server. 
                  Example: "nordvp -rp udp" to use a random UDP server.
  
    -r           Uses a random server within specified protocol 
                (Optionaly use with args -p and -c to protocol and country.)

    --recommend  Get's a recommended server based on your latitude & longitude 
               when a country is specified it get's server from said country

    --exit       pgreps for openvpn and kill's the instance.

    --password   Uses openvpn's default password managment, 
                if used your password will be stored in /etc/openvpn/nordpasswd

    --adv_ovpn   If you are familiar w/ openvpn's more advanced feature's
                use this to append an additional agument
                to the end of the current working ovpn file.
                All changes will be reset at the end of your session.
                Warning!! This takes a whole string and appends it to
                your current server config file regardless if it is a valid command

    -c           Please choose a country and use the abbreviation as the argument. (Please use uppercase)
               
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
