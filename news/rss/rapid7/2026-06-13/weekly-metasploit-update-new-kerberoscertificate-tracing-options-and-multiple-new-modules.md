---
source: rss/rapid7
title: Weekly Metasploit Update: New Kerberos/Certificate tracing options, and multiple new modules
url: https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-13-06-2026
date: 2026-06-13
item_id: https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-13-06-2026
category: news
tags: [Exploit]
---

**Source:** Rapid7
**Link:** https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-13-06-2026

New Tracing Options  As hard as we try to ensure that Metasploit is bug free, issues inevitably come up. Whether you’re running a module on an op or writing a new one, what we can do is make the debugging experience easier. To that end one of our two Google Summer of Code (GSoC) projects is here to deliver. Building on the previous pattern of HttpTrace comes two new options  KerberosTicketTrace  and  CertificateTrace . These options, when enabled, will enable debugging output of Kerberos tickets and Certificates that are both sent and received by applicable modules. Now when things aren’t going quite right, users have new levers to reach for to inspect what’s happening under the hood.  For example, to inspect exactly what’s happening when using the  auxiliary/admin/kerberos/get_ticket   module:   msf auxiliary(admin/kerberos/get_ticket) &gt; set KerberosTicketTrace true 
KerberosTicketTrace =&gt; true
msf auxiliary(admin/kerberos/get_ticket) &gt; run
[*] Running module against 192.168.159.10
[*] 192.168.159.10:88 - Getting TGT for smcintyre@msflab.local
####################
# Kerberos Request: AS-REQ
####################
Protocol Version: 5
Message Type: 10 (AS-REQ)
Pre-Authentication Data:
  Entry[0]:
    Type: 128 (PA_PAC_REQUEST)
    Value: [binary 7 bytes: 3005a0030101ff]
Request Body:
  KDC Options:
    Value: 1082195984
    Flags:
      - FORWARDABLE
      - RENEWABLE
      - CANONICALIZE
      - RENEWABLE_OK
  Client Name:
    Name Type: 1 (NT_PRINCIPAL)
    Name String:
      - smcintyre
  Realm: MSFLAB.LOCAL
  Server Name:
    Name Type: 1 (NT_PRINCIPAL)
    Name String:
      - krbtgt
      - MSFLAB.LOCAL
  Till: 2026-06-12T18:21:36Z
  Rtime: 2026-06-12T18:21:36Z
  Nonce: 6831592
  Encryption Type:
    - 18 (AES256)
    - 17 (AES128)
    - 23 (RC4_HMAC)
    - 3 (DES_CBC_MD5)
    - 16 (DES3_CBC_SHA1)
####################
# Kerberos Response: KRB-ERROR
####################
Protocol Version: 5
Message Type: 30 (KRB-ERROR)
Server Time: 2026-06-11T18:21:36Z
Server Microseconds: 862696
Error Code:
  Name: KDC_ERR_PREAUTH_REQUIRED
  Value: 25
  Description: Additional pre-authentication required
Realm: MSFLAB.LOCAL
Server Name:
  Name Type: 1 (NT_PRINCIPAL)
  Name String:
    - krbtgt
    - MSFLAB.LOCAL
Error Data: [binary 87 bytes: 30553032a103020113a22b04293027301ea003020112a1171b154d53464c41422e4c4f43414c736d63696e747972653005a0030201173009a103020102a20204003009a103020110a20204003009a10302010fa2020400]
####################
# Kerberos Request: AS-REQ
####################
Protocol Version: 5
Message Type: 10 (AS-REQ)
Pre-Authentication Data:
  Entry[0]:
    Type: 2 (PA_ENC_TIMESTAMP)
    Value: [binary 67 bytes: 3041a003020112a23a0438724f4965bd3deb1f061e807b616a09b613f59d9a6749eaee895e2ec3ed3045403cb28874acaa371681e3957a3ec23879141411ba788886f3]
  Entry[1]:
    Type: 128 (PA_PAC_REQUEST)
    Value: [binary 7 bytes: 3005a0030101ff]
