import config.config as cfg
from aip import AipOcr

client = AipOcr(**cfg.config)

def getAipOcr():
	return client
