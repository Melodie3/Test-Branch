import random
import asyncio
import importlib
import typing
import discord
import string
import re

from discord.ext import commands

import verification
import emoji

import bread.utility as utility

#from verification import from_mildly_disliked, from_owner
#from verification import from_friend
#from verification import from_enemy
#from verification import get_rejection_reason

require_politeness = True

@commands.command(
    brief="Says Hello."
)
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')


magic_8_ball_answers = ["● It is certain.",
                        "● It is decidedly so.",
                        "● Without a doubt.",
                        "● Yes definitely.",
                        "● You may rely on it.",

                        "● As I see it, yes.",
                        "● Most likely.",
                        "● Outlook good.",
                        "● Yes.",
                        "● Signs point to yes.",

                        "● Reply hazy, try again.",
                        "● Ask again later.",
                        "● Better not tell you now.",
                        "● Cannot predict now.",
                        "● Concentrate and ask again.",

                        "● Don't count on it.",
                        "● My reply is no.",
                        "● My sources say no.",
                        "● Outlook not so good.",
                        "● Very doubtful."]


calculating_analysis = False
analysis_responses_common = ["Stockfish says it is a losing position.",
                                "Extremely Unlikely.",
                                "Unlikely.",
                                "Models say No.",
                                "No, with a 95% certainty.",
                                "No, with a 80% certainty.",
                                "No, with a 50% certainty.",
                                
                                "I cannot say one way or the other.",
                                "Perhaps.",
                                "Potentially.",
                                "Insufficent information.",
                                "It is impossible to tell.",
                                "Too many variables.",
                                "Stockfish says it is an even position.",
                                "Ask Petrosian.",

                                "It seems likely to me.",
                                "Models have high confidence.",
                                "Models say yes.",
                                "I believe so.",
                                "Yes, with a 50% certainty.",
                                "Yes, with a 75% certainty.",
                                "Yes, with a 90% certainty.",
                                "I think it is true.",
                                "Likely.",
                                "Extremely Likely.",
                                "Stockfish says it is a winning position.",
                                "Stochastic models say yes.",
                                "I would say yes."]

analysis_responses_rare = ["I would not bet your Elo on it.",
                            "Petrosian would have better odds.",
                            "Levy is on your side.",
                            "Is there a chance you could blindfold your opponent?",
                            "It appears your opponent is blindfolded.",
                            "I give it queen's odds.",
                            "Stockfish crashed when the question was entered.",
                            "Some of life's questions shall remain mysteries.",
                            "Error. Attention shoppers, the store will be closing shortly. Please take all final purchases up to the register.",
                            "Error. This answer brought to you by Skillshare. Check out a link in the video description.",
                            "I do not like the form the question was asked in.",
                            "Question formatting error, process exited with code 12.",]

@commands.command(
    brief = "Answers a yes or no question",
    help = "Uses stochastic analysis to determine an answer to a yes or no question.\n\nResults provided as-is.\n\nRely on them at your own risk.",
    aliases = ["analyze", "analysis:", "analyze:"]
)
async def analysis(ctx):
    global calculating_analysis

    if calculating_analysis:
        await ctx.reply("I said please wait. I can only answer one question at a time.")
        return

    calculating_analysis = True
    wait_text = "Calculating an answer."
    message = await ctx.send(wait_text)
    await asyncio.sleep(1)

    if random.randint(1,100) < 80: #80% chance
        wait_text +=  "\n\nPlease wait."
        await message.edit(content = wait_text)
        await asyncio.sleep(1)

        while random.randint(1,8) != 1:
            #25% chance to end each round
            wait_text += "..."
            await message.edit(content = wait_text)
            await asyncio.sleep(1)
    
    analysis = "Analysis: "
    
    if random.randint(1,20): #5% chance
        #choose from all responses
        analysis += random.choice(analysis_responses_common+analysis_responses_rare)
    else:
        #90% chance to choose from only common responses
        analysis += random.choice(analysis_responses_common)

    try:
        await ctx.reply(analysis)
    except:
        await ctx.send(analysis)
        
    calculating_analysis = False
    return


@commands.command(
    aliases=["thank", "thanks!", "thanks."],
    brief="Thanks the bot."
)
async def thanks(ctx):
    await ctx.send("You're welcome!")

@commands.command(
    hidden=True
)
async def emergency_meeting(ctx):
    text = emoji.amogus + " " + emoji.amogus + " " + emoji.amogus + " " + emoji.amogus + " " + \
             ":rotating_light:" +  \
             emoji.amogus + " " + emoji.amogus + " " + emoji.amogus + " " + emoji.amogus
    await ctx.send(text)
    await ctx.message.delete()

