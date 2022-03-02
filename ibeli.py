from bs4 import BeautifulSoup
import random
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import time, sleep

def main():
    print("Welcome to my Monitored Bot...")
    print("The Script is Running...")
    baseurl = 'https://ibeli.com/'

    headers = {
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }

    r = requests.get('https://ibeli.com/gdboutique/pl/all-products')
    soup = BeautifulSoup(r.content, 'html.parser')
    productlist = soup.find_all("div", class_="item-title")

    productlinks = []

    for item in productlist:
        for link in item.find_all("a", href=True):
            productlinks.append(baseurl + link['href'])

    # testlink = 'https://ibeli.com/gdboutique/pd/-%e7%b4%94%e6%ad%a3%e5%8a%a0%e6%96%99%e9%bb%91%e9%87%91%e7%94%98%e6%96%87%e7%85%99-%e3%80%90%e7%89%b9%e7%b4%9a%e5%8a%a0%e5%bc%b7%e7%89%88%e3%80%91--pure-black-gold-kemenyan-with-addition-ingredients-%e3%80%90extra-strong-edition%e3%80%91--1-%e5%a5%97-set-2-%e5%8c%85-pkt-.uid_20157'

    for link in productlinks:
        r1 = requests.get(link)

        soup = BeautifulSoup(r1.content, 'html.parser')

        name = soup.find(class_='item-title').text.strip()
        availability = soup.find('p', class_='style1').text.strip()
        price = soup.find('span', class_='price1').text.strip()

        AllItems = {
            'Name' : name,
            'Availability' : availability,
            'Price' : price,
        }

        if availability == 'Availability: Out of Stock':
            whcolor = 'e83845'
        else:
            whcolor = '64FF33'

        # if availability == 'Availability: Out of Stock':
        #     return
            
        # else:
        webhook = DiscordWebhook(url="<INSERT YOUR DISCORD WEBHOOK>", username="Golden Dragon Boutique")

        embed = DiscordEmbed(
            title= name, description= "GOLDEN DRAGON BOUTIQUE", color= whcolor
        )
        embed.set_thumbnail(url='https://cp.ibeli.com/App_ClientFile/2B1A9183-C79A-4BA1-825B-50C6FAAF5FEF/General/4e751b12-9b85-4e10-afa8-67a79911ff00.jpg?v=1')
        embed.set_timestamp()
        # Set `inline=False` for the embed field to occupy the whole line
        embed.add_embed_field(name="Avalaiblity:", value= availability, inline=False)
        embed.add_embed_field(name="Price:", value= price, inline=False)
        embed.add_embed_field(name="Link:", value= link)


        webhook.add_embed(embed)
        response = webhook.execute()
    

if __name__ == '__main__':
    for i in range(20):
        main()
        print(i, "Completed. Will start in 60 seconds!")
        sleep(60)
        
