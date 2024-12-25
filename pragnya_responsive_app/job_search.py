import requests
import json 
RAPID_API_KEY_LINKDIN = "1112f12ab7msh6c9e4582c6ce79cp13772cjsn8a3336e278cb"
RAPID_API_KEY_JOBS= "1112f12ab7msh6c9e4582c6ce79cp13772cjsn8a3336e278cb"



def dump_jobs(job_description, filepath):
    """   simply dumps the job_dict into the source file job_opening.json    """
    try:
        # Load existing data if the file exists
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # Initialize data if the file doesn't exist
        data = {"jobs": []}

    # Add new job description to the data
    data["jobs"].append(job_description)

    # Write updated data back to the file
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=4)



def get_jobs_from_source():
    file_path = "job_opening.json"
    output_filepath = "jobs.json"
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"Source file '{file_path}' not found!")
        data = []

    for job in data:
        job_description = {
            "title": job["title"],
            "date_posted": job["date_posted"],
            "organization": job["organization"],
            "organization_url": job["organization_url"],
            "source": job["source"],
            "date_validthrough": job["date_validthrough"]
        }
        dump_jobs(job_description, output_filepath)


 

class GETLINKDINJOBS:
    url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"

    headers = {
        "x-rapidapi-key": "1112f12ab7msh6c9e4582c6ce79cp13772cjsn8a3336e278cb",
        "x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com"
    }

    # response = requests.get(url, headers=headers)

    # data = response.json()

    # print(data[0]['title'])



def get_jobs():
    """   this function fetches the jobs from source file and returns all the job 
            posting as a dict         """
    filepath='jobs.json'
    with open(filepath,"r") as json_file:
        data = json.load(json_file)
        jobs = data["jobs"]
    return jobs


