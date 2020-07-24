#Run this file to download any required packages and organize the NMA preprocessed HCP data
#
#Example use:
#	- Download resting state data: python data_downloader.py rest
#	- Download all data (not recommended): python data_downloader.py
#
#Written by TLB 2020

import os, sys, requests, tarfile
from tqdm import tqdm #for monitoring download progress

def download_preprocessed_hcp(dataset_dict, download_dir):
	'''

	Args:
		- dataset_dict (dict): a dictionary where keys are the name of the current preprocessed 
			dataset to download ('rest, 'task', or 'covariates') and values are a list containing
			name to write file and OSF weblink to the dataset
		- download_dir (string): where to write downloaded files
	'''

	for dataset, info in dataset_dict.items():
		fname, weblink = info
		download_path = f'{download_dir}/{fname}'

		if not os.path.exists(download_path): #grab the data file from the OSF weblink

			response = requests.get(f'{weblink}', stream=True)

			total_size = int(response.headers.get('content-length', 0))
			block_size = 1024 #1 Kibibyte

			if response.status_code == 200:
				print (f'Downloading {fname} to {download_path}')
				with open(download_path, 'wb') as f:
					with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
						for data in response.iter_content(block_size):
							pbar.update(len(data))
							f.write(data)

				print (f'Extracting files for {fname}')

				if 'tgz' in fname: #untar if tar file
					tar = tarfile.open(download_path, "r:gz")
					tar.extractall(path=download_dir)
					tar.close()

def download_data(HCP_DIR="./hcp", *argv):
	'''

	Creates the directory structure and downloads data of NMA preprocessed HCP dataset
	HCP_DIR

	Args:
		- HCP_DIR (string): path to where data should be downloaded
		- *argv (string): can be any of ['rest', 'task, 'covariates']. If none are provided, downloads all possible sets
	'''

	datasets = {'rest': ['hcp_rest.tgz', 'https://osf.io/bqp7m/download/'],
		'task': ['hcp_task.tgz', 'https://osf.io/s4h8j/download/'],
		'covariates': ['hcp_covariates.tgz', 'https://osf.io/x5p4g/download/'],
		'atlas': ['atlas.npz', 'https://osf.io/j5kuc/download']}
	
	if not os.path.isdir(HCP_DIR):
	  os.mkdir(HCP_DIR)

	if not len(argv):
		download_preprocessed_hcp(datasets, HCP_DIR)
	else: #download a subset of the data based on the argument strings proviced
		desired_datasets = {key: datasets[key] for key in argv}
		download_preprocessed_hcp(desired_datasets, HCP_DIR)

if __name__ == "__main__":

	HCP_DIR = "./hcp"
	specific_sets = sys.argv[1:]
	download_data(HCP_DIR, *specific_sets)