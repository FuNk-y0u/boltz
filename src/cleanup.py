import time
from src.boltz_util import *
from src.config import *
import os

def clean_up(item,song,db,app):
    with app.app_context():
        try:
            while(True):
                items = item.query.all()
                for i in items:
                    if(i.isDisabled == False):
                        if (round(time.time()) - i.timeOfGen) >= DELETE_TIME:
                            try:
                                os.remove(f"{ZIP_LOCATION}{i.boltId}.zip")
                                logHeader(f"Deleting {i.boltId}.zip")
                                i.isDisabled = True
                                db.session.commit()
                            except:
                                pass
                time.sleep(CHECK_TIME)
        except KeyboardInterrupt:
            print('interrupted!')
