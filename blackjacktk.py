from tkinter import *
from random import choice
from PIL import Image, ImageTk

#Подсчёт карт
def card_score(card):
    if card in ["J", "Q", "K"]:
        return 10
    elif card == "A":
        return 11
    else:
        return int(card)

#Генерация случайной карты
def generate_card():
    card = choice(card_list)
    suit = choice(suit_list)
    return card, suit

#Загрузка изображения карты
def load_card_image(path):
    image = Image.open(path).convert("RGBA")
    return ImageTk.PhotoImage(image)

#Кнопка "Play Again"
def show_play_again():
    btn_hit.place_forget()
    btn_stand.place_forget()
    btn_play_again.place(x=385, y=560)

#Функция для кнопки "Play Again"
def reset_game():
    global place_player, place_dealer

    for i in card_labels:
        i.destroy()
    card_labels.clear()

    player_images.clear()
    dealer_images.clear()
    sum_player.clear()
    sum_dealer.clear()

    place_player = 347
    place_dealer = 471

    btn_hit['state'] = 'normal'
    btn_stand['state'] = 'normal'
    btn_hit.place(x=365, y=560)
    btn_stand.place(x=455, y=560)
    btn_play_again.place_forget()

    #Карты дилера
    img_back = load_card_image('cards/cardback.png')
    lbl_back = Label(root, image=img_back, bg='#35654d')
    lbl_back.place(x=409, y=20)
    card_labels.append(lbl_back)
    dealer_images.append(img_back)

    card, suit = generate_card()
    img = load_card_image(f'cards/{card}-{suit}.png')
    lbl = Label(root, image=img, bg='#35654d')
    lbl.place(x=347, y=20)
    card_labels.append(lbl)
    dealer_images.append(img)

    score = card_score(card)
    sum_dealer.append(score)
    score_label_d.config(text=f"Dealer: {sum(sum_dealer)}")

    #Карты игрока
    for i in range(2):
        card, suit = generate_card()
        img = load_card_image(f'cards/{card}-{suit}.png')
        lbl = Label(root, image=img, bg='#35654d')
        lbl.place(x=place_player, y=320)
        card_labels.append(lbl)
        player_images.append(img)
        score = card_score(card)
        sum_player.append(score)
        place_player += 62

    if sum(sum_player) == 22:
        sum_player.remove(11)
        sum_player.append(1)

    score_label.config(text=f"Player: {sum(sum_player)}")


player_images = []
dealer_images = []
card_labels = []

place_player = 471
place_dealer = 471

#Кнопка "Hit"
def hit():
    global place_player
    card, suit = generate_card()
    img = load_card_image(f'cards/{card}-{suit}.png')
    player_images.append(img)
    lbl = Label(root, image=img, bg='#35654d')
    lbl.place(x=place_player, y=320)
    card_labels.append(lbl)
    place_player += 62

    score = card_score(card)
    sum_player.append(score)

    if sum(sum_player) > 21 and 11 in sum_player:
        sum_player.remove(11)
        sum_player.append(1)

    score_label.config(text=f"Player: {sum(sum_player)}")

    if sum(sum_player) > 21:
        total = Label(root, text="You lost!", font=('Arial', 25, 'bold'), bg='#35654d', fg='red')
        total.place(x=363, y=245)
        card_labels.append(total)
        show_play_again()

#Кнопка "Stand"
def stand():
    btn_hit['state'] = 'disabled'
    btn_stand['state'] = 'disabled'

    card, suit = generate_card()
    img = load_card_image(f'cards/{card}-{suit}.png')
    dealer_images.append(img)
    lbl = Label(root, image=img, bg='#35654d')
    lbl.place(x=409, y=20)
    card_labels.append(lbl)

    score = card_score(card)
    sum_dealer.append(score)

    if sum(sum_dealer) == 22 and 11 in sum_dealer:
        sum_dealer.remove(11)
        sum_dealer.append(1)

    score_label_d.config(text=f"Dealer: {sum(sum_dealer)}")

    root.after(1000, next)

