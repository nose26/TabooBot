#TabooBot
#Brought to you by a jackass with too much free time
#I actully can't read this code anymore.  It started out right, and then it went to shit
#Hopefully none of the errors break it, but just in case don't ever add to a server that doesn't have a general
#Anyway, cheers mate
import discord
import random
import asyncio
from itertools import cycle
import datetime as dt
import re
import time
import tabooWordClass

#Declarations should be at the top, with inconsistant spacing, like God intended

TOKEN = open('../BotTokenVault/TabooBot.txt').read() #Token seperate for security.  Works fine on my machine

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
	forbiddenWordRegex = wordStorage.getWord() #Pulls word from wrapper-thing
	if message.author == client.user:
		print("That's me")
		return
	#Is partially in a try-except, and the rest won't cause any overt issues.  Hopefully.
	elif re.search(forbiddenWordRegex, message.content) and message.server:
		msg = "It seems you've used the taboo word, \"" + wordStorage.getRawWord() + "\".  For this you will been kicked.  May the gods forgive you."
		await client.send_message(message.channel, msg)
		#the big kick
		try:
			await client.kick(message.author)
		except discord.errors.Forbidden:
			await client.send_message(message.channel, "Hmm, you aren't kicked.  Mark my words, even if I cannot punish you, the gods will.")
		return
	else:
		return

#This will change the Taboo word every day at midnight.  It's a really ghetto solution because I don't feel like putting effort into this
async def newWord():
	await client.wait_until_ready()
	counter = 0
	allowChange = True
	while not client.is_closed:
		if dt.datetime.now().hour == 0 and allowChange: #Checks time and ensures no doubles
			
			forbiddenWordInternal = pickWord() #Generates new word and passes it to the retainer class
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

		await asyncio.sleep(1) #Waits a second before checking again

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.loop.create_task(newWord())
client.run(TOKEN)