Request Body:
  KDC Options: 1350565888
  Client Name:
    Name Type: 1 (NT_PRINCIPAL)
    Name String:
      - smcintyre
  Realm: MSFLAB.LOCAL
  Server Name:
    Name Type: 1 (NT_PRINCIPAL)
    Name String:
      - krbtgt
      - MSFLAB.LOCAL
  Till: 2026-06-12T18:21:36Z
  Rtime: 2026-06-12T18:21:36Z
  Nonce: 7068778
  Encryption Type:
    - 18 (AES256)
    - 23 (RC4_HMAC)
####################
# Kerberos Response: AS-REP
####################
Protocol Version: 5
Message Type: 11 (AS-REP)
Pre-Authentication Data:
  Entry[0]:
    Type: 19 (PA_ETYPE_INFO2)
    Value: [binary 34 bytes: 3020301ea003020112a1171b154d53464c41422e4c4f43414c736d63696e74797265]
Client Realm: MSFLAB.LOCAL
Client Name:
  Name Type: 1 (NT_PRINCIPAL)
  Name String:
    - smcintyre
Ticket:
  Ticket Version Number: 5
  Realm: MSFLAB.LOCAL
  Server Name:
    Name Type: 1 (NT_PRINCIPAL)
    Name String:
      - krbtgt
      - MSFLAB.LOCAL
  Encrypted Part:
    Encryption Type: 18 (AES256)
    Key Version Number: 2
    Cipher: [binary 1098 bytes: a3b825bd279344fd0bc454654f7906e31c8f4918c7c69319515e6a722515b55da36e2ae26f107d9f6278b029ba4c1b937a8a4e9df04f4a54da43794b2216fd5d7762582e94e3aa72fd14bfa0cfb9ff5c9a138acecd57351ff7ca98a9d7d890445316b04359e9210f93ba72c578a1605fb5502ba00fe67d9b55417e356e6400ef3bd07b9e1a8e4aedeb62249bef9f56f0cda3a30969d33fe6999a4855ae8f666b82fdff29047b14d4bcd77b31a6b9ce1ee3a4425cd197250af0cc878995afbeb4de42fb7e55d6095ab27ab3fa7f0afb0010b8e8f5e721a3d0417c7342df77619f6520e726652dc4417d2dbc044529236557441f87a50a7188242fb177e5f1bd45d31902c877d51cd05af7215e520c410e9b7036bc78c1ddad458b0ad99832c4fdd6f8f523ca4241aee8ebce4a0000202ebfb870761833feffc2c248683751a11d556bba4c59b20c7a1627b187d4d4679e19b1928f3ab7edeef3f01b459324178a9e49976519b58d6d7164b29c77e20625c4e710e3bbb0bb32452d4bdb9ed0c3e9873b9511cadf36fb0b372af5f67310319f160c0242d2fff1095bc467c4eb6da0382ab0587d519e5390e56eacb6db4f98c2c25b7ac22edf40db2e0e0eca03dfeba48327916a8caa85c382d04dcea16116c76132dcbfc168b7e3435a37f812f479f1e8309b124a9dcbac1e2ae83063a5e49c1ea584f13f64832c713577f07b3229e83c0fe73c3dc350640a69ea643ef24b66ed17114c262d3e5cdddb8182d8da49173e597b23d94f8ef652433713bf1d5e91c7f984945940d27755584137b00baa9696cdd121c641870830ffc86c8f9989254b6b804912c4989014b3f849cd02e6b06d3cc6401fd3f830cfcd36a0ecf31309d5b6dc82a65b427818694002bcf5fac9c936e1d64205a397126f39f684903803a5405baff041881339c4c8d325a2f446178b66383c209f3dba61bdda626f6e6d63c473638191e447d58aebfcb5a98104c2f96afa3283ac3aca675937afd7c497f1bd41a3dd1b52a6a16db791421a4ab9189d9fa0d610713d9c1eeb2f9c46d6ea197f48e2e643fe773ece0855c63b44b6020044fb7cc1396b26b4747941484b73108b7c1c90e2670cf723033274cc24ceb66a7054b35a9653cd7391a4f81b2c977ee251c9295e47be46b14c66b4031c6758415e543153bde190af0f1abe0f207d84145e3521850f89765997ab72cccaaeb4c5ce8b8be9b33712090d59424c2517e4cd539740750f5792f171fec2b4e4b4bc00cb77bc308abe1b70c75684734aa9ef03c4b419d2e10b4ea6229faf5a4b2af9483156ea32bc4b298f158067ac45afd5c812c407bda57880434cb93a60ac19799004a9adc72d845401ebb8e2a31ed0edf539233d293b1141bb49b36b6475d87c0fd114d97a946e82e39ed58e6c2e0d72826059600d412bd05aaf0af5602ade2f1ff6db363ec33e25756c4bc417b248344ba19ecd8d80d2cd2c2ff32aa355c22ee96166fc7043204dcc48b5595416c4312855c7d6e31d422c93c1d6f3df1a5890b45fc55f1b757b8e]
Encrypted Part:
  Encryption Type: 18 (AES256)
  Key Version Number: 3
  Cipher: [binary 271 bytes: 357637faf370a69ec4780f1fc4308e3d639e59ebbdb5d208cf6df75470bcefdd5210a098aa716055f758d9ec58674abc4b56cec2923329309e2be192db3ee1a63c6f0133a96c440707a0f29f2e075f90c54e2ab7626132f8e898112f81cbde6905d992d9ec6a4c26087043ea8f97c1a876354c47b4a6a76e3321f42edc483530d5248f8daa01db15ab019ac4179dfdb5f6d6c1f2666b9983cd02989612acdad2b2efe352fb9708a080fd304d17a87ff1e152dc8ca981de6cff418f38c5c28612766bfc13fbac51bad1a01fcd7aae544c7d839124e1bce745d20d06c8aca5c7125afe069e8d5299a10cd27b392bd8ae3893181f132f3d49dd746c6c70c6d2b651df998c59be84f2d5b83e5b3c0a71b2]
[+] 192.168.159.10:88 - Received a valid TGT-Response
[*] 192.168.159.10:88 - TGT MIT Credential Cache ticket saved to /home/smcintyre/.msf4/loot/20260611142136_default_192.168.159.10_mit.kerberos.cca_918073.bin
####################
# Kerberos Credential: TGT
####################
Creds: 1
  Credential[0]:
    Server: krbtgt/MSFLAB.LOCAL@MSFLAB.LOCAL
    Client: smcintyre@MSFLAB.LOCAL
    Ticket etype: 18 (AES256)
    Key: 58b969939485b53dee75e4399253524d132cc2ca145f4da4e4951c04a843e544
    Subkey: false
    Ticket Length: 1188
    Ticket Flags: 0x50e10000 (FORWARDABLE, PROXIABLE, RENEWABLE, INITIAL, PRE_AUTHENT, CANONICALIZE)
    Addresses: 0
    Authdatas: 0
    Times:
      Auth time: 2026-06-11 14:21:36 -0400
      Start time: 2026-06-11 14:21:36 -0400
      End time: 2026-06-12 00:21:36 -0400
      Renew Till: 2026-06-12 14:21:36 -0400
    Ticket:
      Ticket Version Number: 5
      Realm: MSFLAB.LOCAL
      Server Name: krbtgt/MSFLAB.LOCAL
      Encrypted Ticket Part:
        Ticket etype: 18 (AES256)
        Key Version Number: 2
        Cipher:
          o7glvSeTRP0LxFRlT3kG4xyPSRjHxpMZUV5qciUVtV2jbiribxB9n2J4sCm6TBuTeopOnfBPSlTaQ3lLIhb9XXdiWC6U46py/RS/oM+5/1yaE4rOzVc1H/fKmKnX2JBEUxawQ1npIQ+TunLFeKFgX7VQK6AP5n2bVUF+NW5kAO870HueGo5K7etiJJvvn1bwzaOjCWnTP+aZmkhVro9ma4L9/ykEexTUvNd7Maa5zh7jpEJc0ZclCvDMh4mVr7603kL7flXWCVqyerP6fwr7ABC46PXnIaPQQXxzQt93YZ9lIOcmZS3EQX0tvARFKSNlV0Qfh6UKcYgkL7F35fG9RdMZAsh31RzQWvchXlIMQQ6bcDa8eMHdrUWLCtmYMsT91vj1I8pCQa7o685KAAAgLr+4cHYYM/7/wsJIaDdRoR1Va7pMWbIMehYnsYfU1GeeGbGSjzq37e7z8BtFkyQXip5Jl2UZtY1tcWSynHfiBiXE5xDju7C7MkUtS9ue0MPphzuVEcrfNvsLNyr19nMQMZ8WDAJC0v/xCVvEZ8TrbaA4KrBYfVGeU5Dlbqy220+YwsJbesIu30DbLg4OygPf66SDJ5FqjKqFw4LQTc6hYRbHYTLcv8Fot+NDWjf4EvR58egwmxJKncusHiroMGOl5JwepYTxP2SDLHE1d/B7MinoPA/nPD3DUGQKaepkPvJLZu0XEUwmLT5c3duBgtjaSRc+WXsj2U+O9lJDNxO/HV6Rx/mElFlA0ndVWEE3sAuqlpbN0SHGQYcIMP/IbI+ZiSVLa4BJEsSYkBSz+EnNAuawbTzGQB/T+DDPzTag7PMTCdW23IKmW0J4GGlAArz1+snJNuHWQgWjlxJvOfaEkDgDpUBbr/BBiBM5xMjTJaL0RheLZjg8IJ89umG92mJvbm1jxHNjgZHkR9WK6/y1qYEEwvlq+jKDrDrKZ1k3r9fEl/G9QaPdG1KmoW23kUIaSrkYnZ+g1hBxPZwe6y+cRtbqGX9I4uZD/nc+zghVxjtEtgIARPt8wTlrJrR0eUFIS3MQi3wckOJnDPcjAzJ0zCTOtmpwVLNallPNc5Gk+Bssl37iUckpXke+RrFMZrQDHGdYQV5UMVO94ZCvDxq+DyB9hBReNSGFD4l2WZercszKrrTFzouL6bM3EgkNWUJMJRfkzVOXQHUPV5Lxcf7CtOS0vADLd7wwir4bcMdWhHNKqe8DxLQZ0uELTqYin69aSyr5SDFW6jK8SymPFYBnrEWv1cgSxAe9pXiAQ0y5OmCsGXmQBKmtxy2EVAHruOKjHtDt9TkjPSk7EUG7SbNrZHXYfA/RFNl6lG6C457VjmwuDXKCYFlgDUEr0FqvCvVgKt4vH/bbNj7DPiV1bEvEF7JINEuhns2NgNLNLC/zKqNVwi7pYWb8cEMgTcxItVlUFsQxKFXH1uMdQiyTwdbz3xpYkLRfxV8bdXuO
