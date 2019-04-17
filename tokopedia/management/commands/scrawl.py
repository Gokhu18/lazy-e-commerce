from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Clone Shop using requests'

    def __init__(self, stdout = None, stderr = None, no_color = False):
        self.options = None
        super().__init__(stdout, stderr, no_color)

    def add_arguments(self, parser):
        parser.add_argument('--link',
                            help = 'shop link')

    def handle(self, *args, **options):
        # todo:
        # masuk ke tokopedia.com
        # scrap toko2 yang bagus2 -> masukkan
        # todo: try to check shop's performance. if good -> clone, else, pass
        # penting: mungkin malah ada API untuk ambil flash sale / shop terbaik, dsb

        pass


    # todo: otomatis tambahkan flash sale ke shopee