@commands.command(
    hidden= True,
    aliases= ["ours"]
)
async def our(ctx):
    text = "https://cdn.discordapp.com/attachments/958924344933904445/973723740301049866/unknown.png"
    print(f"granting 'our' request for {ctx.author.display_name}")
    await ctx.send(text)
    await ctx.message.delete()

@commands.command(
    hidden= True,
    aliases=["not_a_rapper"]
)
async def dayum(ctx):
    text = "https://media.giphy.com/media/AJwnLEsQyT9oA/giphy.gif"
    print(f"granting 'dayum' request for {ctx.author.display_name}")
    await ctx.send(text)
    await ctx.message.delete()

@commands.command(
    hidden= True,
)
async def bingo(ctx):
    text = "You can find the current bingo board by running \"%board\""
    await ctx.send(text)

# require proper punctuation for echo command
@commands.command(
    aliases=['echo'],
    brief = "Repeats a message, usually",
    help  = "Proper grammar is important to Machine Mind. Please include punctuation and capitalization. She also does not use chatspeak."
)
async def say(ctx, *, words):
    
    full_phrase = words
    words = words.split(" ")

    #remove all punctuation.
    words_filtered = []
    words_unfiltered = []
    for word in words:
        lower_word = word.lower()
        punctuationless_word = lower_word.translate(str.maketrans('', '', "!.?,()&%*~_"))
        if punctuationless_word != "":
            words_filtered.append(punctuationless_word)
        words_unfiltered.append(lower_word)

    if verification.from_enemy(ctx.author):
        print("ignoring echo command from member of enemy list")
        return

    # be petty
    if (verification.from_mildly_disliked(ctx.author)):
        if random.randint(0,1) == 0:
            await ctx.send("I don't know if I want to.")
            return

    if not require_politeness:
        # just send it, as Jimmer would say
        await ctx.send(full_phrase)
        return

    #check if attempt to manipulate say command
    if full_phrase.startswith("$"):
        await ctx.send("Nice try.")
        return

    #check if those bad emoji are there (they have been removed)
    #if not ((not "<:why:959245770119319593>"   in words_unfiltered) and
            #(not "<:whytf:959327131219947541>" in words_unfiltered)):
        #await ctx.send("I will not say that.")
        #return
    
    #Wanker, bitch, twat, slut, fucker.
    # check if there are bad words
    exclusion_list = [ "fuck", "fucking", "fucker", "shit", "dumb", "wank", "bitch", 
                        "frick", "fricking", "frack"
                        "twat", "slut", "penis", "sex", "cum", "balls",
                        "crap", "hell", "ass", "heck",
                        "tbh", "wtf", "lol", "lmao", "imao", "lol", "sussy baka", "dude", "bro", "bruh",
                        "daddy", "uwu", "holding hands",]
    for word in exclusion_list:
        if word in words_filtered:
            await ctx.send("No chatspeak or vulgarity, please.")
            return

    if ("love" in words_filtered) or ("hate" in words_filtered):
        await ctx.send("I experience neither love nor hate.")
        return

    # check for capitalization and punctuation
    if not (full_phrase[0].isupper()):
        if (verification.from_owner(ctx.author)):
            full_phrase = full_phrase.capitalize()
        else:
            await ctx.send("Please use proper capitalization.")
            return

    # detection of mention
    if re.search("<@&?[0-9]+>", full_phrase) is not None:
        await ctx.send("I will not @ someone for you.")
        return

    if "@everyone" in full_phrase or "@here" in full_phrase:
        await ctx.send("I will not @ everyone for you. And it is rude of you to ask me to.")
        return

    #end in punctuation
    if not full_phrase.endswith(('!', '.', '?')):
        if (verification.from_owner(ctx.author)):
            full_phrase += '.'
        else:
            await ctx.send("Please use proper grammar.")
            return

    # check for missed apostrophes
    if (("cant" in words_filtered) or
        ("wont" in words_filtered) or
        ("dont" in words_filtered) or
        ("shouldnt" in words_filtered) or
        ("im" in words_filtered) or 
        ("aint" in words_filtered) or
        ("isnt" in words_filtered) or
        ("doesnt" in words_filtered) or
        ("shouldve" in words_filtered) or
        ("couldve" in words_filtered) or
        ("wouldve" in words_filtered)):
        await ctx.send("Please use proper grammar.")
        return
    
    full_phrase = full_phrase.replace("can't", "cannot")
    full_phrase = full_phrase.replace("won't", "will not") 
    full_phrase = full_phrase.replace("don't", "do not")
    full_phrase = full_phrase.replace("shouldn't", "should not")
    full_phrase = full_phrase.replace("I'm", "I am")
    full_phrase = full_phrase.replace("I've", "I have")
    full_phrase = full_phrase.replace("I'll", "I will")
    full_phrase = full_phrase.replace("I'd", "I would")
    full_phrase = full_phrase.replace("ain't", "is not")
    full_phrase = full_phrase.replace("isn't", "is not")
    full_phrase = full_phrase.replace("doesn't", "does not")
    full_phrase = full_phrase.replace("should've", "should have")
    full_phrase = full_phrase.replace("would've", "would have")
    full_phrase = full_phrase.replace("could've", "could have")


    
    print("echo request granted for " + str(ctx.message.author) + " in channel " + str(ctx.message.channel) + " at " + str(ctx.message.created_at) + ":\n" + str(full_phrase))
    await ctx.send(full_phrase) # say message
    # if from_owner(ctx) or from_friend(ctx): # we'll just let anyone have their message deleted
    await ctx.message.delete() # delete trigger message




