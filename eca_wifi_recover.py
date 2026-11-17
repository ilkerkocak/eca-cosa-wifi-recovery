#!/usr/bin/env python3
"""Unofficial Wi-Fi recovery for legacy E.C.A./Cosa devices. Use on owned devices only."""
import getpass
import json
import ssl
import urllib.parse
import urllib.request

BASE = 'https://192.168.10.1'
CTX = ssl._create_unverified_context()  # Legacy local device certificate expired in 2018.

def fetch(path, params):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f'{BASE}{path}?{query}', headers={'User-Agent': 'eca-wifi-recovery/0.1'})
    with urllib.request.urlopen(req, context=CTX, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

def parse_jsonp(value):
    start = value.find('(')
    end = value.rfind(')')
    if start == -1 or end <= start:
        raise ValueError('Beklenmeyen JSONP yanıtı')
    return json.loads(value[start + 1:end])

print('Yalnızca kendi ECA/Cosa cihazınızda kullanın.')
print('Önce bilgisayarı cihazın E.C.A._XXXX Wi-Fi ağına bağlayın.')
response = parse_jsonp(fetch('/scan', {'callback': 'ecaRecovery'}))
print('Cihaz sürümü:', response.get('version', 'bilinmiyor'))
networks = response.get('networks', [])
seen = set()
for network in sorted(networks, key=lambda x: x.get('signal', -999), reverse=True):
    if network.get('ssid') and network['ssid'] not in seen:
        seen.add(network['ssid'])
        print(f"  {network['ssid']}  [{network.get('security','?')}] {network.get('signal','?')} dBm")
ssid = input('Bağlanılacak 2.4 GHz SSID (tam yazılışı): ').strip()
matched = [n for n in networks if n.get('ssid') == ssid]
if not matched:
    raise SystemExit('SSID taramada bulunamadı. İşlem yapılmadı.')
network = max(matched, key=lambda n: n.get('signal', -999))
if network.get('security') not in ('psk2',):
    raise SystemExit('Bu örnek yalnızca WPA2-PSK (psk2) için doğrulandı. İşlem yapılmadı.')
endpoint = input('ECA web portalındaki kendi ev/endpoint kimliğiniz: ').strip()
if not endpoint or any(c not in '0123456789abcdefABCDEF' for c in endpoint):
    raise SystemExit('Endpoint kimliği doğrulanamadı. İşlem yapılmadı.')
api_url = 'https://kiwi.cosa.com.tr'
password = getpass.getpass('Wi-Fi şifresi (ekranda görünmez): ')
if len(password) < 8:
    raise SystemExit('WPA2 şifresi en az 8 karakter olmalı. İşlem yapılmadı.')
print('UYARI: Eski cihaz API’si kimlik ve Wi-Fi şifresini HTTPS URL sorgu parametreleriyle alıyor.')
print('Yerel cihaz sertifikası süresi dolduğu için doğrulama yalnızca bu bağlantıda atlanıyor.')
confirm = input('Ağ ayarlarını şimdi cihaza GÖNDER? [evet/Hayır]: ').strip().lower()
if confirm != 'evet':
    raise SystemExit('İptal edildi.')
params = {'callback': 'ecaRecovery', 'ssid': ssid, 'password': password,
          'security': network['security'], 'endpoint': endpoint, 'apiUrl': api_url}
try:
    result = fetch('/configure', params)
    print('Cihaz yanıtı:', result[:500])
except Exception as exc:
    print('Cevap alınamadı; cihaz yeni ağa geçerken bağlantı kesilmiş olabilir.')
    print('Hata tipi:', type(exc).__name__)
print('Sonraki adım: bilgisayarı eski ağa döndürün, yönlendirici istemci listesinden ve uygulamadan çevrimiçi durumu doğrulayın.')
