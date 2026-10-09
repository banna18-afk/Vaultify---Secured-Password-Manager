def pass_check(user_pass):
	if len(user_pass) < 8:
		return False, 'password required minimum 8 characters'
	elif not any(u.isupper() for u in user_pass):
		return False, 'Password has not any uppercase letter'
	elif not any(u.isdigit() for u in user_pass):
		return False, 'Password has not any digit'
	elif not any(not u.isalnum() for u in user_pass):
	       return False, 'Password must contain at least one special character'
	else:
		return True, 'Password is strong'
		
		
if __name__ == '__main__':
    while True:
    	input_pass = input('Enter your password or Exit- ')
    	if input_pass == 'exit' or input_pass == 'Exit' or input_pass == 'EXIT':
    		print('Thank You! Bye Bye.')
    		break
    	is_valid, msg = pass_check(input_pass)
    	print(msg)
