from logentries import LogentriesHandler
import logging

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)

log.addHandler(LogentriesHandler('265ecca7-8cfe-44c5-8cb9-2be77cebb3bb'))