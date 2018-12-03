from django.contrib import admin
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Shop, Good, GoodImage, Note, Etalase, Department, Category
from django.forms import TextInput, Textarea, URLInput
from django.db import models

from django.conf import settings

##### custom order multiple field
from django.contrib.admin.views.main import ChangeList, ORDER_VAR
class SpecialOrderingChangeList(ChangeList):
    """ This is the class that will be overriden in order to change the way the admin_order_fields are read """
    def get_ordering(self, request, queryset):
        """ This is the function that will be overriden so the admin_order_fields can be used as lists of fields instead of just one field """
        params = self.params
        ordering = list(self.model_admin.get_ordering(request) or self._get_default_ordering())
        if ORDER_VAR in params:
            ordering = []
        order_params = params[ORDER_VAR].split('.')
        for p in order_params:
            try:
                none, pfx, idx = p.rpartition('-')
                field_name = self.list_display[int(idx)]
                order_field = self.get_ordering_field(field_name)
                if not order_field:
                    continue
                # Here's where all the magic is done: the new method can accept either a list of strings (fields) or a simple string (a single field)
                if isinstance(order_field, list):
                    for field in order_field:
                        ordering.append(pfx + field)
                else:
                    ordering.append(pfx + order_field)
            except (IndexError, ValueError):
                continue
        ordering.extend(queryset.query.order_by)
        pk_name = self.lookup_opts.pk.name
        if not (set(ordering) & set(['pk', '-pk', pk_name, '-' + pk_name])):
            ordering.append('pk')
        return ordering
#####

def custom_humanize(str_number, return_int = False):
    if 'rb' in str_number:
        multiplier = 1000
        str_number = str_number.replace('rb', '')
        str_number = str_number.replace(',', '.')
        float_number = float(str_number)
        str_number = int(float_number * multiplier)
    else:
        str_number = str_number.replace('.', '')

    if return_int:
        return int(str_number)
    return intcomma(int(str_number))


# Register your models here.
class GoodImageInline(admin.TabularInline):
    model = GoodImage
    extra = 3

    readonly_fields = ('link_barang',)
    can_delete = False

    def link_barang(self, obj):
        if obj.gambar_url:
            return format_html('<img src="{url}" height="200" width="200"/>', url = obj.gambar_url)
        else:
            return ''


class GoodInline(admin.TabularInline):
    model = Good
    extra = 3
    exclude = ('last_update',)
    # fields = (
    #     'barang_url',
    #     'barang_nama',
    #     'barang_gambar_utama',
    # 'barang_nama',
    # 'barang_nama',
    # )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs = {'size': '60'})},
    }

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset[10]


