from sv_utils import *

pdb = SQLAlchemy()

class DBTrackEntry(pdb.Model):
	id        = pdb.Column(pdb.String(25), primary_key = True)
	downloads = pdb.Column(pdb.Integer)
	size      = pdb.Column(pdb.Float)

