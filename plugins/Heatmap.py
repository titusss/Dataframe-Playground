def main(parameters):
    upload_url = "https://hp-heatmap-frontend-44nub6ij6q-ez.a.run.app/"
    response = requests.post(upload_url, files={'file': output})
    return upload_url+parameters["db_entry_id"]