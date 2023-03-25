# RaspberryPi-Ink-Dash
RaspberryPi Ink Dashboard for waveshare 2.13inch e-Paper HAT

### step1: pip install waveshare-epd-driver

https://pypi.org/project/waveshare-epd-driver/

### step2: copy this python script to `/usr/local/bin/`

### step3: add line above into `/etc/local.rc`, before the `exit 0`.

```
/usr/bin/python3 /usr/local/bin/dashboard.py
```
