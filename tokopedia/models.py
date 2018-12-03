from django.db import models
import uuid, os

# Create your models here.

class Category(models.Model):
    category_id = models.IntegerField(blank = True, null = True)
    category_name = models.CharField(max_length = 150, blank = True, null = True)

    def __str__(self):
        return self.category_name

class Department(models.Model):
    department_id = models.IntegerField(blank = True, null = True)
    department_name = models.CharField(max_length = 150, blank = True, null = True)

    def __str__(self):
        return self.department_name


class Shop(models.Model):
    toko_url = models.URLField()

    toko_id = models.IntegerField(null = True, blank = True)
    toko_nama = models.CharField(max_length = 200, blank = True, null = True)
    toko_slogan = models.TextField(blank = True, null = True)
    toko_quote = models.TextField(blank = True, null = True)
    toko_gambar = models.URLField(blank = True, null = True)
    toko_cover = models.URLField(blank = True, null = True)

    toko_lokasi = models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'Lokasi Toko')
    toko_kota = models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'Kota Toko')


    toko_terjual = models.CharField(max_length = 50, blank = True, null = True)
    toko_terjual_int = models.CharField(max_length = 50, blank = True, null = True, default = 0)
    toko_follower = models.CharField(max_length = 50, blank = True, null = True)
    toko_follower_int = models.CharField(max_length = 50, blank = True, null = True, default = 0)

    toko_1_bulan_speed = models.IntegerField(blank = True, null = True)
    toko_1_bulan_order_count = models.IntegerField(blank = True, null = True)
    toko_3_bulan_speed = models.IntegerField(blank = True, null = True)
    toko_3_bulan_order_count = models.IntegerField(blank = True, null = True)
    toko_12_bulan_speed = models.IntegerField(blank = True, null = True)
    toko_12_bulan_order_count = models.IntegerField(blank = True, null = True)

    toko_reputasi_score = models.IntegerField(blank = True, null = True)
    toko_reputasi_level = models.IntegerField(blank = True, null = True, choices = (
        (20, 'Diamond 5'),
        (19, 'Diamond 4'),
        (18, 'Diamond 3'),
        (17, 'Diamond 2'),
        (16, 'Diamond 1'),

        (15, 'Gold 5'),
        (14, 'Gold 4'),
        (13, 'Gold 3'),
        (12, 'Gold 2'),
        (11, 'Gold 1'),

        (10, 'Silver 5'),
        (9, 'Silver 4'),
        (8, 'Silver 3'),
        (7, 'Silver 2'),
        (6, 'Silver 1'),

        (5, 'Bronze 5'),
        (4, 'Bronze 4'),
        (3, 'Bronze 3'),
        (2, 'Bronze 2'),
        (1, 'Bronze 1'),

        (0, 'Belum ada reputasi'),
    ))
    toko_reputasi_badge_url = models.URLField(blank = True, null = True)

    toko_jumlah_barang = models.IntegerField(blank = True, null = True, verbose_name = 'Jumlah Barang')

    toko_is_official = models.BooleanField(default = False, verbose_name = 'Toko Official')
    toko_is_gold = models.BooleanField(default = False, verbose_name = 'Gold Merchant')

    last_update = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.toko_nama

    # def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
    #     obj.toko_terjual_int = custom_humanize(obj.toko_terjual, return_int = True)
    #     obj.toko_follower_int = custom_humanize(obj.toko_follower, return_int = True)
    #     super().save(force_insert, force_update, using, update_fields)


