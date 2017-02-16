import requests
from operator import itemgetter
from requests.exceptions import ConnectionError


def sort_dataset_by_key(container, key):
	container.sort(key=itemgetter(key), reverse=True)
	return container


def slice_dataset(container, count):
	return container[:count]


def get_total_repos(org):
	try:
		response = requests.get("https://api.github.com/orgs/{}".format(org))
	except ConnectionError as e:
		raise e
	return response.json()['public_repos']

def find_top_repos(org, n, total_repos):
	paginate_by = 0
	if total_repos % 30 == 0:
		paginate_by = total_repos/30
	else:
		paginate_by = total_repos/30 + 1
	org_repo = []
	for i in range(paginate_by+1):
		try:
			response = requests.get("https://api.github.com/orgs/{}/repos?page={}".format(org, i+1))
		except ConnectionError as e:
			raise e
		
		for data in response.json():
			repo_dict = dict()
		 	repo_dict['id'] = data['id']
		 	repo_dict['name'] = data['name']
		 	repo_dict['owner'] = data['owner']['login']
		 	repo_dict['contributors_url'] = data['contributors_url']
		 	repo_dict['forks_count'] =  data['forks_count']

		 	org_repo.append(repo_dict)

	org_repo = slice_dataset(sort_dataset_by_key(org_repo, 'forks_count'), n)
	return org_repo


def top_contributors(org_repo, m):
	result_dict = dict()
	for i, data in enumerate(org_repo):
		contributor_list = []
		response = requests.get("https://api.github.com/repos/{}/{}/stats/contributors".format(data['owner'], data['name']))
		for contributor in response.json():
			contributor_dict = dict()
			contributor_dict['login']  = contributor['author']['login']
		 	contributor_dict['commits'] = contributor['total']
		 	contributor_list.append(contributor_dict)
		contributor_list = slice_dataset(sort_dataset_by_key(contributor_list, 'commits'), m)
		result_dict[str(data['id'])] = contributor_list

	return result_dict


if __name__ == "__main__":
	org = raw_input("Enter organization name to search repositories: ")
	n = input("How many top repos to look for? ")
	m = input("How many top contributors to look for? ")
	total_repos = get_total_repos(org)
	top_repos = find_top_repos(org, n, total_repos)
	top_contribs = top_contributors(top_repos, m)

	print "Top {} repos for organization name: {}".format(n, org.title())
	for k, data in enumerate(top_repos):
		print "\n{}. {}".format(k+1, data['name'])
		print "\nTop contributors for {}".format(data['name'])
		for i, contributor in enumerate(top_contribs[str(data['id'])]):
			print "{}. {}, commits: {}".format(i+1, contributor['login'], contributor['commits'])

