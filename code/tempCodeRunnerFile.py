 with open('score_file.json','r+') as score_file:
                file_data = json.load(score_file)
                file_data["scorefile"].append(score_data)
                score_file.seek(0)
                json.dump(file_data,score_file,indent=4)