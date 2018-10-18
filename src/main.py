import requests
import json
import configparser
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from time import sleep
from ratelimit import limits, sleep_and_retry
        
class mtg_image_importer:

    def __init__(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        self.output_dest = config.get('file_config', 'output_dest') + '/mtg_images'
        self._create_folder(self.output_dest)
        self.is_threaded = config.getboolean('thread_config', 'threaded')
        self.threads = config.getint('thread_config', 'max_threads')
        with open(config.get('file_config', 'json_source')) as card_file:
            self.card_list = json.load(card_file)        

    def _create_folder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory ' + directory)

    def _write_image(self, card_name, card_set, collector_num, response):
        if not response.ok:
            with open('{0}/errors.txt'.format(self.output_dest), 'a') as error_file:
                error_file.write('{0}_{1}_{2}\n'.format(card_name, card_set, collector_num))
                return
        self._create_folder('{0}/{1}_{2}_{3}'.format(self.output_dest, card_name, card_set, collector_num))
        with open('{0}/{1}_{2}_{3}/original.png'.format(self.output_dest, card_name, card_set, collector_num), 'wb+') as new_image:
            print('Writing {0}_{1}_{2}'.format(card_name, card_set, collector_num))
            for block in response.iter_content(1024):
                if not block:
                    break
                new_image.write(block)

    @sleep_and_retry
    @limits(calls = 8, period = 1.0)
    def get_image(self, image_url):
        response = requests.get(image_url, stream=True)
        while not response.ok:
            print(response)
            print("Trying Again...")
            sleep(0.25)
            response = requests.get(image_url, stream=True)
        return  response

    def _card_done(self, card_name, card):
        return os.path.exists('{0}/{1}_{2}_{3}'.format(self.output_dest, card_name, card['set'], card['collector_number']))

    def _card_thread(self, card):
        if card['digital'] == True:
            return 
        if card['layout'] == 'transform' or card['layout'] == 'double_faced_token':
            for card_face in card['card_faces']:
                card_name = card_face['name']
                if self._card_done(card_name, card):
                    continue
                response = self.get_image(card_face['image_uris']['png'])
                self._write_image(card_name, card['set'], card['collector_number'], response)
        else:
            trantab = str.maketrans('/', '-')
            card_name = card['name'].translate(trantab)
            if self._card_done(card_name, card):
                return
            try:
                image_uri = self.get_image(card['image_uris']['png'])
                response = self.get_image(image_uri)
                self._write_image(card_name, card['set'], card['collector_number'], response)
                
            except KeyError:
                print(card_name, ' has no image uri associated with it.')

    def _import_cards_threaded(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self._card_thread, card) for card in self.card_list]

        for future in as_completed(futures):
            print(future.result())

    def _import_cards_unthreaded(self):
        for card in self.card_list:
            self._card_thread(card)

    def import_cards(self):
        if self.is_threaded:
            self._import_cards_threaded()
        else:
            self._import_cards_unthreaded()

if __name__ == '__main__':
    if os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/config.ini'):
        importer = mtg_image_importer(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')
    else:
        importer = mtg_image_importer(os.path.dirname(os.path.realpath(__file__)) + '/example.ini')
    importer.import_cards()
