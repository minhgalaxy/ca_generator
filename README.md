# Generate Root CA

This script auto generate CA to bypass SSL Pinning on Android >= 7.0.

How to use:

* `git clone https://github.com/minhgalaxy/ca_generator.git`

* `python3 generate_cert.py`

* `adb push 35aa2e12.0 /sdcard/`

* Copy file `/sdcard/35aa2e12.0` to  `/etc/security/cacerts/`

* `chmod 777 /etc/security/cacerts/35aa2e12.0`

* Reboot device 

Credit: [https://github.com/Hamz-a/frida-android-helper](https://github.com/Hamz-a/frida-android-helper)
