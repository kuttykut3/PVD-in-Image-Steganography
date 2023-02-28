from PIL import Image
import math

cover_image = Image.open('./PVD/baboon512.bmp','r') #open image

pixel_value_cover_image = list(cover_image.getdata()) #we have pixels in this list

#print(pix_val_secret[0:30])
def pixel_value(list_of_values): #RGB(R,G,B) in gray scale = RGB(X,X,X) so one of them is enough
    pixel_val=[]
    for i in list_of_values:
        pixel_val+=[i[0]]
    return pixel_val #From RGB(X,X,X) -> Grey value X

def calculate_di(pixels_value):
    list_of_di=[]
    for i in range(0,len(pixels_value),2):  #Compute by pairs of pixel (step=2)
        list_of_di+=[pixels_value[i+1]-pixels_value[i]]
    return list_of_di

def abs_di(pixels_value):
    abs_list_of_di = []
    for i in range(0,len(pixels_value),2):  #Compute by pairs of pixel (step=2)
        abs_list_of_di+=[abs(pixels_value[i]-pixels_value[i+1])]
    return abs_list_of_di 

def find_domain_in_quantity_table(abs_list_of_di):
    lower_uper_bound=[]
    for i in abs_list_of_di :
        if 0<=i<=7 :
            n = int(math.log2(7-0+1))   # number of embeddable data bits
            lower_uper_bound+=[[0,7,n]]
        elif 8<=i<=15 :
            n = int(math.log2(15-8+1))
            lower_uper_bound+=[[8,15,n]]
        elif 16<=i<=31 :
            n = int(math.log2(31-16+1))
            lower_uper_bound+=[[16,31,n]]
        elif 32 <= i <=63 :
            n = int(math.log2(63-32+1))
            lower_uper_bound+=[[32,63,n]]
        elif  64 <= i <=127 :
            n = int(math.log2(7-0+1))
            lower_uper_bound+=[[64,127,n]]
        elif 128 <= i <=255 :
            n = int(math.log2(7-0+1))
            lower_uper_bound+=[[128,255,n]]
    return lower_uper_bound

def list_of_bin_secret_data(file): #all the scret data in the one string (dua het ve 1 hang)
        with open("./PVD/secret.txt", "r") as ins:
            array = []
            for line in ins:
                array.append(line.replace('\n',' '))     
        secret_line = ''.join(map(str,array))
        binary_secret_string = ''.join(format(ord(char), '08b') for char in secret_line)
        return binary_secret_string    

def split_secret_data_with_n_bit(string_of_secret_data,lowerbound_and_n_slice):
    list_of_sliced_secret_data=[]
    for i in lowerbound_and_n_slice:
            if string_of_secret_data=='' :
                return list_of_sliced_secret_data
    
            temp= i[2] #n bits embeddable

            list_of_sliced_secret_data +=[string_of_secret_data[0:temp]]
            
            string_of_secret_data = string_of_secret_data[temp:]

    return list_of_sliced_secret_data
            
        
def convert_secret_data_to_decimal(secret_data_n_slice_n_slice):
    decimal_secret_data_n_slices=[]
    for i in secret_data_n_slice_n_slice :
        z=int(i,2)
        decimal_secret_data_n_slices += [z]
    return decimal_secret_data_n_slices

def calculate_new_di(find_domain_in_quantity_table_and_lowerbound, convert_secret_data_decimal, dif_2pixels):
    new_di = []
    for i in range(len(convert_secret_data_decimal)):
            if dif_2pixels[i] >= 0 :
                new_di+=[find_domain_in_quantity_table_and_lowerbound[i][0]+convert_secret_data_decimal[i]]
            else:
                new_di+=[-(find_domain_in_quantity_table_and_lowerbound[i][0]+convert_secret_data_decimal[i])]
    return new_di          

def cal_new_val_of_pixels(pixel_value,new_di,dif_2pixels):
    new_pixels=[]
    j=0
    for i in range(len(new_di)):        #change new value embedded data
        m = new_di[i] - dif_2pixels[i]

        if dif_2pixels[i] % 2 != 0 : 
            new_pixel_1 = pixel_value[j] - math.ceil(m/2)
            new_pixel_2 = pixel_value[j+1] + math.floor(m/2)
            if (new_pixel_1 < 0 or new_pixel_1 > 255) or (new_pixel_2 < 0 or new_pixel_2 > 255):
                new_pixels += [pixel_value[j], pixel_value[j+1]]
            else:
                new_pixels += [new_pixel_1, new_pixel_2]
            j+=2
        else :
            new_pixel_1 = pixel_value[j] - math.floor(m/2)
            new_pixel_2 = pixel_value[j+1] + math.ceil(m/2)
            if (new_pixel_1 < 0 or new_pixel_1 > 255) or (new_pixel_2 < 0 or new_pixel_2 > 255):
                new_pixels += [pixel_value[j], pixel_value[j+1]]
            else:
                new_pixels += [new_pixel_1, new_pixel_2]
            j+=2

    for k in range(j,len(pixel_value),2):   #keep remain value without data embedded
        new_pixels+=[pixel_value[k],pixel_value[k+1]]

    return new_pixels

def show_new_picture(pixels):
    img = Image.new('L', (512, 512))    # L mode - grayscale
    img.putdata(pixels)
    img.save("./PVD/embedded_img.bmp")
    img.show()


pixel_values=pixel_value(pixel_value_cover_image)

print(pixel_values[:30]) 

dif_2pixels =calculate_di(pixel_values)
# print(dif_2pixels[:50]) 
abs_list_of_di = abs_di(pixel_values)

# print(abs_list_of_di[:50])

find_domain_in_quantity_table_and_lowerbound=find_domain_in_quantity_table(abs_list_of_di)

# print(find_domain_in_quantity_table_and_lowerbound[0:30]) 

string_of_secret_data = list_of_bin_secret_data('./PVD/secret.txt')
print(string_of_secret_data) 

secret_data_n_slice_n_slice = split_secret_data_with_n_bit(string_of_secret_data,find_domain_in_quantity_table_and_lowerbound)
# print(secret_data_n_slice_n_slice) OK

convert_secret_data_decimal=convert_secret_data_to_decimal(secret_data_n_slice_n_slice)
# print(convert_secret_data_decimal) OK

new_di=calculate_new_di(find_domain_in_quantity_table_and_lowerbound,convert_secret_data_decimal,dif_2pixels)
# print('*****************************************************')
print(new_di) 
pvd_pixels=cal_new_val_of_pixels(pixel_values,new_di,dif_2pixels)

print('*****************************************************')
print(pvd_pixels[:30])

show_new_picture(pvd_pixels)
