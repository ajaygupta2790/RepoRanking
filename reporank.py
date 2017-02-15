import requests
import json
from operator import itemgetter

response = requests.get("https://api.github.com/orgs/google/repos")
repo = []
n = 5
m = 4
for data in response.json():
	repo_dict = dict()
 	repo_dict['id'] = data['id']
 	repo_dict['contributors_url'] = data['contributors_url']
 	repo_dict['forks_count'] =  data['forks_count']

 	repo.append(repo_dict)

repo.sort(key=itemgetter('forks_count'), reverse=True)
repo = repo[:n]
contributor_list = []
for data in repo:
	response = requests.get(data['contributors_url'])

	for contributor in response.json():
		print contributor
		contributor_dict = dict()
		contributor_dict['login']  = contributor['login']
	 	contributor_dict['contributions'] = contributor['contributions']
	 	contributor_list.append(contributor_dict)