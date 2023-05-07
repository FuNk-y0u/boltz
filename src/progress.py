'''
Function To Update Progress Of Download
'''

import json


def update_state(token, tprogress, csong, iscomplete):
    '''
    token: token for each download process
    tprocess: Total Process Of Download
    csong: current song which is downloading
    iscomplete: if the whole progress is completed or not
    '''

    #Writing Progress Into Json FIle
    with open("user_progress.json","r") as json_file:
        file_data = json.load(json_file)
        json_file.close()
    with open("user_progress.json","w") as json_file:
        detail = {"total_progress": tprogress, "current_song": csong, "is_complete": iscomplete}
        file_data.update({token:detail})
        json.dump(file_data,json_file)
        json_file.close()