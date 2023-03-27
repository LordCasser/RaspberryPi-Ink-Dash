import logging
import sys
import os
from waveshare_epd_driver import epd2in13_V3
import time
from PIL import Image, ImageDraw, ImageFont
import math
import socket
import subprocess
import random
# LOGO_PATH = "/usr/share/startup"
FONT_PATH = "/usr/share/fonts/truetype/DejavuNerd"
# LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# FONT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
INFO_TIME = 10
HALT_TIME = 180
sleep_time = INFO_TIME


def subprocess_popen(statement):
    p = subprocess.Popen(statement, shell=True,
                         stdout=subprocess.PIPE)
    while p.poll() is None:
        if not p.wait() == 0:
            logging.info("exec", statement, "failed. Return Code is ", p.returncode)
            return []
        else:
            re = p.stdout.readlines()
            result = []
            for i in range(len(re)):
                res = re[i].decode('utf-8').strip('\r\n')
                result.append(res)
            return result


logging.basicConfig(level=logging.DEBUG)


def get_external_ip():
    """
    查询本机外网ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        # logging.info(s.getsockname())
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_internal_wlan_ip():
    data = subprocess_popen("ip addr show dev wlan0 | grep inet | head -1")
    # logging.info(data[0].split())
    if data == []:
        return None
    net = data[0].split()[-1]
    ip = data[0].split()[1].split("/")[0]
    return (net, ip)


def get_internal_eth_ip():
    data = subprocess_popen("ip addr show dev eth0 | grep inet | head -1")
    # logging.info(data)
    if data == []:
        return ("eth0", "Down")
    net = data[0].split()[-1]
    ip = data[0].split()[1].split("/")[0]
    return (net, ip)


def get_total_mem():
    # # 总内存
    return subprocess_popen("cat /proc/meminfo | grep MemTotal")


def get_cpu_temp():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000


def get_rest_mem():
    return subprocess_popen("cat /proc/meminfo | grep MemAvailable")


def get_load():
    return subprocess_popen("w | head -1")


def get_hostname():
    return subprocess_popen("uname -n")


def get_wlan():
    return subprocess_popen("iwgetid")


def get_wlan_list():
    subprocess_popen("wpa_cli reconfigure")
    wlans = subprocess_popen("wpa_cli list_networks | sed -n '1,2d;p'")
    # logging.info(wlans)
    wlan = []
    for i in wlans:
        wlan.append(i.split("\t")[1])
    # logging.info(wlan)
    return wlan


if __name__ == '__main__':
    # get_wlan_list()
    # logging.info("epd2in13_V3 HWS start page")
    try:
        epd = epd2in13_V3.EPD()

        logging.info("init and Clear")
        epd.init()
        epd.Clear(0xFF)

        logging.info(os.path.join(
            FONT_PATH, 'DejaVu Sans Mono Nerd Font Complete Mono.ttf'))
        font15 = ImageFont.truetype(os.path.join(
            FONT_PATH, 'DejaVu Sans Mono Nerd Font Complete Mono.ttf'), 15)
        font20 = ImageFont.truetype(os.path.join(
            FONT_PATH, 'DejaVu Sans Mono Nerd Font Complete Mono.ttf'), 20)
        font30 = ImageFont.truetype(os.path.join(
            FONT_PATH, 'DejaVu Sans Mono Nerd Font Complete Mono.ttf'), 30)
        font_icon = ImageFont.truetype(os.path.join(
            FONT_PATH, 'DejaVu Sans Mono Nerd Font Complete Mono.ttf'), 35)
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in13_V3.epdconfig.module_exit()
        sys.exit()
    except Exception as e:
        logging.info(e)

    buffer = None
    flag = True
    counter = 0
    while True:

        try:
            epd.init()
            # epd.Clear(0xFF)
            base_image = Image.new('1', (epd.height, epd.width), 255)
            base_image = base_image.transpose(Image.ROTATE_180)

            text_page = Image.new('1', (epd.height, epd.width), 255)
            draw = ImageDraw.Draw(text_page)
            # logging.info("loading LOGO image")
            # logo = Image.open(os.path.join(LOGO_PATH, 'logo.bmp'))
            # logo = logo.resize((epd.height, epd.width), Image.ANTIALIAS)
            # logo = logo.transpose(Image.ROTATE_180)
            # logging.info("displaying LOGO image")
            # epd.display(epd.getbuffer(logo))
            # time.sleep(3)

            # 255: clear the frame

            logging.info("displaying text")
            # draw.text((0, 0), u'Welcome to HWS', font = font30, fill = 0)
            # draw.text((0, 50), u'May the pwn be with you', font = font20, fill = 0)

            # banner
            ssid = get_wlan()
            if ssid != []:
                ssid = ssid[0].split(":")[1].strip('"')
                icon = "\ufaa8"
                if len(ssid) > 10:
                    ssid = ssid[:7] + "..."
            else:
                ssid = ""
                icon = ""
            hostname = get_hostname()[0]
            draw.text((0, 0), hostname, font=font30, fill=0)
            draw.text((250-len(ssid)*12-30, -2), icon, font=font_icon, fill=0)
            draw.text((250-len(ssid)*12-4, 8), ssid, font=font20, fill=0)

            # IP
            # message = '%s: %s' % (get_wlan()[0].split(":")[1].replace('"',''), get_external_ip())
            wlan_info = get_internal_wlan_ip()
            if wlan_info == None:
                wlans = get_wlan_list()
                if len(wlans) >= 2:
                    random.shuffle(wlans)
                    message = 'wlans: %s\%s' % (wlans[0], wlans[1])
                else:
                    message = 'wlan: %s' % wlans[0]
            else:
                message = '%s: %s' % get_internal_wlan_ip()
            draw.text((0, 40), message, font=font20, fill=0)
            message = '%s: %s' % get_internal_eth_ip()
            draw.text((0, 60), message, font=font20, fill=0)
            # Mem
            mem_total = math.ceil(int(get_total_mem()[0].replace(
                ' ', '').replace('kB', ':kB').split(':')[1])/1024/1024)
            mem_free = int(get_rest_mem()[0].replace(
                ' ', '').replace('kB', ':kB').split(':')[1])/1024/1024
            message = 'Memory: %0.1fG/%dG' % (mem_free, mem_total)
            draw.text((0, 80), message, font=font20, fill=0)
            # Load
            message = 'Temperature: %.1f\ufa03' % get_cpu_temp()
            # message = 'AVG load: %s' % get_load()[0].split(
            #     "load average: ")[1].split(',')[2].replace(' ', '')
            draw.text((0, 100), message, font=font20, fill=0)

            # message = 'Wlan: %s' % get_wlan()[0].split(":")[1].replace('"','')
            # draw.text((0, 100),message,font=font20,fill=0)

            text_page = text_page.transpose(Image.ROTATE_180)
            if flag:
                epd.display(epd.getbuffer(text_page))
                buffer = text_page
                flag = False
            else:
                # logging.info(text_page == buffer)
                if text_page == buffer:
                    pass
                else:
                    counter = counter + 1
                    if counter == 3:
                        epd.display(epd.getbuffer(text_page))
                        counter = 0
                    else:
                        epd.displayPartBaseImage(epd.getbuffer(base_image))
                        epd.displayPartial(epd.getbuffer(text_page))
                        logging.info("partial flush")
            epd.sleep()
            time.sleep(sleep_time)

            if wlan_info == None:
                sleep_time = INFO_TIME
            else:
                sleep_time = HALT_TIME

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd2in13_V3.epdconfig.module_exit()
            sys.exit()
        except Exception as e:
            logging.info(e)
