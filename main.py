import PySimpleGUI as sg
from data_structures.stack import Stack
from data_structures.linked_list import LinkedList
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import random
import base64

sg.theme('LightBlue7')

product_prices = {
    "Kahve": 45.0,
    "Çay": 15.0,
    "Su": 5.0,
    "MilkShake": 38.0,
    "Bubble Tea": 65.0,
    "Soğuk Kahve": 53.5,
    "Sütlaç": 32.5,
    "Baklava": 95.99,
    "Kek": 35.0,
    "Pasta": 35.0,
    "CheeseCake": 74.75,
}



drinks = LinkedList()
drinks.append("Kahve")
drinks.append("Çay")
drinks.append("Su")
drinks.append("MilkShake")
drinks.append("Bubble Tea")
drinks.append("Soğuk Kahve")

desserts = LinkedList()
desserts.append("Sütlaç")
desserts.append("Baklava")
desserts.append("Kek")
desserts.append("Pasta")
desserts.append("CheeseCake")



shopping_cart = Stack()
item_count = 0
total_price = 0.0


def create_receipt(shopping_cart, total_price):
    order_number = random.randint(10, 100)
    file_name = f"restaurant_receipt_{order_number}.pdf"
    c = canvas.Canvas(file_name, pagesize=(68, 150))
    c.setFont("Helvetica", 3)
    page_width, page_height = (68, 150)
    order_time = time.strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(5, page_height - 5, "RESTORAN ADI: YALOVA UNIVERSITESI")
    c.drawString(5, page_height - 20, "SAAT: " + order_time)
    c.drawString(5, page_height - 35, "SIPARIS NUMARASI: " + str(order_number))
    y = page_height - 65
    for item, price in shopping_cart:
        c.drawString(5, y, f"{item} x 1")
        c.drawString(35, y, f"TL{price:.2f}")
        y -= 12
    y -= 20
    c.drawString(5, y, "Toplam Fiyat:")
    c.drawString(35, y, f"TL{total_price:.2f}")
    c.rect(2, 2, page_width - 4, page_height - 4)
    c.showPage()
    c.save()

def create_page_layout(page_name, data_structure):
    layout = [
        [sg.Text(f'{page_name}')],
    ]

    if data_structure is not None:
        current = data_structure.head
        while current:
            layout.append([sg.Button(current.data)])
            current = current.next
    return layout




layout_main = [
    [sg.TabGroup([
        [sg.Tab('İçecekler', create_page_layout('İçecekler', drinks)),
         sg.Tab('Tatlılar', create_page_layout('Tatlılar', desserts)),
         sg.Tab('Yemekler', create_page_layout('Yemekler', None))]
    ])],
    [sg.Text('Alışveriş Sepeti', font=('Helvetica', 12))],
    [sg.Listbox(values=[], size=(40, 4), key='-CART-')],
    [sg.Button('Çıkart', size=(12, 1))],
    [sg.Text('Toplam Fiyat: TL0.00', size=(20, 1), key='-TOTAL-')],
    [sg.Button('Satışı Tamamla', size=(15, 1))],
]

window = sg.Window('Alışveriş Sepeti', layout_main, size=(500, 500))

def update_total_price():
    cart_total = sum(item[1] for item in shopping_cart.items)
    window['-TOTAL-'].update(f'Toplam Fiyat: TL{cart_total:.2f}')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event in product_prices:
        product_name = event
        product_price = product_prices[event]
        shopping_cart.push((product_name, product_price))
        item_count += 1
        window['-CART-'].update(values=shopping_cart.items)
        total_price += product_price
        update_total_price()
    elif event == 'Çıkart':
        if item_count > 0:
            item_name, item_price = shopping_cart.pop()
            item_count -= 1
            window['-CART-'].update(values=shopping_cart.items)
            total_price -= item_price
            update_total_price()
    elif event == 'Satışı Tamamla':
        if item_count > 0:
            create_receipt(shopping_cart.items, total_price)
            sg.popup("Satış tamamlandı. Fiş yazdırıldı.")

window.close()
