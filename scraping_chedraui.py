# -*- coding: utf8 -*-
#By Darian Ramos
#---------------------
from selenium import webdriver
import time

baseurl = "https://www.chedraui.com.mx/ajusco/endeca/category/view/id/457/"
xpaths = { '_item_first' : "//div[@class='item first']",
           '_item' : "//div[@class='item ']",
           '_item_last' : "//div[@class='item last']",
           '_sku_and_name' : "div[@class='product-image']/a",
           '_normal_price' : "div[@class='product-shop']/div[@class='f-fix']/div[@class='price-box']/span[@class='regular-price']/span[@class='price']",
           '_old_price' :   "div[@class='product-shop']/div[@class='f-fix']/div[@class='price-box']/div[@class='price-box']/p[@class='old-price']/span[@class='price']", 
           '_new_price' :   "div[@class='product-shop']/div[@class='f-fix']/div[@class='price-box']/div[@class='price-box']/p[@class='special-price']/span[@class='price']",
           '_price_add_to_cart' :   "div[@class='product-shop']//div[@class='f-fix']/div[@class='add-to-cart']/div[@class='product-qty']/p[@class='product-list-button']/button[@class='button btn-cart']",
           '_url_imagen' :   "div[@class='product-image']/a/img",
           '_paging' : "//a[@class='next i-next']",
           '_items_in_page' : "//select[@class='items-per-page']/option[@value='48']"
         }

""" HTML STRUCTURE WITH PROPS, WE NEED: UPC-SKU,NOMBRE,PRICE,URL IMAGE

#DIV CLASS: item first | DIV CLASS: item  | DIV CLASS: item last
    #DIV CLASS: product-image   TITLE   HREF
        #A CLASS: gtm-name  gtm-sku
            #IMG CLASS: product-image-endeca-XXXXXX
    #DIV CLASS: product-shop
        #DIV CLASS: f-fix
            #H3 CLASS: product-name
            #DIV CLASS: price-box
                #DIV CLASS: price-box
                #P CLASS: old-price
                    #SPAN CLASS: price
                #P CLASS: special-price 
                    #SPAN CLASS: price
""" 
mydriver = webdriver.Firefox()
mydriver.get(baseurl)
mydriver.maximize_window()
counter = []

def Obtain_Data(products_item):
    
    for x in products_item:
        counter.append(x)
        print('\n%s' % str(len(counter)))
        try:
            sku = x.find_element_by_xpath(xpaths['_sku_and_name'])
            print('NOMBRE: %s'  % sku.get_attribute("gtm-name"))
            print('SKU: %s'  % sku.get_attribute("gtm-sku"))
        except Exception as Error_en_sku_and_name:
            print('Error _sku_and_name, %s' % Error_en_sku_and_name)
        try:
            imagen = x.find_element_by_xpath(xpaths['_url_imagen'])
            print('IMAGEN: %s'  % imagen.get_attribute("src")) 
        except Exception as Error_en_url_imagen:
            print('Error _url_imagen, %s' % Error_en_url_imagen)
        try:
            normal_price = x.find_element_by_xpath(xpaths['_normal_price'])
            print('PRECIO NORMAL: %s'  % normal_price.text) 
        except Exception as Error_en_normal_price:
            print('PRECIO NORMAL: EL PRODUCTO ESTA EN PROMOCION')
        try:
            old_price = x.find_element_by_xpath(xpaths['_old_price'])
            print('PRECIO LISTA (Por Promocion): %s'  % old_price.text) 
        except Exception as Error_en_old_price:
            print('PRECIO LISTA (Por Promocion): EL PRODUCTO NO ESTA EN PROMOCION ACTUALMENTE')
        try:
            new_price = x.find_element_by_xpath(xpaths['_new_price'])
            print('PRECIO OFERTA: %s'  % new_price.text)
        except Exception as Error_en_new_price:
            print('PRECIO OFERTA: EL PRODUCTO NO ESTA EN PROMOCION ACTUALMENTE')
        try:
            price_to_cart = x.find_element_by_xpath(xpaths['_price_add_to_cart'])
            print('PRECIO CARRITO: %s'  % price_to_cart.get_attribute("data-pprice"))
        except Exception as Error_en_price_add_to_cart:
            print('Error _price_add_to_cart, %s' % Error_en_price_add_to_cart)

def Get_First_Item(mydriver):
    Obtain_Data(mydriver.find_elements_by_xpath(xpaths['_item_first']))


def Get_Item(mydriver):
    Obtain_Data(mydriver.find_elements_by_xpath(xpaths['_item']))

def Get_Item_Last(mydriver):
    Obtain_Data(mydriver.find_elements_by_xpath(xpaths['_item_last']))

def Main(mydriver):  
    time.sleep(10)     #MORE COOL: try:#products_item_first = WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['_item_first'])))#finally:#mydriver.quit()
    mydriver.find_element_by_xpath(xpaths['_items_in_page']).click()
    time.sleep(5)#MORE COOL: try:#products_item_first = WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['_item_first'])))#finally:#mydriver.quit()
    try:
        while mydriver.find_element_by_xpath(xpaths['_paging']):            
            time.sleep(5)#MORE COOL: try:#products_item_first = WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['_item_first'])))#finally:#mydriver.quit()
            Get_First_Item(mydriver)
            Get_Item(mydriver)
            Get_Item_Last(mydriver)
            mydriver.find_element_by_xpath(xpaths['_paging']).click() # NEXT PAGE >>
        endWhile

        time.sleep(5)#MORE COOL: try:#products_item_first = WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['_item_first'])))#finally:#mydriver.quit()
        Get_First_Item(mydriver)
        Get_Item(mydriver)
        Get_Item_Last(mydriver)
        print('\nLast Page. Scraping Finished') 
        mydriver.close()
    except Exception as NotPaging:        
        print('\nLast Page.  Scraping Finished')
        mydriver.close()

Main(mydriver)
print('\n\nFin :)')