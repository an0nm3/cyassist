# Cyassist Daily Cron Setup

## Option 1: Crontab (add to crontab -e)

```
# Cyassist daily news scrape at 6am UTC
0 6 * * * cd /path/to/cyassist && python3 cyassist.py --daily >> /tmp/cyassist-daily.log 2>&1

# Cyassist watch mode (optional, runs continuously)
# @reboot cd /path/to/cyassist && screen -dmS cyassist-watch python3 reader.py
```

## Option 2: systemd timer

Create `/etc/systemd/system/cyassist-daily.service`:
```
[Unit]
Description=Cyassist daily news update

[Service]
Type=oneshot
ExecStart=/path/to/cyassist/cyassist.py --daily
WorkingDirectory=/path/to/cyassist
User=youruser
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
- News metadata only, no blobs
- After daily run: news archive updates, DB grows ~0.01-0.3MB/day depending on scraped content
