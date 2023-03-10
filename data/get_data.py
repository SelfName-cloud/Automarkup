import os
import requests
import io
from PIL import Image

urls = [
    'https://userpic.fishki.net/2016/04/04/1039965/5a25011b4139fb036e885949a4da58fb.jpg', #Dicaprio
    'https://cinewest.ru/wp-content/uploads/2017/05/Molodye-amerikanskie-aktyory-Gollivuda-1.jpg',#Henly
    'https://nationmagazine.ru/upload/medialibrary/2f9/2f94b6b1336ea6becbdebd0e100eb780.jpg',#Robert
    'https://i.pinimg.com/originals/26/3d/6a/263d6aeaa871337b997dced6e17aba21.jpg',#Renny
    'https://i.pinimg.com/originals/44/8b/89/448b894ea5c9f7aabd1b839fc1e7819b.jpg',#Renny
    'https://krot.info/uploads/posts/2019-09/1569415185_seksualnaja-jendrju-garfild-67.jpg', #Renny
    'https://wallbox.ru/resize/1024x1024/wallpapers/main/201523/97120f594c6fea3.jpg',#Walter
    'https://i.artfile.ru/4256x2832_1439357_[www.ArtFile.ru].jpg',#Dicaprio
    'https://i.ytimg.com/vi/Jpt4Eym1K84/maxresdefault.jpg',#Poul
    'https://i.pinimg.com/originals/27/a3/e3/27a3e3008856515cd89831b49014b090.jpg',#Robert
    'https://i.artfile.ru/3840x2400_1439342_[www.ArtFile.ru].jpg',#Nikolos
    'https://sun9-71.userapi.com/Pl2TXq8EulqG2P5QtzmQiW0PaROSfrIRctf1AQ/eA1dl6pSVK4.jpg',#Nikolos
    'https://avatarko.ru/img/kartinka/1/znamenitosti_Angelina_Jolie.jpg',#Angelina
    'https://www.startfilm.ru/images/base/person/29_07_16/10393_38005_hqcb_keira_knightley_white_11_123_240lo.jpg',#Kira
    'https://salon.su/images/stories/articles/news/moviemusic/angelina-jolie-highest-paid-actress.jpg',#Angelina
    'https://www2.pictures.fp.zimbio.com/Nicolas+Cage+Nicholas+Cage+David+Letterman+LdHdvvnBnXDl.jpg',#Nikolos
    'https://cdnn1.lt.sputniknews.com/img/07e5/0c/10/20506378_0:59:2949:1718_1280x0_80_0_0_8463b228e53511139c6d7592ff02c358.jpg',#Kira
    'https://f.otzyv.ru/f/kino/2015/4821/1908151228192.jpg',#Nikolos
    'https://s1.1zoom.ru/big0/998/346370-pinkoo39.jpg',#Jennyfer
    'https://rossoshru.ru/wp-content/uploads/2020/04/121.jpg',#Kira
    'https://horrorzone.ru/uploads/jessica-alba/jessica-albawallpaper04.jpg',#Jessica
    'https://i.pinimg.com/736x/20/10/bd/2010bd53e31b5647abc5afffcb4092c8.jpg'#Jennyfer
]


def get_image(url, title):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    image.save("dataset/{}.jpg".format(title))


def main():
    try:
        os.makedirs('dataset')
    except FileExistsError:
        print('Its dir exists')
    for idx, url in enumerate(urls):
        get_image(url, f'img{idx}') #Загрузка изобржений


if __name__ == '__main__':
    main()