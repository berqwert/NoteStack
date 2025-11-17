# 📝 NoteStack

Modern ve kullanıcı dostu Python masaüstü not alma uygulaması. CustomTkinter ile geliştirilmiş şık ve kullanışlı bir arayüze sahiptir.

## ✨ Özellikler

- 🎨 **Modern Arayüz**: CustomTkinter ile geliştirilmiş dark theme
- 📑 **Tab Yönetimi**: Notlarınızı tab'lar halinde görüntüleyin ve yönetin
- 🔍 **Arama**: Notlarınızda hızlıca arama yapın
- ⌨️ **Klavye Kısayolları**: 
  - `Ctrl+S` / `Cmd+S`: Notu kaydet
  - `Ctrl+N` / `Cmd+N`: Yeni not oluştur
  - `Ctrl+T` / `Cmd+T`: Başlık alanına odaklan
  - `Ctrl+F` / `Cmd+F`: Arama alanına odaklan
  - `Escape`: Yeni not moduna geç
- 🗑️ **Akıllı Silme**: Not düzenlerken "Kaldır", yeni not yazarken "Temizle"
- 💬 **Modern Dialog'lar**: Onay, bilgi, uyarı ve hata mesajları için özel dialog'lar
- 💾 **Otomatik Kayıt**: Notlarınız JSON formatında otomatik olarak kaydedilir
- ✅ **Validasyon**: Not içeriği ve uzunluk kontrolü
- 🎯 **Akıllı Başlangıç**: Uygulama açıldığında ilk notu otomatik seçer

## 🚀 Kurulum

### Gereksinimler

- Python 3.10 veya üzeri
- pip (Python paket yöneticisi)

### Adımlar

1. Projeyi klonlayın veya indirin:
```bash
git clone https://github.com/berqwert/NoteStack.git
cd NoteStack
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python main.py
```

## 📁 Proje Yapısı

```
NoteStack/
├── main.py              # Ana uygulama dosyası
├── config.py            # Yapılandırma ayarları
├── models.py            # Veri modelleri
├── storage.py           # Veri saklama işlemleri
├── utils.py             # Yardımcı fonksiyonlar
├── ui/
│   ├── components.py    # UI bileşenleri
│   ├── dialogs.py       # Dialog pencereleri
│   ├── handlers.py      # Event handler'lar
│   └── tab_handlers.py  # Tab yönetimi
├── data/
│   └── notes.json       # Notlar (otomatik oluşturulur)
└── requirements.txt     # Python bağımlılıkları
```

## 🛠️ Teknolojiler

- **Python 3.10+**: Programlama dili
- **CustomTkinter**: Modern UI framework
- **Pillow**: Görsel işleme (CustomTkinter bağımlılığı)
- **JSON**: Veri saklama formatı

## 📝 Kullanım

1. **Yeni Not Oluşturma**: "➕ New Note" butonuna tıklayın veya `Ctrl+N` tuşlarına basın
2. **Not Kaydetme**: "💾 Kaydet" butonuna tıklayın veya `Ctrl+S` tuşlarına basın
3. **Not Düzenleme**: Tab'lardan bir not seçin ve içeriğini düzenleyin
4. **Not Silme**: Tab üzerine gelin ve çıkan X butonuna tıklayın
5. **Arama**: Üst kısımdaki arama kutusuna yazın

## 🔧 Yapılandırma

`config.py` dosyasından aşağıdaki ayarları değiştirebilirsiniz:

- `WINDOW_WIDTH` / `WINDOW_HEIGHT`: Pencere boyutları
- `MAX_NOTE_LENGTH`: Maksimum not uzunluğu
- `DATA_DIR`: Veri klasörü yolu

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen önce bir issue açın veya pull request gönderin.

## 📧 İletişim

Sorularınız veya önerileriniz için issue açabilirsiniz.
