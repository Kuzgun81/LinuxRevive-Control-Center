# LinuxRevive Control Center

Linux kullanan son kullanıcılar için kolay, anlaşılır ve güvenli sistem yönetim
paneli. Amaç, günlük bakım ve sistem bilgilerini terminal komutlarını ezberleme
gerektirmeden tek bir arayüzden sunmaktır.

Bu proje, WinRevive Control Center'ın Linux için ayrı geliştirilen kardeş
projesidir. Windows optimizasyonlarını kopyalamaz; Linux masaüstü kullanımını
kolaylaştırmaya odaklanır.

## İlk sürüm kapsamı

- İşletim sistemi, çekirdek, işlemci, bellek ve disk özeti
- Kullanıcıya ait başlangıç uygulamalarını görüntüleme
- Geçici dosya alanlarını tarama ve açık onayla temizleme
- Güncelleme durumunu görüntüleme ve dağıtıma uygun grafiksel güncelleme
  aracını açma
- Tüm işlemlerde açık durum mesajı ve hata bildirimi

Sistem dosyalarını silen, rastgele komut çalıştıran veya güvenlik ayarlarını
devre dışı bırakan bir optimizasyon modu yoktur.

## Çalıştırma

GTK 3 Python bağlayıcıları ve `psutil` gerekir:

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 python3-psutil
python3 -m linuxrevive
```

Arch Linux için:

```bash
sudo pacman -S python-gobject gtk3 python-psutil
python3 -m linuxrevive
```

Uygulamayı dağıtım menüsünde göstermek için `data/linuxrevive.desktop`
dosyasını kullanıcı uygulamaları klasörüne kopyalayabilirsiniz.

## Geliştirme

Testleri standart kütüphane ile çalıştırın:

```bash
python3 -m unittest discover -s tests -v
```

## Lisans

Bu proje **All Rights Reserved** özel lisansı ile yayımlanır. Ayrıntılar için
`LICENSE` dosyasına bakın. Kaynak kodu, derlemeler ve release dosyaları izin
olmadan kullanılamaz, değiştirilemez veya yeniden dağıtılamaz.
