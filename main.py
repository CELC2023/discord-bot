import discord
from discord.ext import commands
import os
#from dotenv import load_dotenv
import pandas as pd

#Side note, "pip install py-cord" is required, be sure to also "pip uninstall discord.py" to prevent conflicts
bot = commands.Bot(intents = discord.Intents.all()) #Create default bot

#load_dotenv() #Load Environment Files
TOKEN = ("MTAxMzIxNzkwMjU2NjA2NDE4MA.G775Pb.qvj_qZPZPWUDiv8IqrtiKKlwDvdRO1GI-JAzHY") #Obtain Discord API Token from .Env File

#Other static variables
guild_ids_list=[1000686343761973338, 1013218114948833331] #Put discord server id here

#Config Roles
verificationRoleName = "Verified || Vérifié" #RoleName for Verified Role to check against

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for new peeps!"))
    print('{0.user} has been started'.format(bot))


#================= Helper Functions =================
#Helper function to set role that already exists
async def assignRole(ctx, RoleName):
    member_role = discord.utils.get(ctx.guild.roles, name=f"{RoleName}")
    await ctx.author.add_roles(member_role)

#================= Helper Functions =================
#Helper function to set role that already exists
async def assignNewRole(ctx, RoleName):
    #Check to see if that role already exists
    try:
        #If role exists, Add
        member_role = discord.utils.get(ctx.guild.roles, name=f"{RoleName}")
        await ctx.author.add_roles(member_role)
    except:
        #If role does not exist, create a random colour first //Feature turned off
        #random_colour = random.randint(0,16777215)
        #await ctx.guild.create_role(name=f"{RoleName}", colour=discord.Colour(random_colour))

        #Plain Colour
        await ctx.guild.create_role(name=f"{RoleName}")
        new_member_role = discord.utils.get(ctx.guild.roles, name=f"{RoleName}")
        await ctx.author.add_roles(new_member_role)

#Checks email against the datasheet
def verifyData(ctx, email):
    df = pd.read_csv('DiscordDatabase.csv', encoding='utf-8', index_col = "email")
    try: 
        nickname = df.loc[email, 'nickname']
        pronouns_check = df.loc[email, 'pronouns']
        if pd.isna(pronouns_check):
            pronouns = ""
        else:
            pronouns = df.loc[email, 'pronouns']

        school = df.loc[email, 'school']
        region_check = df.loc[email, 'region']
        if pd.isna(region_check):
            region = ""
        else:
            region = df.loc[email, 'region']
        return [nickname, pronouns, school.replace("Ã©","é"), region.replace("Ã©","é")]
    except:
        #Email not at all in database
        return ["ERROR_NONEXISTENT", "", "", ""] #Return error for no email existing in the system

async def changeNickname(ctx, name, school):
    nickname = f'{name}'
    try:
        await ctx.author.edit(nick=nickname)
    except:
        print("Admin attempted to change nickname")

#================= Commands =================

#Verify
@bot.slash_command(name = "verify", guild_ids = guild_ids_list, description = "/verify <email> to gain access to other channels")