class Good(models.Model):
    toko_induk = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'daftar_barang')

    barang_id = models.IntegerField()
    barang_url = models.URLField()
    barang_url_full = models.URLField()

    barang_nama = models.CharField(max_length = 200, blank = True, null = True)
    barang_child = models.CharField(max_length = 200, blank = True, null = True)
    barang_parent_id = models.IntegerField(null = True, blank = True)

    barang_gambar_utama = models.URLField(null = True, blank = True)

    barang_jumlah_kurir = models.IntegerField(blank = True, null = True)
    barang_kondisi = models.IntegerField(blank = True, null = True, choices = (
        (1, 'Baru'),
        (2, '2?'),
        (3, '3?'),
        (4, '4?'),
        (5, '5?'),

    ))
    # 1 = baru

    barang_is_unggulan = models.BooleanField(default = False, verbose_name = 'Produk Unggulan')

    barang_harga_asli = models.IntegerField(blank = True, null = True)
    barang_harga_jual = models.IntegerField(blank = True, null = True, default = 0)

    # diskon
    barang_diskon_harga_asli = models.IntegerField(null = True, blank = True)
    barang_diskon_start = models.CharField(max_length = 150, null = True, blank = True)
    barang_diskon_expired = models.CharField(max_length = 150, null = True, blank = True)
    barang_diskon_percentage = models.IntegerField(null = True, blank = True)

    barang_stok = models.IntegerField(null = True, blank = True)
    barang_status = models.IntegerField(null = True, blank = True)
    # belum tahu berapa-berapa choice nya nya

    barang_is_preorder = models.BooleanField(default = False)
    barang_minimal_order = models.IntegerField(blank = True, null = True)

    # get by api
    barang_dilihat = models.CharField(max_length = 50, blank = True, null = True)
    barang_dilihat_int = models.IntegerField(blank = True, null = True)
    barang_terjual = models.IntegerField(blank = True, null = True)
    barang_transaksi_sukses = models.IntegerField(blank = True, null = True)
    barang_transaksi_gagal= models.IntegerField(blank = True, null = True)

    barang_rating = models.IntegerField(null = True, blank = True, default = 0, verbose_name = 'Jumlah Bintang')
    barang_rating_count = models.IntegerField(null = True, blank = True, default = 0, verbose_name = 'Jumlah Pemberi Bintang')

    # ulasan ? (BUKAN review/bintang)
    # barang_jumlah_ulasan = models.IntegerField(null = True, blank = True)

    barang_informasi_produk = models.TextField(blank = True, null = True)

    barang_category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'kategori_barang')
    barang_department = models.ForeignKey(Department, on_delete = models.CASCADE, related_name = 'department_barang')

    last_update = models.DateTimeField(blank = True, null = True)
    last_upload = models.DateTimeField(blank = True, null = True)

    # todo: mekanisme untuk tahu bahwa dia belum sinkron
    # - ada 2 field
    # terakhir_update
    # terakhir_diedit
    # pertama insert, keduanya sama. lalu, tiap admin edit, update salah satu ke now. nanti query nya upload untuk yang kedua data beda, lalu set ke now lagi


    def __str__(self):
        if self.barang_nama:
            return self.barang_nama
        else:
            return self.barang_url

class GoodImage(models.Model):
    barang_induk = models.ForeignKey(Good, on_delete = models.CASCADE, related_name = 'daftar_gambar_barang')
    gambar_url = models.URLField()

class Etalase(models.Model):
    toko_induk = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'daftar_etalase')

    etalase_id = models.IntegerField(blank = True, null = True)
    etalase_nama = models.CharField(max_length = 150, blank = True, null = True)
    etalase_alias = models.CharField(max_length = 150, blank = True, null = True)
    etalase_url = models.URLField(max_length = 150, blank = True, null = True)
    etalase_jumlah_produk = models.IntegerField(null = True, blank = True)

class Note(models.Model):
    toko_induk = models.ForeignKey(Shop, on_delete = models.CASCADE, related_name = 'daftar_catatan')

    catatan_id = models.IntegerField(blank = True, null = True)
    catatan_judul = models.CharField(max_length = 150, blank = True, null = True)
    catatan_posisi = models.IntegerField(blank = True, null = True)
    catatan_uri = models.URLField(max_length = 150, blank = True, null = True)
    catatan_last_update = models.CharField(max_length = 150, blank = True, null = True)


# todo: untuk jenis/warna gimana? misal biru, putih, dsb -> sudah terjawab dengan API child