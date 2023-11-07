import PySimpleGUI as sg
from data_structures.stack import Stack
from data_structures.linked_list import LinkedList
import serial

sg.theme('LightBlue7')  

product_prices = {
    "Kahve": 5.0,
    "Çay": 2.0,
    "Su": 1.0,
    "Portakal suyu": 4.0,
    "Limonata": 3.0,
    "Meyve suyu": 4.0,
    "Soda": 2.5,
    "Milkshake": 6.0,
    "Kola": 2.5,
    "İçeceğiniz 10": 3.0,
    "Sütlaç": 8.0,
    "Baklava": 10.0,
    "Sütlü": 7.0,
    "Kesme Şeker": 6.0,
    "Pamuk Şeker": 5.0
}

drinks = LinkedList()
drinks.append("Kahve")
drinks.append("Çay")
drinks.append("Su")

desserts = LinkedList()
desserts.append("Sütlaç")
desserts.append("Baklava")
desserts.append("Sütlü")

shopping_cart = Stack()
item_count = 0  
total_price = 0.0  

def create_page_layout(page_name, data_structure):
    layout = [
        [sg.Text(f'This is {page_name}')],
    ]

    if data_structure is not None:
        current = data_structure.head
        while current:
            layout.append([sg.Button(current.data)])
            current = current.next
    return layout

def create_product_buttons(product_list):
    product_buttons = []
    for product in product_list:
        product_buttons.append(sg.Button(product, key='-PRODUCT-', size=(12, 1)))
    return product_buttons

product_buttons = create_product_buttons(product_prices.keys())

layout_main = [
    [sg.TabGroup([
        [sg.Tab('İçecekler', create_page_layout('İçecekler', drinks)),
         sg.Tab('Tatlılar', create_page_layout('Tatlılar', desserts)),
         sg.Tab('Yemekler', create_page_layout('Yemekler', None))]
    ])],
    [sg.Text('Alışveriş Sepeti', font=('Helvetica', 12))],
    [sg.Listbox(values=[], size=(40, 4), key='-CART-')],
    [sg.Button('Çıkart', size=(12, 1))],
    [sg.Text('Toplam Fiyat: $0.00', size=(20, 1), key='-TOTAL-')],
    [sg.Button('Satışı Tamamla', size=(15, 1))],  
]

window = sg.Window('Alışveriş Sepeti', layout_main, size=(500, 500))

def print_receipt(cart, total_price):
    ser = serial.Serial('/dev/tty15', 9600, timeout=1)  
    receipt_header = "Alışveriş Fişi\n\n"
    ser.write(receipt_header.encode('utf-8'))
    for item in cart:
        product_name, product_price = item
        line = f"{product_name}: ${product_price:.2f}\n"
        ser.write(line.encode('utf-8'))
    total_line = f"\nToplam: ${total_price:.2f}\n"
    ser.write(total_line.encode('utf-8'))
    receipt_footer = "\nTeşekkür ederiz!"
    ser.write(receipt_footer.encode('utf-8'))
    ser.close()

def update_total_price():
    cart_total = sum(item[1] for item in shopping_cart.items)
    window['-TOTAL-'].update(f'Toplam Fiyat: ${cart_total:.2f}')

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
            print_receipt(shopping_cart.items, total_price)
            sg.popup("Satış tamamlandı. Fiş yazdırıldı.")

window.close()
