import discord
import random
import asyncio
from itertools import cycle
import datetime as dt
import re
import time
import tabooWordClass

#Declarations should be at the top, with inconsistant spacing, like God intended

TOKEN = 'NTAzNjMxODYzNDk2MzEwNzg0.Dq-u_g.fQ4cFmMFbjFiURJ2nMmkF8rWIoE'

client = discord.Client()

singleWordRegex = re.compile(r'\w+')

wordFile = open('./200MostCommonWords')
wordText = wordFile.read()
wordFile.close()
wordList = singleWordRegex.findall(wordText)

#Picks one of the 200 most common words in the english language
def pickWord ():
	aynRand = random.randint(0 , 199) #Named because I was going to call it randInt, but that's a function.  Then rand, but that's Ayn Rand's last name.  Thus, aynRand.
	out = wordList[aynRand]
	print(out)
	return out

forbiddenWord = pickWord()

wordStorage = tabooWordClass.tabooWordClass(forbiddenWord)

print(forbiddenWord)

@client.event #Should I have cleaned this up? Yes.  Did I? No.
async def on_message(message):
	print ("------------------")
	print ("New Message: " + message.content)
	print ("As a reminder, the word is " + wordStorage.getRawWord())
	forbiddenWordRegex = wordStorage.getWord()
	if message.author == client.user:
		print("That's me")
		return
	#Should be in a try-catch, but fuck that shit
	elif re.search(forbiddenWordRegex, message.content) and message.server:
		msg = "It seems you've used the taboo word, \"" + forbiddenWord + "\".  For this you have been kicked.  May the gods forgive you, and I, for our use of this foul word."
		await client.send_message(message.channel, msg)
		#the big kick
		await client.kick(message.author)
		return
	else:
		return

#This will change the Taboo word every day at midnight.  It's a really ghetto solution because I don't feel like putting effort into this
async def newWord():
	await client.wait_until_ready()
	counter = 0
	allowChange = True
	while not client.is_closed:
		if dt.datetime.now().hour == 15 and allowChange: #Checks time and ensures no doubles
			print("THE TIME IS NIGH")
			
			forbiddenWordInternal = pickWord() #Generates new word and regex
			#forbiddenWordRegexOut = re.compile(r'(\W|^)' + forbiddenWord + '(\W|$)')

			wordStorage.setWord(forbiddenWordInternal)

			allowChange = False #No doubling allowed

			for servlad in client.servers: #Sends alert
				print(servlad.name)
				for chad in servlad.channels:
					if chad.name == "general":
						chadID = chad.id
				await client.send_message(servlad.get_channel(chadID), "@everyone Alert: the new taboo word is \"" + forbiddenWordInternal + "\"")

		if (not allowChange): #Should count out two hours before checking again
			counter = counter + 1
			if counter > 7200:
				allowChange = True
				counter = 0

		await asyncio.sleep(1)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.loop.create_task(newWord())
client.run(TOKEN)