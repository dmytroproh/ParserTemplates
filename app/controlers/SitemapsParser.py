import random
from configparser import SafeConfigParser
from datetime import datetime
from threading import Thread
import cfscrape
from ..models import *
from ..serviceManager import *
from bs4 import BeautifulSoup


def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out


class SitemapsParser(QThread):
    logs = pyqtSignal('QString')

    def __init__(self, parent, cfg_file):
        print("__init__(self,parent,cfg_file):")
        super(SitemapsParser, self).__init__(parent)
        QThread.__init__(self, parent)
        self.setTerminationEnabled(True)
        self.config = SafeConfigParser()
        self.config.read(cfg_file)
        self.config = SafeConfigParser()
        self.config.read(cfg_file)
        self.urllistxt = '''
                https://www.ficegallery.com/sitemap_products_1.xml
                https://www.pampamlondon.com/sitemap_products_1.xml
                https://www.theclosetinc.com/sitemap_products_1.xml
                https://www.thedarksideinitiative.com/sitemap_products_1.xml
                http://commonwealth-ftgg.com/sitemap_products_1.xml
                http://dope-factory.com/sitemap.xml
                http://en.sneakerium.com/sitemap.en.xml
                http://graduatestore.fr/sitemap-1.xml
                http://kicks-hawaii.myshopify.com/sitemap_products_1.xml
                http://kosmosstore.com/1_en_0_sitemap.xml
                http://nrml.ca/sitemap_products_1.xml
                http://packershoes.com/sitemap_products_1.xml
                http://rsvpgallery.com/sitemap_products_1.xml
                http://runcolors.pl/sitemap.xml
                http://shop.doverstreetmarket.com/sitemap.xml
                http://shop.epitomeatl.com/sitemap.xml
                http://shop.nordstrom.com/sitemap_productset_0.xml
                http://shop.nordstrom.com/sitemap_productset_1.xml
                http://streetsupply.pl/1_en_0_sitemap.xml
                http://tres-bien.com/sitemap.xml
                http://undefeated.com/sitemap.xml
                http://unheardof.bigcartel.com/sitemap.xml
                http://us.octobersveryown.com/sitemap_products_1.xml
                http://us.puma.com/sitemap_0.xml
                http://www.adidas.co.uk/sitemap1_en_GB.xml
                http://www.adidas.co.uk/sitemap2_en_GB.xml
                http://www.adidas.co.uk/sitemap3_en_GB.xml
                http://www.adidas.com/on/demandware.static/-/Sites-adidas-US-Library/en_US/v/sitemap/product/adidas-US-en-us-product.xml
                http://www.anatomystore.co.za/productdetail_1006_0.xml.gz
                http://www.anrosa-store.com/sitemap.xml
                http://www.apbstore.com/sitemap_products_1.xml
                http://www.aphrodite1994.com/sitemaps/sitemap.xml
                http://www.avenuestore.be/en/sitemap.xml
                http://www.back-door.it/product-sitemap.xml
                http://www.champssports.com/sitemap.xml.gz
                http://www.consortium.co.uk/sitemap.xml
                http://www.cornerstreet.fr/cornerstreetmap.xml
                http://www.doubleclutch.it/sitemap.xml
                http://www.dtlr.com/sitemap.xml
                http://www.eastbay.com/sitemap.xml.gz
                http://www.endclothing.com/media/eu_sitemap.xml
                http://www.endclothing.com/media/gb_sitemap.xml
                http://www.endclothing.com/media/us_sitemap.xml
                http://www.featuresneakerboutique.com/sitemap_products_1.xml
                http://www.finishline.com/detail0.xml
                http://www.footaction.com/sitemap.xml.gz
                http://www.footasylum.com/ProductsSiteMap1.xml
                http://www.footasylum.com/ProductsSiteMap2.xml
                http://www.footasylum.com/ProductsSiteMap3.xml
                http://www.footlocker.com/sitemap.xml.gz
                http://www.gloryholeshop.com/feeds/sitemap.xml
                http://www.holypopstore.com/sitemap.xml
                http://www.hypnotik.fr/sitemap.xml
                http://www.inflammable.com/sitemap.xml
                http://www.jimmyjazz.com/sitemap/sitemap.xml
                http://www.lebuzzsneakershop.com/sitemap.xml
                http://www.mate-store.com/product-sitemap.xml
                http://www.nike.com/sitemap-www-en-us.xml
                http://www.notre-shop.com/sitemap_products_1.xml
                http://www.oipolloi.com/sitemap_products_1.xml
                http://www.oneblockdown.it/sitemap.xml
                http://www.oqium.nl/sitemap.xml
                http://www.pacsun.com/sitemap_0.xml
                http://www.petrolioshop.com/1_it_0_sitemap.xml
                http://www.piils.fr/1_fr_0_sitemap.xml
                http://www.reebok.com/on/demandware.static/-/Sites-Reebok-US-Library/en_US/v/sitemap/product/Reebok-US-en-us-product.xml
                http://www.roadrunnersports.com/sitemap.xml
                http://www.schuhdealer.de/sitemap.xml
                http://www.selfridges.com/sitemap_US_en_1.xml
                http://www.shoepalace.com/sitemaps/sitemap_001.xml
                http://www.shop.renarts.com/sitemap_products_1.xml
                http://www.sivasdescalzo.com/sitemaps/en/sitemap-1.xml
                http://www.sivasdescalzo.com/sitemaps/en/sitemap-2.xml
                http://www.sneak-a-venue.com/sitemap.xml
                http://www.sneak-a-venue.cz/sitemap.xml
                http://www.sneakerbaas.com/feeds/nl/sitemap.xml
                http://www.snipes.com/sitemap.xml
                http://www.solekitchen.de/sitemap.xml
                http://www.superstylin.it/product-sitemap.xml
                http://www.urbanindustry.co.uk/sitemap_products_1.xml
                http://www.urbanjunglestore.com/sitemap.xml
                http://www.wishatl.com/sitemap_products_1.xml
                http://www.ycmc.com/sitemap.xml
                https://atmosny.com/sitemap_products_1.xml
                https://attic2zoo.com/sitemap_products_1.xml
                https://bapeonline.com/sitemap_products_1.xml
                https://beatniconline.com/sitemap_products_1.xml
                https://brandshop.ru/sitemap.xml
                https://brooklynwaynyc.com/sitemap_products_1.xml
                https://burnrubbersneakers.com/sitemap_products_1.xml
                https://ca.octobersveryown.com/sitemap_products_1.xml
                https://centre214.com/sitemap_products_1.xml
                https://cncpts.com/sitemap_products_1.xml
                https://concrete.nl/sitemap_products_1.xml
                https://en.aw-lab.com/shop/en/sitemap.xml
                https://en.beyondstore.fi/sitemap.xml
                https://fearofgod.com/sitemap_products_1.xml
                https://footdistrict.com/sitemaps/sitemap_en/sitemap.xml
                https://hotoveli.com/sitemap_products_1.xml
                https://justdon.com/sitemap_products_1.xml
                https://kith.com/sitemap_products_1.xml
                https://minishopmadrid.myshopify.com/sitemap_products_1.xml
                https://nomadshop.net/sitemap_products_1.xml
                https://nrml.ca/sitemap_products_1.xml
                https://offthehook.ca/sitemap_products_1.xml
                https://properlbc.com/sitemap_products_1.xml
                https://rezetstore.dk/sitemap.xml
                https://rise45.com/sitemap_products_1.xml
                https://rockcitykicks.com/sitemap_products_1.xml
                https://samtabak.com/sitemap_products_1.xml
                https://sapatostore.com/product-sitemap.xml
                https://shoegallerymiami.com/sitemap_products_1.xml
                https://shop.bdgastore.com/sitemap_products_1.xml
                https://shop.bdgastore.com/sitemap_products_2.xml
                https://shop.exclucitylife.com/sitemap_products_1.xml
                https://shop.extrabutterny.com/sitemap_products_1.xml
                https://shop.havenshop.ca/sitemap_products_1.xml
                https://shop.reigningchamp.com/sitemap_products_1.xml
                https://shopdripla.com/sitemap_products_1.xml
                https://shopnicekicks.com/sitemap_products_1.xml
                https://shopnicekicks.com/sitemap_products_2.xml
                https://sneakerjunkiesusa.com/sitemap_products_1.xml
                https://sneakerpolitics.com/sitemap_products_1.xml
                https://thesportsedit.com/sitemap_products_1.xml
                https://us.bape.com/sitemap_products_1.xml
                https://varunco.com/sitemap_products_1.xml
                https://www.12amrun.com/sitemap_products_1.xml
                https://www.290sqm.com/sitemap.xml
                https://www.a-ma-maniere.com/sitemap_products_1.xml
                https://www.addictmiami.com/sitemap_products_1.xml
                https://www.afew-store.com/sitemap.xml
                https://www.allikestore.com/sitemap_en.xml
                https://www.ateaze.com/sitemap_products_1.xml
                https://www.bbbranded.com/sitemap_products_1.xml
                https://www.blendsus.com/sitemap_products_1.xml
                https://www.blkmkt.us/sitemap_products_1.xml
                https://www.bowsandarrowsberkeley.com/sitemap_products_1.xml
                https://www.capsuletoronto.com/sitemap_products_1.xml
                https://www.cityblueshop.com/sitemap_products_1.xml
                https://www.courtsidesneakers.com/sitemap_products_1.xml
                https://www.craemerco.de/sitemap.xml
                https://www.deadstock.ca/sitemap_products_1.xml
                https://www.flannel.com.au/sitemap_products_1.xml
                https://www.forbucks.es/product-sitemap.xml
                https://www.graffitishop.net/sitemap_https_eng_1.xml
                https://www.highsandlows.net.au/sitemap_products_1.xml
                https://www.huntinglodge.no/sitemap_products_1.xml
                https://www.hypedc.com/sitemap-products.xml
                https://www.iconsbybizanc.com/sitemap_products_1.xml
                https://www.jdsports.co.uk/sitemaps/sitemap001.xml
                https://www.jdsports.fr/sitemaps/sitemap001.xml
                https://www.k101store.com/sitemap_products_1.xml
                https://www.kickz.com/de/sitemap-products.xml.gz
                https://www.kickz.com/en/sitemap-products.xml.gz
                https://www.kyliecosmetics.com/sitemap_products_1.xml
                https://www.lapstoneandhammer.com/sitemap_products_1.xml
                https://www.minishopmadrid.com/sitemap_products_1.xml
                https://www.nighshop.com/media/sitemap/nigh_en/sitemap.xml
                https://www.nojokicks.com/sitemap_products_1.xml
                https://www.oneness287.com/sitemap_products_1.xml
                https://www.overkillshop.com/sitemap.xml
                https://www.patta.nl/sitemap.xml
                https://www.ruvilla.com/media/sitemaps/sitemap.xml
                https://www.saintalfred.com/sitemap_products_1.xml
                https://www.saveoursole.de/sitemap.xml
                https://www.shelflife.co.za/sitemap.xml
                https://www.shiekh.com/media/sitemaps/shiekh_sitemap.xml
                https://www.size.co.uk/sitemaps/sitemap001.xml
                https://www.sneakerloungeusa.com/sitemap_products_1.xml
                https://www.socialstatuspgh.com/sitemap_products_1.xml
                https://www.solebox.com/sitemap1.xml.gz
                https://www.soleheaven.com/sitemap_products_1.xml
                https://www.solestop.com/sitemap_products_1.xml
                https://www.solestory.se/product-sitemap1.xml
                https://www.ssense.com/sitemap_products_1.xml
                https://www.staging.adidas.fr/static/on/demandware.static/-/Sites-adidas-FR-Library/fr_FR/v/sitemap/product/adidas-FR-fr-fr-product.xml
                https://www.stickabush.com/_sitemaps/en/sitemap.xml
                https://www.subtypestore.com/product-sitemap.xml
                https://www.thefactoryokc.com/sitemap_products_1.xml
                https://www.thegoodwillout.com/media/sitemap/en/sitemap.xml
                https://www.thegoodwillout.de/media/sitemap/en/sitemap.xml
                https://www.thehipstore.co.uk/sitemaps/sitemap001.xml
                https://www.trophyroomstore.com/sitemap_products_1.xml
                https://www.uebervart-shop.de/product-sitemap.xml
                https://www.westnyc.com/sitemap_products_1.xml
                https://www.wrongweather.net/sitemap.xml
                https://www.xhibition.co/sitemap_products_1.xml
                https://yeezysupply.com/sitemap_products_1.xml
                '''
        self.url_list = list(set(self.urllistxt.split()))
        print(self.url_list)
        #self.url_list = open('SITEMAPS/SITEMAPS.txt').readlines()
        self.dump = []
        self.proxies = []
        self.proxies.append(None)

    def load_proxies(self):
        try:
            proxies_list = open('mod/proxies.txt', 'r').readlines()
            for p in proxies_list:
                # noinspection PyTypeChecker
                self.proxies.append(
                    {
                        'http': 'http://' + p,
                        'https': 'https://' + p
                    }
                )
            self.logs.emit("[LOG] " + str(len(proxies_list)) + " Proxies loaded")
        except Exception:
            print_exception_info("ERROR OCCURRED WHEN LOADING PROXIES", Exception)


    def update_db(self, urllist):
        print("update_db(self)")
        for url in urllist:
            self.parse_sitemap(url)

    def _openurl(self, url):
        self.logs.emit("[LOG] Requesting URL : " + url)
        try:
            p_pick = random.choice(self.proxies)
            if p_pick is not None:
                self.logs.emit("[LOG] using proxy " + p_pick['http'])
            scraper = cfscrape.create_scraper()
            response = scraper.get(url, proxies=p_pick)
            html = ''
            for chunk in response.iter_content(chunk_size=512 * 1024):
                html = html + str(chunk)
            return html.encode('utf-8')
        except Exception:
            print_exception_info("ERROR OCCURRED WHEN requesting URL", Exception)

    def parse_sitemap(self, url):
        try:
            print("Parsing sitemap " + str(url) + " STARTED AT " + str(datetime.now()))
            try:
                bs = BeautifulSoup(self._openurl(url), features="lxml")
            except KeyError:
                print("THIS SITEMAP IS maybe EMPTY or an unexpected Error occurred")
                return None
            # extract what we need from the url
            dataset = []
            for row in bs.findAll('url'):
                if row.find('lastmod') is not None:
                    dataset.append({'loc': row.find('loc').text, 'lastmod': row.find('lastmod').text})
                else:
                    dataset.append({'loc': row.find('loc').text, 'lastmod': '2000-00-00'})
            dataset = self.remove_duplicate(dataset)
            print("Parsing sitemap " + str(url) + " ENDED AT " + str(datetime.now()))
            self.sgdump(dataset)
        except Exception:
            print_exception_info("ERROR OCCURRED WHEN PARSING ", Exception)

    @staticmethod
    def remove_duplicate(dataset):
        print("remove_duplicate(dataset)")
        return [dict(tupleized) for tupleized in set(tuple(item.items()) for item in dataset)]

    def sgdump(self, data):
        print("SGdump" + str(len(data)))
        sto = DataStore()
        sto.set_op('add', data)
        t = Thread(target=sto.run)
        t.start()
        t.join()
        self.logs.emit("[LOG] Data stored")

    def run(self):
        self.logs.emit("scraping and updating database in background ")
        self.logs.emit(" URL SET CONTAINS " + str(len(self.url_list)) + " URLs")
        self.dump = []
        print("run(self):")
        while True:
            try:
                time.sleep(1)
                t0 = time.time()
                print("Parsing sitemap ALL SITEMAPS STARTED AT " + str(datetime.now()))
                threads = []
                four_lists = chunk_it(self.url_list, 4)
                for i in four_lists:
                    t = Thread(target=self.update_db, args=(i,))
                    t.start()
                    threads.append(t)
                self.logs.emit("[LOG] 4 threads started")
                for j in threads:
                    j.join()
                t1 = time.time()
                self.logs.emit("[LOG] Parsing sitemap ALL SITEMAPS ended in seconds : " + str(t1 - t0))
            except Exception :
                print_exception_info("ERROR OCCURRED WHEN PARSING ", Exception)

