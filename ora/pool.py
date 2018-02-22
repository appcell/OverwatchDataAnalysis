import multiprocessing as mp

def initPool():
	global PROCESS_POOL
	PROCESS_POOL = mp.Pool(processes=mp.cpu_count())