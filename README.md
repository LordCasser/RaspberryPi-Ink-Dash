# RaspberryPi-Ink-Dash
RaspberryPi Ink Dashboard for waveshare 2.13inch e-Paper HAT

You should install font before all!!!

[DejaVuSansMono](https://github.com/ryanoasis/nerd-fonts/releases/download/v2.3.3/DejaVuSansMono.zip)

Put it into you `/usr/share/fonts/truetype` folder, make a dir named `DejavuNerd`, and unzip all `.ttf` file into it.

### step1: pip install waveshare-epd-driver

https://pypi.org/project/waveshare-epd-driver/

### step2: copy this python script to `/usr/local/bin/`

### step3: add line above into `/etc/local.rc`, before the `exit 0`.

```
/usr/bin/python3 /usr/local/bin/dashboard.py
```
