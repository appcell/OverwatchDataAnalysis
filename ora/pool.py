import multiprocessing as mp

def initPool():
	global PROCESS_POOL

	# More than 12 processes makes no sense with our use case
	PROCESS_POOL = mp.Pool(processes=min(mp.cpu_count(), 12)) 