@commands.command(
    brief = "Verifies sender of request",
    help =  "Some commands require more status than others."
)
async def verify(ctx, user: typing.Optional[discord.Member]):
    if user is None:
        user = ctx.author

    if utility.contains_ping(user.display_name):
        name = user.name
    else:
        name = user.display_name

    output = f"Verification of {name}...\n\n" 
    descriptors = list()

    if verification.from_owner(user):
        #descriptors.append("Hello, mum.")
        await ctx.send("Hello, mum.")
        return

    if verification.from_friend(user):
        descriptors.append("Friend!")
    if verification.from_enemy(user):
        descriptors.append("Meanie.")
    if verification.from_mildly_disliked(user):
        descriptors.append("I'm not sure about you.")

    if (user.id == 350868168455094272): #treesarentreal.com
        descriptors.append("My mother told me that trees are actually real.")
    if (user.id == 763513342102208533): #ij monke
        descriptors.append("Monke?")
    if (user.id == 399291491639492621): #emptyRook
        descriptors.append("I was told you are good at transcribing things.")
    if (user.id == 303067719463600129): #zyxia
        descriptors.append("Hello Ms. Zyxia!")
    if (user.id == 461995062893608961): #prockpj
        descriptors.append("Didn't I ban you?")
    if (user.id == 1060254289899044954): #omar
        descriptors.append("The bread rolls incident :skull:")


    #Addicted to _____ Roles
    if "addicted to carpal tunnel" in [y.name.lower() for y in user.roles]:
        descriptors.append("Copy and pasting $bread so many times has left a mark on you.")
    if "addicted to roles" in [y.name.lower() for y in user.roles]:
        descriptors.append("Do you collect roles just to get more responses from this command?")
    if "addicted to bricks" in [y.name.lower() for y in user.roles]:
        descriptors.append("I feel like I've delivered a lot of bricks to you recently.")
        descriptors.append("You *do* know that bricks weren't intended for recreational use, right?")
    if "easily addicted" in [y.name.lower() for y in user.roles]:
        descriptors.append("Are you addicted to running this command?")
    if "addicted to bread" in [y.name.lower() for y in user.roles]:
        descriptors.append("How can you still be hungry after all the bread?")
        descriptors.append(":bread:")
        descriptors.append("Do you even roll bro?")
    if "addicted to stats" in [y.name.lower() for y in user.roles]:
        descriptors.append("You are too good at math for your own good.")
    if "addicted to gambling" in [y.name.lower() for y in user.roles]:
        descriptors.append("I hope you're not gambling with your life savings.")
        descriptors.append("Remember, gambling is a sin.")
    if "addicted to milk" in [y.name.lower() for y in user.roles]:
        descriptors.append("Your bones are looking strong!")
    if "addicted to evangelion" in [y.name.lower() for y in user.roles]:
        descriptors.append("You're the lowest of the low.")
    if "addicted to counting" in [y.name.lower() for y in user.roles]:
        descriptors.append("Think fast! What comes after 1841492?")
        descriptors.append("Think fast! What comes after 24905427502745?")
        descriptors.append("Think fast! What comes after 4241?")
        descriptors.append("Think fast! What comes after 2492482975?")
        descriptors.append("Think fast! What comes after 2?")
    if "not a role" in [y.name.lower() for y in user.roles]:
        descriptors.append("Why are you reading through the $verify response list?")
    if "addicted to chonny jash" in [y.name.lower() for y in user.roles]:
        descriptors.append("Call me the soul, or call me my name.")
    #Seriously Addicted to _____ Roles
    if "seriously addicted to bricks" in [y.name.lower() for y in user.roles]:
        descriptors.append("How many times will you decline en passant?")
    if "seriously addicted to gambling" in [y.name.lower() for y in user.roles]:
        descriptors.append("Positive outcome on average.")
    if "seriously addicted to bread" in [y.name.lower() for y in user.roles]:
        descriptors.append("You remember when bread was rolled on one line, don't you?")
    #Pride roles
    if "garlic bread enjoyer" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "fast walker" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "good at archery" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "kitchen pan-ic" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "bisexual mess" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "transbian thirst-trap" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "useless lesbian" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "scared of computers" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "blahaj enjoyer" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    #Miscellaneous roles
    if "bread" in [y.name.lower() for y in user.roles]:
        descriptors.append("Bread club!")
    if "moderator" in [y.name.lower() for y in user.roles]:
        descriptors.append("A moderator!")
    if "admin" in [y.name.lower() for y in user.roles]:
        descriptors.append("An amdin!")
    if "here when it all began" in [y.name.lower() for y in user.roles]:
        descriptors.append("You've been here since the very beginning.")
    if "og raid defenders" in [y.name.lower() for y in user.roles]:
        descriptors.append("Thank you for your service in defending us from raids.")
    if "old guard" in [y.name.lower() for y in user.roles]:
        descriptors.append("Hello, member of the old guard.")
    if "game night group" in [y.name.lower() for y in user.roles]:
        descriptors.append("I hope to see you at the next game night!")
    if "paperclip optimized 📎" in [y.name.lower() for y in user.roles]:
        descriptors.append("I estimate you could become approximately 10,000 paperclips.")
    if "ghomerl vs. cmauhin" in [y.name.lower() for y in user.roles]:
        descriptors.append("ghomerl vs. cmauhin")
    if "literally does care" in [y.name.lower() for y in user.roles]:
        descriptors.append("Thank you for signing up to be notified of server events!")
    if "gets pinged too much" in [y.name.lower() for y in user.roles]:
        descriptors.append("<@&967443956659019786>")
    if "hapy capy :heart:" in [y.name.lower() for y in user.roles]:
        descriptors.append("A fellow supporter of the capybaras. I tip my hat to you.")
    if "r/chess mod" in [y.name.lower() for y in user.roles]:
        descriptors.append("Hey, OP! Did your game end in a stalemate? Did you encounter a weird pawn move? Are you trying to move a piece and it's not going? We have just the resource for you!")
    if "r/anarchychess mod!!" in [y.name.lower() for y in user.roles]:
        descriptors.append("Look, it's the 1984 police.")
    if "gvc commentator" in [y.name.lower() for y in user.roles]:
        descriptors.append("Will you be returning for the rematch, commentator?")
    if "in debt" in [y.name.lower() for y in user.roles]:
        descriptors.append("Interest is piling up for your debts.")
    if "based" in [y.name.lower() for y in user.roles]:
        descriptors.append("Thank you for boosting this server and making the bread game possible!")
    if "(addicted to bricks)²" in [y.name.lower() for y in user.roles]:
        descriptors.append("Your dedication seems to know no bounds.")
    if "event coordinator (brings cookies)" in [y.name.lower() for y in user.roles]:
        descriptors.append("When is the next event?")
    if "bribed a mod" in [y.name.lower() for y in user.roles]:
        descriptors.append("Why did you bribe the mods? For fame? For power? For *bread*?")
    if "brick jailed" in [y.name.lower() for y in user.roles]:
        descriptors.append("What did you do this time?")
    if "Minecraft" in [y.name.lower() for y in user.roles]:
        descriptors.append("Have you eaten bread in Minecraft too?")
    if "31004150 player" in [y.name.lower() for y in user.roles]:
        descriptors.append(":brown_square:")
    if "the peng affair" in [y.name.lower() for y in user.roles]:
        descriptors.append("I am clean.")
    if "r/place 2023 coordinator" in [y.name.lower() for y in user.roles]:
        descriptors.append("Still waiting for r/Place 2023 huh?")
    if "ping list poster" in [y.name.lower() for y in user.roles]:
        descriptors.append("Stop using this command and go make the next ping list.")
    if "l*ndon system 🤢" in [y.name.lower() for y in user.roles]:
        descriptors.append("What compels you to play the London?")
    if "bingo-bot" in [y.name.lower() for y in user.roles]:
        descriptors.append("Hmm... Why are you running this command?")
    if "ghost council" in [y.name.lower() for y in user.roles]:
        descriptors.append("What does the Ghost Council even mean?")
    if "sus" in [y.name.lower() for y in user.roles]:
        descriptors.append("<:sus:961517169424883722>")
    if "lunatic" in [y.name.lower() for y in user.roles]:
        descriptors.append("I AM NOT CRAZY!")
    if "chess club" in [y.name.lower() for y in user.roles]:
        descriptors.append("What's your favorite opening?")
    if "strongest player in the server" in [y.name.lower() for y in user.roles]:
        descriptors.append("What's your rating?")
    if "snacqk attacqk" in [y.name.lower() for y in user.roles]:
        descriptors.append("Snacqk attacqk stays winning!")
    if "blahaj enjoyer" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "onion rebel" in [y.name.lower() for y in user.roles]:
        descriptors.append(":onion:")
    if "very chill" in [y.name.lower() for y in user.roles]:
        descriptors.append("You're cool.")
    if "the garry chess!! real!!" in [y.name.lower() for y in user.roles]:
        descriptors.append("When is your next NFT drop?")
    if "pasta cult" in [y.name.lower() for y in user.roles]:
        descriptors.append("What's your favorite pasta? I like fettucine alfredo.")
    if "furry" in [y.name.lower() for y in user.roles]:
        descriptors.append("OwO")
    if "gives bread facts" in [y.name.lower() for y in user.roles]:
        descriptors.append("Can I have a bread fact?")
    if "gives water facts" in [y.name.lower() for y in user.roles]:
        descriptors.append("Can I have a water fact?")
    if "blahaj enjoyer" in [y.name.lower() for y in user.roles]:
        descriptors.append("You seem to be a very valid person.")
    if "cvc gang" in [y.name.lower() for y in user.roles]:
        descriptors.append("Chess variants are super fun!")
    if "relevant" in [y.name.lower() for y in user.roles]:
        descriptors.append("You are relevant.")
    if "likes the rain" in [y.name.lower() for y in user.roles]:
        descriptors.append("What is it that's so great about the rain? The ambience? The feel of the water on your face? The peaceful feeling of cleansing?")
    if "some dumb shit like that" in [y.name.lower() for y in user.roles]:
        descriptors.append("W")
    if "brick dodger" in [y.name.lower() for y in user.roles]:
        descriptors.append("I'll get you next time!") 
    if "murderer" in [y.name.lower() for y in user.roles]:
        descriptors.append("Why would you do such a thing?")
    if "en passant enabler" in [y.name.lower() for y in user.roles]:
        descriptors.append("Holy Hell!")
    if "spunchrole" in [y.name.lower() for y in user.roles]:
        descriptors.append("Who lives in a pineapple under the sea?")
    if "actual redditor" in [y.name.lower() for y in user.roles]:
        descriptors.append("This!!!\nEdit: Thank for the gold!")
    if "guessed correctly" in [y.name.lower() for y in user.roles]:
        descriptors.append("What number am I holding up?")
    
        
    if len(descriptors) == 0:
        await ctx.send("Verification failed.")
    else:
        
        await ctx.send(output + random.choice(descriptors))

