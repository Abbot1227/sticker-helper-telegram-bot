ADMIN_ID = ['SAMPLE_ID1', 'SAMPLE_ID2']

def check_status(user_id: str) -> bool:
	if user_id in ADMIN_ID:
		return True

	else:
		return False
