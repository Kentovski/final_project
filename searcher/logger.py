from logentries import LogentriesHandler
import logging

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)

log.addHandler(LogentriesHandler('265ecca7-8cfe-44c5-8cb9-2be77cebb3bb'))


alert_log = logging.getLogger('logentries')
alert_log.setLevel(logging.INFO)

alert_log.addHandler(LogentriesHandler('2b9331ee-8c47-4525-8efd-5fad1b29e747'))
