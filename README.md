# Eski E.C.A. / Cosa akıllı termostat – Wi-Fi kurulumunu kurtarma

> **Topluluk rehberi, resmî E.C.A./Cosa yazılımı değildir.** 18 Kasım 2026 itibarıyla bir kullanıcı tarafından E.C.A. akıllı termostat üzerinde başarıyla denendiği bildirilmiştir. Her modelde çalışacağı garanti edilmez.

## Hangi sorunu çözüyor?

Termostat `E.C.A._XXXX` isimli geçici Wi-Fi ağını oluşturuyor fakat E.C.A. web/mobil kurulum arayüzü termostata bağlanamıyor veya yeni ev ağına geçiremiyorsa, cihazın web uygulamasında kullanılan yerel Wi-Fi yapılandırma arabirimini kullanmayı dener.

**Test edilen ortam:** E.C.A./Cosa tabanlı cihaz, yazılım sürümü `3.1.0.6-1`; Linux bilgisayar; hedef ağ 2.4 GHz WPA2-PSK. Kurulumun başarıyla tamamlandığı kullanıcı tarafından bildirilmiştir. Tekil vaka, genellenemez.

## Güvenlik ve sınırlamalar

- Kombinin elektrik/klemens bağlantılarına müdahale etmeyin.
- Yalnızca size ait cihazlarda kullanın. Önce cihazın uygulamasındaki ayarları ve ev/endpoint kaydını koruyun.
- Eski cihazın `*.cosa.com.tr` sertifikasının 2 Aralık 2018'de sona erdiği görüldü. Script yalnızca **yerel cihaz bağlantısı** için TLS sertifika doğrulamasını atlıyor. Bu, güvenli bir kalıcı çözüm değildir; güvenmediğiniz ağlarda kullanmayın.
- Orijinal uygulamanın API'si şifreyi HTTPS GET sorgu parametresi olarak gönderiyor. Şifreyi terminal komutuna yazmayın, logları/komut geçmişini yayımlamayın, HAR dosyalarını paylaşmayın.
- Ev/endpoint kimliği **kişiye özeldir**. Başka bir kullanıcının kimliğini kopyalamayın. Script sizden kendi kimliğinizi ister.
- Misafir ağı cihaz izolasyonu uzaktan çalışmayı etkileyebilir; kurulum sonrası uygulamada çevrimiçi durumu kontrol edin.
- Script yalnızca WPA2-PSK (`psk2`) ağlar için hazırlandı; WPA3 ve farklı şifreleme türleri doğrulanmadı.

## Hazırlık ve kullanım

1. Yönlendiricide 2.4 GHz WPA2-PSK ağının açık olduğundan emin olun. Ağ adı ve şifresini hazır bulundurun.
2. E.C.A. web portalındaki **kendi ev/endpoint kimliğinizi** not edin. Bu değer URL'deki `/endpoint/<kimlik>/...` bölümünden görülebilir; kamuya açık paylaşmayın.
3. Linux/macOS bilgisayarınızı termostatın açtığı `E.C.A._XXXX` geçici Wi-Fi ağına bağlayın. İnternet bağlantısının bulunmaması normaldir.
4. Bu depodaki `eca_wifi_recover.py` dosyasını bilgisayarınıza kaydedin ve `python3 eca_wifi_recover.py` komutunu çalıştırın.
5. Cihazın gördüğü ağlardan hedef SSID'yi, ardından **kendi** endpoint kimliğinizi ve Wi-Fi şifrenizi girin. Şifre ekranda gösterilmez.
6. Komut göndermeden önce onay verin. Cihaz yeni Wi-Fi ağına geçerken geçici ağa bağlantı kopabilir.
7. Bilgisayarı normal ağa bağlayın. Yönlendiricinin istemci listesi ve E.C.A. uygulamasından cihazın çevrimiçi olduğunu doğrulayın.

**Not:** Python 3 standart kütüphanesini kullanır; ek Python paketi gerektirmez. Uygulama başka cihazlarda bağımsız olarak doğrulanmamıştır.

## Teknik bulgular

Cihazın geçici ağı üzerinden `192.168.10.1` DHCP/gateway çalışıyordu. HTTPS kökü `{"ok":1}` yanıtı verdi. Web uygulamasının JavaScript kodunda yeni cihazlar için `https://chiku.cosa.com.tr/scan?callback=...` ve `/configure` istekleri bulundu. Cihazın kendi DNS servisi `chiku.cosa.com.tr` adını `192.168.10.1` IP'sine çözdü. `/scan` JSONP yanıtında yazılım sürümü ve görülen 2.4 GHz ağları listelendi.

### Kaynak ve köken

Bu rehber, kullanıcının kendi cihazında yürüttüğü ağ testleri ve `https://akilli.eca.com.tr/` web uygulamasının tarayıcıda yüklediği JavaScript dosyasının incelenmesiyle hazırlanmıştır. E.C.A./Cosa ile bağlı değildir. Web uygulamasının kodu veya HAR yakalaması **bu depoya eklenmemiştir**.

## Sorun giderme

- **`/scan` yanıt vermiyor:** Cihazın geçici ağına bağlandığınızı ve `192.168.10.1` adresine erişilebildiğini kontrol edin.
- **Hedef SSID görünmüyor:** 2.4 GHz yayınını ve cihazın kapsama alanını kontrol edin.
- **`/configure` sırasında bağlantı koptu:** Başarısızlık kanıtı değildir; yönlendiricinin istemci listesini ve uygulamayı kontrol edin.
- **Ağa bağlandı ama uygulamada çevrimdışı:** İnternet/bulut hizmeti, misafir ağ izolasyonu, yanlış endpoint ve DNS erişimini ayrıca inceleyin.

## Sorumluluk

Bu topluluk aracı herhangi bir garanti içermez. Isıtma emniyeti ve kombi fonksiyonları üreticinin kontrolünde kalmalıdır.