async def verify(ctx, email: discord.Option(str)): #Create verify command expecting one input
    if email == None: #Error message is someone puts something invalid
        await ctx.respond("No Arguments!", ephemeral=True) 
    else:
        #Check to see if they are already verified
        #Assign roles based on database query
        verified_role = discord.utils.get(ctx.author.roles, name=f"{verificationRoleName}")
        if verified_role is not None and verified_role.name == f"{verificationRoleName}":
            await ctx.respond(f"You have already been verified. If you are experiencing any technical issues, please DM one of our administrators or contact us at chair@celc.cfes.ca \nVous avez déjà été vérifié. Si vous rencontrez des problèmes de nature technique, veuillez communiquer avec l'un de nos administrateurs ou nous contacter à l'adresse suivante : register@celc.cfes.ca.", ephemeral=True) #Response
        else:
            data = verifyData(ctx, email.lower())
            match data[0]:
                #Very YOLO Python State Handler
                case "ERROR_NONEXISTENT":
                    await ctx.respond(f"{email} is not in our system, please confirm that you are using the same email that you used to register for CELC delegate registration \n{email} n'est pas dans notre système. Veuillez confirmer que vous utilisez le même courriel que celui utilisé pour l'inscription des délégués de la CCLI.", ephemeral=True) #Response Message
                case "ERROR_USED":
                    await ctx.respond(f"{email} has already been used for verification, if you believe this is an error, please DM one of our administrators or contact us at chair@celc.cfes.ca \n{email} a déjà été utilisé pour la vérification. Si vous pensez qu'il s'agit d'une erreur, veuillez envoyer un message à l'un de nos administrateurs ou nous contacter à l'adresse register@celc.cfes.ca.", ephemeral=True) #Response message
                case _:
                    await ctx.respond(f"Thank you {data[0]}, you have now been verified on the CELC 2023 Discord! Welcome aboard and hope to see you soon in Calgary! \nMerci {data[0]}, vous avez maintenant été vérifié sur le Discord CCLI 2023 ! Bienvenue à bord et nous espérons vous voir bientôt à Calgary!", ephemeral=True) #Response message
                    await assignRole(ctx, verificationRoleName) #Assign verified role
                    await changeNickname(ctx, data[0], data[2]) #Assign Nickname
                    if data[1] is None or data[1] == "":
                        pass
                    else:
                        await assignNewRole(ctx, data[1]) #Assign Pronouns
                    await assignNewRole(ctx, data[2]) #Assign School
                    if data[3] is None or data[3] == "":
                        pass
                    else:
                        await assignNewRole(ctx, data[3]) #Assign Region
            #Response message

@bot.slash_command(name = "vérifié", guild_ids = guild_ids_list, description = "/vérifié <email> pour recevoir accès aux autres forums")

async def vérifié(ctx, email: discord.Option(str)): #French Version
    if email == None: #Error message is someone puts something invalid
        await ctx.respond("No Arguments!", ephemeral=True) 
    else:
        #Check to see if they are already verified
        #Assign roles based on database query
        verified_role = discord.utils.get(ctx.author.roles, name=f"{verificationRoleName}")
        if verified_role is not None and verified_role.name == f"{verificationRoleName}":
            await ctx.respond(f"Vous avez déjà été vérifié. Si vous rencontrez des problèmes de nature technique, veuillez communiquer avec l'un de nos administrateurs ou nous contacter à l'adresse suivante : register@celc.cfes.ca.", ephemeral=True) #Response
        else:
            data = verifyData(ctx, email.lower())
            match data[0]:
                #Very YOLO Python State Handler
                case "ERROR_NONEXISTENT":
                    await ctx.respond(f"{email} n'est pas dans notre système. Veuillez confirmer que vous utilisez le même courriel que celui utilisé pour l'inscription des délégués de la CCLI.", ephemeral=True) #Response Message
                case "ERROR_USED":
                    await ctx.respond(f"{email} a déjà été utilisé pour la vérification. Si vous pensez qu'il s'agit d'une erreur, veuillez envoyer un message à l'un de nos administrateurs ou nous contacter à l'adresse register@celc.cfes.ca.", ephemeral=True) #Response message
                case _:
                    await ctx.respond(f"Merci {data[0]}, vous avez maintenant été vérifié sur le Discord CCLI 2023 ! Bienvenue à bord et nous espérons vous voir bientôt à Calgary!", ephemeral=True) #Response message
                    await assignRole(ctx, verificationRoleName) #Assign verified role
                    await changeNickname(ctx, data[0], data[2]) #Assign Nickname
                    if data[1] is None or data[1] == "":
                        pass
                    else:
                        await assignNewRole(ctx, data[1]) #Assign Pronouns
                    await assignNewRole(ctx, data[2]) #Assign School
                    if data[3] is None or data[3] == "":
                        pass
                    else:
                        await assignNewRole(ctx, data[3]) #Assign Region
            #Response message
#=============================================
bot.run(TOKEN) #Run the client with the token