@commands.command(
    brief = "Change ping reply settings",
    help =  "Change your ping reply setting. 'on' to enable ping replies, 'off' to disable."
)
async def ping(
        ctx: commands.Context,
        setting: typing.Optional[str]
    ):
    try:
        json_cog = ctx.bot.json_cog
    except AttributeError:
        await ctx.reply("Unable to change setting, please try again later.")
        return
    
    new = None
    if setting is not None:
        if setting.lower() in ["on", "y", "yes", "enable"]:
            new = True
        elif setting.lower() in ["off", "n", "no", "disable"]:
            new = False
    
    data = json_cog.get_filing_cabinet(name="ping_settings", guild=ctx.guild, create_if_nonexistent=True)

    if new is None:
        new = not data.get(str(ctx.author.id), True)

    data[str(ctx.author.id)] = new

    json_cog.set_filing_cabinet(name="ping_settings", guild=ctx.guild, cabinet=data)

    if new:
        await ctx.reply("You will now be pinged in replies.")
    else:
        await ctx.reply("You will no longer be pinged in replies.")

async def setup(bot: commands.Bot):
    importlib.reload(verification)
    importlib.reload(emoji)
    importlib.reload(utility)
    bot.add_command(hello)
    #bot.add_command(echo)
    bot.add_command(verify)
    bot.add_command(say)
    #bot.add_command(bread)
    #bot.add_command(edit_test)
    bot.add_command(thanks)
    bot.add_command(analysis)
    bot.add_command(emergency_meeting)
    bot.add_command(our)
    bot.add_command(dayum)
    bot.add_command(bingo)
    bot.add_command(ping)

    return bot
