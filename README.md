# Generate Root CA

This script auto generate CA to bypass SSL Pinning on Android >= 7.0.

How to use:

* `git clone https://github.com/minhgalaxy/ca_generator.git`

* `python3 generate_cert.py`

* `adb push 35aa2e12.0 /sdcard/`

* `adb shell cp /sdcard/35aa2e12.0 /etc/security/cacerts/`

#Credit: https://github.com/Hamz-a/frida-android-helper
