import logging

from granoclient.loader import Loader
from unicodecsv import DictReader

from kompromatron.core import grano, NotFound
from kompromatron.loaders.util import read_file

SOURCE_URL = 'http://www.bundestag.de/service/glossar/R/rechenschaftsberichte.html'
log = logging.getLogger(__name__)


def load_spende(loader, spende):
    log.info('Parteispende: %s an %s', spende['spender_name'], spende['partei_acronym'])
    
    party = loader.make_entity(['party'])
    party.set('name', spende.pop('partei_name'))
    party.set('acronym', spende.pop('partei_acronym'))
    party.save()

    typ = 'person' if spende.pop('spender_typ') == 'nat' else 'organisation'
    spender = loader.make_entity(['address', typ])
    spender.set('name', spende.pop('spender_name'))
    spender.set('street', spende.pop('spender_strasse'))
    spender.set('postcode', spende.pop('spender_plz'))
    spender.set('city', spende.pop('spender_stadt'))
    spender.save()

    s = loader.make_relation('party_donation', spender, party)
    s.unique('internal_id')
    s.set('internal_id', spende.pop('id'))
    s.set('year', spende.pop('jahr'))
    s.set('amount', spende.pop('betrag_eur'))
    s.save()


def load_spenden():
    loader = Loader(grano, source_url=SOURCE_URL)

    fh = read_file('data/spenden.csv')
    reader = DictReader(fh)
    for row in reader:
        load_spende(loader, row)
