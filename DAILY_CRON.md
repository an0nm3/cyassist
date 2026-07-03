# Cyassist Daily Cron Setup

## Option 1: Crontab (add to crontab -e)

```
# Cyassist daily scrape at 6am UTC
0 6 * * * cd /home/kali/bugbounty/cyassist && python3 cyassist.py --daily >> /tmp/cyassist-daily.log 2>&1

# Cyassist watch mode (optional, runs continuously)
# @reboot cd /home/kali/bugbounty/cyassist && screen -dmS cyassist-watch python3 cyassist.py --watch --watch-interval 600
```

## Option 2: systemd timer

Create `/etc/systemd/system/cyassist-daily.service`:
```
[Unit]
Description=Cyassist daily intel update

[Service]
Type=oneshot
ExecStart=/home/kali/bugbounty/cyassist/cyassist.py --daily
WorkingDirectory=/home/kali/bugbounty/cyassist
User=kali
```

Create `/etc/systemd/system/cyassist-daily.timer`:
```
[Unit]
Description=Cyassist daily schedule

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Then: `sudo systemctl enable cyassist-daily.timer --now`

## Stats

- Current DB: 0.13MB (targeting <100MB)
- 50 exploits indexed (DNA only), 117 news articles
- After daily run: news + exploits update, DB grows ~0.01-0.3MB/day depending on scraped content