def next():
    global place_dealer
    if sum(sum_dealer) <= 16:
        card, suit = generate_card()
        img = load_card_image(f'cards/{card}-{suit}.png')
        dealer_images.append(img)
        lbl = Label(root, image=img, bg='#35654d')
        lbl.place(x=place_dealer, y=20)
        card_labels.append(lbl)
        place_dealer += 62

        score = card_score(card)
        sum_dealer.append(score)

        if sum(sum_dealer) > 21 and 11 in sum_dealer:
            sum_dealer.remove(11)
            sum_dealer.append(1)

        score_label_d.config(text=f"Dealer: {sum(sum_dealer)}")
        root.after(1000, next)
    else:
        result()

def result():
    if sum(sum_dealer) > 21:
        total = Label(root, text="You won!", font=('Arial', 25, 'bold'), bg='#35654d', fg='green2')
        total.place(x=360, y=245)
        card_labels.append(total)
    elif sum(sum_dealer) == sum(sum_player):
        total = Label(root, text="Draw!", font=('Arial', 25, 'bold'), bg='#35654d', fg='LightCyan4')
        total.place(x=385, y=245)
        card_labels.append(total)
    elif sum(sum_dealer) > sum(sum_player):
        total = Label(root, text="You lost!", font=('Arial', 25, 'bold'), bg='#35654d', fg='red')
        total.place(x=363, y=245)
        card_labels.append(total)
    else:
        total = Label(root, text="You won!", font=('Arial', 25, 'bold'), bg='#35654d', fg='green2')
        total.place(x=360, y=245)
        card_labels.append(total)

    show_play_again()

#Колода
suit_list = ['C', 'D', 'H', 'S']
card_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
sum_player = []
sum_dealer = []

root = Tk()
root.title('BlackJack')
root.iconbitmap('cards/icon1.ico')
root.geometry('880x600+520+240')
root.config(bg='#35654d')
root.resizable(width=False, height=False)

#Кнопки
btn_hit = Button(root, text='Hit', font=('Arial', 13, 'bold'), width=5, command=hit)
btn_hit.place(x=365, y=560)

btn_stand = Button(root, text='Stand', font=('Arial', 13, 'bold'), width=5, command=stand)
btn_stand.place(x=455, y=560)

btn_play_again = Button(root, text='Play again', font=('Arial', 13, 'bold'), width=10, command=reset_game)

#Карты дилера
img_back = load_card_image('cards/cardback.png')
lbl_back = Label(root, image=img_back, bg='#35654d')
lbl_back.place(x=409, y=20)
card_labels.append(lbl_back)

card, suit = generate_card()
img = load_card_image(f'cards/{card}-{suit}.png')
lbl = Label(root, image=img, bg='#35654d')
lbl.place(x=347, y=20)
card_labels.append(lbl)
dealer_images.append(img)

score = card_score(card)
sum_dealer.append(score)

#Счёт дилера
score_label_d = Label(root, text=f"Dealer: {sum(sum_dealer)}", font=('Arial', 18, 'bold'), bg='#35654d', fg='white')
score_label_d.place(x=115, y=100)

#Карты игрока
place_player = 347
for i in range(2):
    card, suit = generate_card()
    img = load_card_image(f'cards/{card}-{suit}.png')
    lbl = Label(root, image=img, bg='#35654d')
    lbl.place(x=place_player, y=320)
    card_labels.append(lbl)
    player_images.append(img)
    score = card_score(card)
    sum_player.append(score)
    place_player += 62

if sum(sum_player) == 22:
    sum_player.remove(11)
    sum_player.append(1)

#Счёт игрока
score_label = Label(root, text=f"Player: {sum(sum_player)}", font=('Arial', 18, 'bold'), bg='#35654d', fg='white')
score_label.place(x=115, y=400)

root.mainloop()