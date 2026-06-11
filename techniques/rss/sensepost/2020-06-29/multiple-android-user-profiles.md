---
source: rss/sensepost
title: Multiple Android User Profiles
url: https://sensepost.com/blog/2020/multiple-android-user-profiles/
date: 2020-06-29
item_id: https://sensepost.com/blog/2020/multiple-android-user-profiles/
category: techniques---

**Source:** SensePost
**Link:** https://sensepost.com/blog/2020/multiple-android-user-profiles/

I was recently on a mobile assessment where you could only register one profile on the app, per device. To use another account you had to first deactivate the profile and then register a new one. I wasn&#8217;t sure whether that would invalidate the original token especially since my goal was to test authorisation issues against the backend. Sure, I could have tested whether the token was invalidated or not, which later I found out it wasn&#8217;t. But there were other restrictions within this environment which made me look for a different approach.
