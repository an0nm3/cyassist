---
source: rss/sensepost
title: Constrained Delegation Considerations for Lateral Movement
url: https://sensepost.com/blog/2022/constrained-delegation-considerations-for-lateral-movement/
date: 2022-05-18
item_id: https://sensepost.com/blog/2022/constrained-delegation-considerations-for-lateral-movement/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2022/constrained-delegation-considerations-for-lateral-movement/

The abuse of constrained delegation configuration, whereby a compromised domain user or computer account configured with constrained delegation can be leveraged to impersonate domain users to preconfigured trusted services, is a common attack path in Active Directory. For each trusted service, a unique service ticket is used, that explicitly corresponds to the service type for which it was requested. For example, to access Windows file shares,  a  CIFS  ticket is required. Meanwhile, to leverage the WinRM protocol, a  HTTP  service ticket is required instead. Compromise of such service tickets aids in lateral movement and further compromise.
