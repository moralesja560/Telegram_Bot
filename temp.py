while True:
	offset = load_finished
	#get the updates 
	updates = get_Telegram_updates(offset)
	#create a list of each telegram updates
	upds = []
	rows = load_finished()
	for update in updates:
		upds.append(update)
	#a loop to check if update exists

	for upd in upds:
		if int(upd['update_id']) in rows:
			print(f"id {upd['update_id']} ya fue respondido.")
		else:
			try:
				#check if the update is a message
				userID = str(upd['message']['from']['id'])
				TelegramCommand = str(upd['message']['text'])
			except:
				#nop. it wasn't a message
				print(f"el mensaje con id {upd['update_id']} no es un mensaje de comando")
			else:
				##yes it was a message
				#add the id to the database
				userID = str(upd['message']['from']['id'])
					#check the text user sent
				print(f"el update {upd['update_id']} usuario {userID} envió el texto: {TelegramCommand}")
				if TelegramCommand == '/info':
					send_message(userID,quote('Claro que si!'),token)
				#answer it

				#save it
		register_finished.append(upd['update_id'])
	if len(register_finished) >0:
		log_finished(register_finished)
	else:
		print("nada que agregar")
	time.sleep(20)