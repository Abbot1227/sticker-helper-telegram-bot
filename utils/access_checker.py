ADMIN_ID = '2011969371'

def check_status(user_id: str) -> bool:
	if user_id == ADMIN_ID:
		return True

	else:
		return False