import os, sys, glob
import numpy as np


class HCP_NMA:

	def __init__(self, N_SUBJECTS = 339):
		'''
		Initialize a class that contains data specs for NMA HCP data

		Args:
			- N_SUBJECTS (int): Default is 339 (subset of HCP data), this can be 
			changed to a smaller number for testing analyses
			
		'''
		# The data shared for NMA projects is a subset of the full HCP dataset
		self.N_SUBJECTS = N_SUBJECTS

		# The data have already been aggregated into ROIs from the Glasser parcellation
		self.N_PARCELS = 360

		# The acquisition parameters for all tasks were identical
		self.TR = 0.72  # Time resolution, in sec

		# The parcels are matched across hemispheres with the same order
		self.HEMIS = ["Right", "Left"]

		# Each experiment was repeated multiple times in each subject
		self.N_RUNS_REST = 4
		self.N_RUNS_TASK = 2

		# Time series data are organized by experiment, with each experiment
		# having an LR and RL (phase-encode direction) acquistion
		self.BOLD_NAMES = [
		  "rfMRI_REST1_LR", "rfMRI_REST1_RL",
		  "rfMRI_REST2_LR", "rfMRI_REST2_RL",
		  "tfMRI_MOTOR_RL", "tfMRI_MOTOR_LR",
		  "tfMRI_WM_RL", "tfMRI_WM_LR",
		  "tfMRI_EMOTION_RL", "tfMRI_EMOTION_LR",
		  "tfMRI_GAMBLING_RL", "tfMRI_GAMBLING_LR",
		  "tfMRI_LANGUAGE_RL", "tfMRI_LANGUAGE_LR",
		  "tfMRI_RELATIONAL_RL", "tfMRI_RELATIONAL_LR",
		  "tfMRI_SOCIAL_RL", "tfMRI_SOCIAL_LR"
		]

		# You may want to limit the subjects used during code development.
		# This will use all subjects:
		self.subjects = range(N_SUBJECTS)

def get_image_ids(name):
  """Get the 1-based image indices for runs in a given experiment.

    Args:
      name (str) : Name of experiment ("rest" or name of task) to load
    Returns:
      run_ids (list of int) : Numeric ID for experiment image files

  """
  run_ids = [
    i for i, code in enumerate(BOLD_NAMES, 1) if name.upper() in code
  ]
  if not run_ids:
    raise ValueError(f"Found no data for '{name}''")
  return run_ids

def load_timeseries(subject, name, runs=None, concat=True, remove_mean=True):
  """Load timeseries data for a single subject.
  
  Args:
    subject (int): 0-based subject ID to load
    name (str) : Name of experiment ("rest" or name of task) to load
    run (None or int or list of ints): 0-based run(s) of the task to load,
      or None to load all runs.
    concat (bool) : If True, concatenate multiple runs in time
    remove_mean (bool) : If True, subtract the parcel-wise mean

  Returns
    ts (n_parcel x n_tp array): Array of BOLD data values

  """
  # Get the list relative 0-based index of runs to use
  if runs is None:
    runs = range(N_RUNS_REST) if name == "rest" else range(N_RUNS_TASK)
  elif isinstance(runs, int):
    runs = [runs]

  # Get the first (1-based) run id for this experiment 
  offset = get_image_ids(name)[0]

  # Load each run's data
  bold_data = [
      load_single_timeseries(subject, offset + run, remove_mean) for run in runs
  ]

  # Optionally concatenate in time
  if concat:
    bold_data = np.concatenate(bold_data, axis=-1)

  return bold_data


def load_single_timeseries(subject, bold_run, remove_mean=True):
  """Load timeseries data for a single subject and single run.
  
  Args:
    subject (int): 0-based subject ID to load
    bold_run (int): 1-based run index, across all tasks
    remove_mean (bool): If True, subtract the parcel-wise mean

  Returns
    ts (n_parcel x n_timepoint array): Array of BOLD data values

  """
  bold_path = f"{HCP_DIR}/subjects/{subject}/timeseries"
  bold_file = f"bold{bold_run}_Atlas_MSMAll_Glasser360Cortical.npy"
  ts = np.load(f"{bold_path}/{bold_file}")
  if remove_mean:
    ts -= ts.mean(axis=1, keepdims=True)
  return ts

def load_evs(subject, name, condition):
  """Load EV (explanatory variable) data for one task condition.

  Args:
    subject (int): 0-based subject ID to load
    name (str) : Name of task
    condition (str) : Name of condition

  Returns
    evs (list of dicts): A dictionary with the onset, duration, and amplitude
      of the condition for each run.

  """
  evs = []
  for id in get_image_ids(name):
    task_key = BOLD_NAMES[id - 1]
    ev_file = f"{HCP_DIR}/subjects/{subject}/EVs/{task_key}/{condition}.txt"
    ev_array = np.loadtxt(ev_file, ndmin=2, unpack=True)
    ev = dict(zip(["onset", "duration", "amplitude"], ev_array))
    evs.append(ev)
  return evs