[*] Auxiliary module execution completed
msf auxiliary(admin/kerberos/get_ticket) &gt;   Stay tuned for future enhancements like KerberosTicketTraceLevel which should have verbosity toggles such as meta, ticket, and full. We’d like to thank our GSoC contributors  eve0805  and  Pushpenderrathore  for their hard work on this project.  Upcoming Evasion Module Changes  Metasploit is currently reconsidering the UX of evasion modules whereby users are currently required to use the module, set the payload, run it, then return to their exploit and copy the generated output from the evasion module into the exploit. This is a cumbersome process and we think we can do better but before we commit to a direction, we are soliciting feedback from the community on what they think would be the best path forward. To that end, we’ve  published  a writeup of the options we’re considering and a  form  through which we’re hoping to receive feedback. The form contains 3 questions and will be open until July 1st, 2026.  New module content (1)  ClickFix Server  Authors: boredchilada and h00die  Type: Exploit  Pull request:  #21212  contributed by  h00die   Path: multi/misc/clickfix_server  Description: Adds a new Metasploit exploit module exploit/multi/misc/clickfix_server that runs an HTTP server to deliver a "ClickFix"-style social-engineering page which copies a generated command payload to the victim’s clipboard that they are prompted execute.  Enhancements and features (9)    #21008  from  EclipseAditya  - Adds kernel_rex_version to Msf::Post::Linux::Kernel, a new helper that extracts the upstream kernel version from  uname -r    and returns a  Rex::Version . This eliminates an ArgumentError crash that occurred when 15+ Linux local exploit modules encountered distro-specific kernel version suffixes.   #21198  from  Pushpenderrathore  - This adds a  CertificateTracePresenter , implementing certificate tracing using the presenter pattern aligned with existing Metasploit conventions. This can be enabled by setting the  CertificateTrace  datastore option when using modules like  icpr_cert  and  get_ticket  to see the X.509 certificates being sent and received.   #21222  from  g0tmi1k  - Standardizes the log output across many Metasploit modules to improve the host and port log details when IPv6 addresses are present.   #21266  from  zeroSteiner  - This improves how we log SMB services. If the service is detected but authentication fails, the client still logs what dialect was negotiated so we log the service even if we couldn't authenticate to it.   #21383  from  zeroSteiner  - This bumps Ruby SMB to version 3.1.21 and closes a feature gap between Ruby SMB and the Rex SMB client. With the feature gap closed,  modules/auxiliary/admin/smb/samba_symlink_traversal.rb  can now be switched from Rex to the RubySMB client. One less module in the way of dropping the ancient Rex client.   #21466  from  eve0805  - This adds introduces KerberosTicketTrace support as a datastore option for Metasploit's Kerberos authentication flows. Enabling  KerberosTicketTrace  allows users to see the following requests and responses as they are sent and received: AS-REQ, AS-REP, TGS-REQ, TGS-REP, KRB-ERROR. Inbound messages are colored blue and outgoing messages are colored red to match the existing HttpTrace functionality. The coloring can be turned off and on with the KerberosTicketTraceColors datastore option.   #21528  from  h00die  - This PR updates Metasploit module metadata by adding Exploit-DB (EDB) reference IDs to existing modules that already have CVE references, improving cross-referencing for higher-fidelity vulnerability tracking.   #21535  from  adfoster-r7  - Updates multiple HTTP login scanners to validate the remote target as a pre-requisite to running the login attempts.   #21554  from  sjanusz-r7  - Make WebDAV upload PHP exploit checks less strict.   Bugs fixed (4)    #20618  from  Aaditya1273  - Updates the MSSQL modules to no longer crash when running stored procedures like  EXEC sp_linkedservers;  against a remote host.   #21543  from  sjanusz-r7  - Addresses a recent issue stemming from the recently-made changes to the webdav upload php module, where a false positive was being reported based on only the response code.   #21549  from  4ravind-b  - Adds the missing  https://github.com/advisories/GHSA-hxj9-549w-4pcq  reference to  modules/auxiliary/scanner/smtp/smtp_relay.rb .   #21557  from  adfoster-r7  - Fixes a db_import crash when importing zip files.   Documentation  You can find the latest Metasploit documentation on our docsite at  docs.metasploit.com .  Get it  As always, you can update to the latest Metasploit Framework with msfupdate and you can get more details on the changes since the last blog post from GitHub:    Pull Requests 6.4.136...6.4.137    Full diff 6.4.136...6.4.137    If you are a git user, you can clone the  Metasploit Framework repo  (master branch) for the latest. To install fresh without using git, you can use the open-source-only  Nightly Installers  or the commercial edition  Metasploit Pro