class GoodAdmin(admin.ModelAdmin):
    inlines = [GoodImageInline]
    ordering = ('barang_nama', )
    list_display = (
        'barang_nama',
        'rating',
        'harga_asli',
        'harga_jual',
        'link_barang',
        # 'barang_url'
    )
    list_filter = (
        'toko_induk',
        'barang_category',
        'barang_department',
    )
    fields = (
        # 'barang_url',
        # 'barang_url_full',

        'barang_nama',
        'barang_gambar_utama',
        'barang_informasi_produk',

        'barang_dilihat',
        'barang_dilihat_int',
        'barang_terjual',
        'barang_transaksi_sukses',
        'barang_transaksi_gagal',

        'rating',
        'barang_rating',
        'barang_rating_count',

        'barang_harga_asli',
        'barang_harga_jual',

        'barang_is_unggulan',
        'barang_kondisi',
        'barang_stok',
        'barang_status',
        'barang_minimal_order',
        'barang_is_preorder',

        'barang_jumlah_kurir',

        # diskon
        'barang_diskon_harga_asli',
        'barang_diskon_start',
        'barang_diskon_expired',
        'barang_diskon_percentage',

        # 'link_barang',
    )

    def get_fieldsets(self, request, obj = None):
        # return super().get_fieldsets(request, obj)
        return [
            ('Informasi Umum', {
                'fields': [
                    'barang_nama',
                    # 'barang_gambar_utama',
                    'gambar_barang',
                    'barang_informasi_produk',
                ]
            }),
            ['Harga', {
                'fields': [
                    'barang_harga_asli',
                    'barang_harga_jual',

                    'harga_asli',
                    'harga_jual'

                ]
            }],
            ['Status Barang', {
                'fields': [
                    'barang_dilihat',
                    'barang_dilihat_int',
                    'barang_terjual',
                    'barang_transaksi_sukses',
                    'barang_transaksi_gagal',

                    'rating',
                    'barang_rating',
                    'barang_rating_count',

                ]
            }],
            ['Informasi Lain', {
                'fields': [
                    'barang_category',
                    'barang_department',
                    'barang_kondisi',
                    'barang_stok',
                    'barang_status',
                    'barang_minimal_order',
                    'barang_is_preorder',
                    'barang_jumlah_kurir',
                ]
            }],
            ['Diskon', {
                'fields': [
                    'barang_diskon_harga_asli',
                    'barang_diskon_start',
                    'barang_diskon_expired',
                    'barang_diskon_percentage',
                ]
            }],
        ]

    def get_readonly_fields(self, request, obj = None):
        # return super().get_readonly_fields(request, obj)
        return (
            'gambar_barang',
            'barang_is_unggulan',
            'barang_dilihat',
            'barang_dilihat_int',
            'barang_terjual',
            'barang_transaksi_sukses',
            'barang_transaksi_gagal',

            'barang_category',
            'barang_department',

            'barang_kondisi',
            'barang_stok',
            'barang_status',
            'barang_minimal_order',
            'barang_is_preorder',
            'barang_jumlah_kurir',

            'barang_diskon_harga_asli',
            'barang_diskon_start',
            'barang_diskon_expired',
            'barang_diskon_percentage',

            'barang_rating',
            'barang_rating_count',
            'rating',

            'harga_asli',
            'harga_jual'
        )

    # ordering = ('barang_nama',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs = {'size': '60'})},
    }


    def link_barang(self, obj):
        return format_html("<a href='{url}' target='_blank'>link</a>", url = obj.barang_url)

    def gambar_barang(self, obj):
        single_image_string = '<a href="{}" target="_blank"><img src="{}" height="200" width="200"/></a>&nbsp;'
        final_html = ''

        gambar_barang = GoodImage.objects.filter(barang_induk = obj)
        for gambar in gambar_barang:
            final_html += single_image_string.format(gambar.gambar_url, gambar.gambar_url)
        return format_html(final_html)

    def harga_asli(self, obj):
        return 'Rp. ' + custom_humanize(str(obj.barang_harga_asli))

    harga_asli.admin_order_field = 'barang_harga_asli'

    def harga_jual(self, obj):
        return 'Rp. ' + custom_humanize(str(obj.barang_harga_jual))

    harga_jual.admin_order_field = 'barang_harga_jual'


    # def get_changelist(self, request, **kwargs):
    #     return SpecialOrderingChangeList

    def get_queryset(self, request):
        default_query = super().get_queryset(request)
        return default_query.order_by('barang_rating')

    def rating(self, obj):
        # todo: show star
        # star_icon = "<svg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'><title>icon / review / full</title><defs><path id='a' d='M0 0v17.358h17.986V0H0z'/></defs><g transform='translate(1 1)' fill='none' fill-rule='evenodd'><mask id='b' fill='#fff'><use xlink:href='#a'/></mask><path d='M17.8 7.155l-3.914 3.6a.733.733 0 0 0-.22.684l1.069 5.245a.561.561 0 0 1-.217.56.544.544 0 0 1-.596.032l-4.597-2.654a.719.719 0 0 0-.71 0l-4.587 2.664a.543.543 0 0 1-.597-.036.56.56 0 0 1-.216-.56c.478-2.35 1.029-4.99 1.07-5.22a.731.731 0 0 0-.19-.705L.18 7.165a.561.561 0 0 1-.155-.581.546.546 0 0 1 .443-.412l5.26-.565A.726.726 0 0 0 6.3 5.18L8.48.3a.566.566 0 0 1 .997 0l2.182 4.885a.714.714 0 0 0 .57.422l5.261.565a.546.546 0 0 1 .463.38.562.562 0 0 1-.154.603' fill='#FFC107' mask='url(#b)'/></g></svg>"
        # star_icon = '<span style="font-size:300%;color:yellow;">&starf;</span>'
        star_icon = ''
        return format_html("{icon_url} {star} ({count})",
                           icon_url = star_icon,
                           star = obj.barang_rating,
                           count = obj.barang_rating_count
                           )
    # rating.admin_order_field = ['barang_rating', 'barang_rating_count']

    def get_view_on_site_url(self, obj = None):
        # return super().get_view_on_site_url(obj)
        return obj.barang_url


