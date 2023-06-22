from .makeCatalog import makeCatalog
from .eventDownloader import eventDownloader
from .downLoadAllMarsquakeEvent import downloadAll

class Downloader():
    def __init__(self) -> None:
        pass

    def makeCatalog(self, path_Catalog):

        makeCatalog(path_Catalog)

    def eventDownloader(self, path_Catalog='./data/SeismicCatalog', event2find='S1237a', save_path=None):

        print('Running code for: Event ' + event2find)
        eventDownloader(path_Catalog, event2find, save_path)
        
        print('Event downloaded to ' + save_path)
    
    def downloadAll(self, path_Catalog='./data/SeismicCatalog', event_qualitys=['A', 'B', 'C', 'D'], event_classs=['LOW_FREQUENCY', 'BROADBAND', '2.4_HZ', 'HIGH_FREQUENCY', 'VERY_HIGH_FREQUENCY'], save_path='./data/SeismicCatalog'):
        print('Downloading all events')
        downloadAll(path_Catalog, event_qualitys, event_classs, save_path)
        print('All events downloaded')

        
        