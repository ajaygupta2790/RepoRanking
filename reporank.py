import requests
from operator import itemgetter
from requests.exceptions import ConnectionError


def sort_dataset_by_key(container, key):
	container.sort(key=itemgetter(key), reverse=True)
	return container


def slice_dataset(container, count):
	return container[:count]


def find_top_repos(org, n):
	try:
		response = requests.get("https://api.github.com/orgs/{}/repos".format(org))
	except ConnectionError as e:
		raise e
	org_repo = []
	for data in response.json():
		repo_dict = dict()
	 	repo_dict['id'] = data['id']
	 	repo_dict['name'] = data['name']
	 	repo_dict['contributors_url'] = data['contributors_url']
	 	repo_dict['forks_count'] =  data['forks_count']

	 	org_repo.append(repo_dict)

	org_repo = slice_dataset(sort_dataset_by_key(org_repo, 'forks_count'), n)
	return org_repo


def top_contributors(org_repo, m):
	result_dict = dict()
	for i, data in enumerate(org_repo):
		contributor_list = []
		response = requests.get(data['contributors_url'])
		for contributor in response.json():
			contributor_dict = dict()
			contributor_dict['login']  = contributor['login']
		 	contributor_dict['contributions'] = contributor['contributions']
		 	contributor_list.append(contributor_dict)
		contributor_list = slice_dataset(sort_dataset_by_key(contributor_list, 'contributions'), m)
		result_dict[str(data['id'])] = contributor_list

	return result_dict


if __name__ == "__main__":
	org = raw_input("Enter organization name to search repositories: ")
	n = input("How many top repos to look for? ")
	m = input("How many top contributors to look for? ")
	top_repos = find_top_repos(org, n)
	print top_repos

	top_contribs = top_contributors(top_repos, m)
	print top_contributors
	print "Top {} repos for organization name: {}".format(n, org.title())
	for k, data in enumerate(top_repos):
		print "\n{}. {}".format(k+1, data['name'])
		print "\nTop contributors for {}".format(data['name'])
		for i, contributor in enumerate(top_contribs[str(data['id'])]):
			print "{}. {}, commits: {}".format(i+1, contributor['login'], contributor['contributions'])

