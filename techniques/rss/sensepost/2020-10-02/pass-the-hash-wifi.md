---
source: rss/sensepost
title: Pass-the-hash WiFi
url: https://sensepost.com/blog/2020/pass-the-hash-wifi/
date: 2020-10-02
item_id: https://sensepost.com/blog/2020/pass-the-hash-wifi/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/pass-the-hash-wifi/

Thanks to a  tweet  Dominic responded to, I saw someone mention Passing-the-hash when I think they actually meant relay. The terminology can be confusing for sure, however, it made me realise that I had never Passed-the-hash with a Wi-Fi network. 
 So having learnt my lesson from previous projects I first made sure this was possible for NT -&gt; MSCHAP by looking at the  RFC . 
  8.1.  GenerateNTResponse()

   GenerateNTResponse(
   IN  16-octet              AuthenticatorChallenge,
   IN  16-octet              PeerChallenge,
   IN  0-to-256-char         UserName,

   IN  0-to-256-unicode-char Password,
   OUT 24-octet              Response )
   {
      8-octet  Challenge
      16-octet PasswordHash

      ChallengeHash( PeerChallenge, AuthenticatorChallenge, UserName,
                     giving Challenge)

      NtPasswordHash( Password, giving PasswordHash )
      ChallengeResponse( Challenge, PasswordHash, giving Response )
   }
  
 Looks like you can! As you can see in the above, the ChallengeResponse is created using the NT hash and not the password. I then checked  wpa_supplicant  to see if this was not a feature already, and it turns out it is! Looking at the  wpa_supplicant  configuration file it says:
