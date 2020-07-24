#Run this file to download any required packages and organize the NMA preprocessed HCP data

import os

def download_preprocessed_hcp(dataset_dict):
	'''

	Args:
		- dataset_dict (dict): A dictionary where keys are the name of the current preprocessed 
			dataset to download ('rest, 'task', or 'covariates') and values are the OSF weblink
			to the dataset
	'''

	for data, weblink in dataset_dict:
		fname = f'hcp_{data}.tgz'

		if not os.path.exists(fname): #grab the data file from the OSF weblink
		  !wget -qO $fname $weblink
		  !tar -xzf $fname -C $HCP_DIR --strip-components=1

def download_data(HCP_DIR="./hcp", *argv):
	'''

	Creates the directory structure and downloads data of NMA preprocessed HCP dataset
	HCP_DIR

	Args:
		- HCP_DIR (string): path to where data should be downloaded
		- *argv (string): can be any of ['rest', 'task, 'covariates']. If none are provided, downloads all possible sets
	'''

	datasets = {'rest': 'https://osf.io/bqp7m/download/',
		'task': 'https://osf.io/s4h8j/download/',
		'covariates': 'https://osf.io/x5p4g/download/'}
	
	if not os.path.isdir(HCP_DIR):
	  os.mkdir(HCP_DIR)

	if not len(argv):
		download_preprocessed_hcp(datasets)
	else: #download a subset of the data based on the argument strings proviced
		desired_datasets = {key: datasets[key] for key in argv}
		download_preprocessed_hcp(desired_datasets)

	if 'atlas' in argv: #download the 
		fname = f'{HCP_DIR}/atlas.npz'

		if not os.path.exists(fname):
		  !wget -qO $fname https://osf.io/j5kuc/download

if __name__ == "__main__":

	HCP_DIR = "./hcp"
	specific_sets = sys.argv[1:]
	print (specific_sets)
	# download_data(HCP_DIR)