class ShopAdmin(admin.ModelAdmin):
    # inlines = [GoodInline]
    list_filter = (
        'toko_is_gold',
        'toko_is_official',
        'toko_lokasi',
        'toko_kota',
        'toko_reputasi_level',
    )
    list_display = (
        'toko_nama',
        'reputasi_toko',
        # 'toko_reputasi_score',
        # 'toko_reputasi_level',

        'produk_terjual',
        'follower',
        # 'toko_terjual',
        # 'toko_follower',

        'toko_1_bulan_speed',
        # 'toko_1_bulan_order_count',
        'toko_3_bulan_speed',
        # 'toko_3_bulan_order_count',
        'toko_12_bulan_speed',
        # 'toko_12_bulan_order_count',

        'lokasi_toko',
        # 'toko_lokasi',
        # 'toko_kota',

        'jumlah_barang',
        # 'toko_jumlah_barang',

        'toko_is_official',
        'toko_is_gold',
    )

    # fields = (
    #     'foto_toko',
    # )
    # readonly_fields = (
    #     'foto_toko',
    # )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs = {'size': '20'})},
        # models.TextField: {'widget': Textarea(attrs = {'rows': 4, 'cols': 40})},
    }

    def save_model(self, request, obj, form, change):
        obj.toko_terjual_int = custom_humanize(obj.toko_terjual, return_int = True)
        obj.toko_follower_int = custom_humanize(obj.toko_follower, return_int = True)
        super().save_model(request, obj, form, change)

    def reputasi_toko(self, obj):
        return format_html("<img src='{url}'/> {level} &nbsp; {point} poin",
                           url = obj.toko_reputasi_badge_url,
                           point = intcomma(obj.toko_reputasi_score),
                           level = obj.get_toko_reputasi_level_display()
                           )

    reputasi_toko.admin_order_field = 'toko_reputasi_score'

    def jumlah_barang(self, obj):
        return str(Good.objects.filter(toko_induk = obj).count()) + ' / ' + str(obj.toko_jumlah_barang)

    def produk_terjual(self, obj):
        return custom_humanize(obj.toko_terjual)

    produk_terjual.admin_order_field = 'toko_terjual_int'

    def follower(self, obj):
        return custom_humanize(obj.toko_follower)

    follower.admin_order_field = 'toko_follower_int'

    # def jumlah_barang(self, obj):
    #     return custom_humanize(obj.toko_jumlah_barang)

    def lokasi_toko(self, obj):
        if obj.toko_lokasi == obj.toko_kota:
            return obj.toko_lokasi
        else:
            return obj.toko_lokasi + ' - ' + obj.toko_kota
        'jumlah_barang',

    def foto_toko(self, obj):
        # return format_html("<img href='{url}' target='_blank'>{url}</a>", url = obj.link_gedung)
        return format_html("<img src='{url}'/>", url = obj.toko_gambar)

    def get_view_on_site_url(self, obj = None):
        # return super().get_view_on_site_url(obj)
        return obj.toko_url


admin.site.register(Shop, ShopAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(GoodImage)
admin.site.register(Note)
admin.site.register(Etalase)
admin.site.register(Department)
admin.site.register(Category)
