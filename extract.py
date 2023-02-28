from PIL import Image
import math
stegano_image = Image.open('./PVD/embedded_img.bmp','r') #open image 

pixel_value_stegano_image = list(stegano_image.getdata())

def calculate_di(pixels_value):
    list_of_di=[]
    for i in range(0,len(pixels_value),2):
        list_of_di+=[pixels_value[i+1]-pixels_value[i]]
    return list_of_di

def abs_di(pixels_value):
    abs_list_of_di = []
    for i in range(0,len(pixels_value),2):  #Compute by pairs of pixel (step=2)
        abs_list_of_di+=[abs(pixels_value[i]-pixels_value[i+1])]
    return abs_list_of_di 

def find_domain_in_quantity_table(abs_list_of_di):
    lower_upper_bound=[]
    for i in abs_list_of_di :

        # if 0<=i<=7 :

        #     lower_upper_bound+=[[0,7]]

        # elif 8<=i<=15 :
        
        #     lower_upper_bound+=[[8,15]]

        # elif 16<=i<=31 :
             
        #     lower_upper_bound+=[[16,31]]
            
        # elif 32 <= i <=63 :
           
        #     lower_upper_bound+=[[32,63]]
        # elif  64 <= i <=127 :
            
        #     lower_upper_bound+=[[64,127]]
        # elif 128 <= i <=255 :
              
        #      lower_upper_bound+=[[128,255]]
        if 0<=i<=7 :
            n = int(math.log2(7-0+1))   # number of embeddable data bits
            lower_upper_bound+=[[0,7,n]]
        elif 8<=i<=15 :
            n = int(math.log2(15-8+1))
            lower_upper_bound+=[[8,15,n]]
        elif 16<=i<=31 :
            n = int(math.log2(31-16+1))
            lower_upper_bound+=[[16,31,n]]
        elif 32 <= i <=63 :
            n = int(math.log2(63-32+1))
            lower_upper_bound+=[[32,63,n]]
        elif  64 <= i <=127 :
            n = int(math.log2(7-0+1))
            lower_upper_bound+=[[64,127,n]]
        elif 128 <= i <=255 :
            n = int(math.log2(7-0+1))
            lower_upper_bound+=[[128,255,n]]
    return lower_upper_bound

def check_falling_off_bound(pixels_value,list_of_di,lower_upper_bound):
    embeddable_pixels=[]
    j=0
    for i in range(len(list_of_di)):
        m = lower_upper_bound[i][1] - list_of_di[i]
        if list_of_di[i] % 2 != 0 : 
            pixel_1 = pixels_value[j] - math.ceil(m/2)
            pixel_2 = pixels_value[j+1] + math.floor(m/2)
            if (pixel_1 < 0 or pixel_1 > 255) or (pixel_2 < 0 or pixel_2 > 255):
                continue
            else:
                embeddable_pixels += [[lower_upper_bound[i],list_of_di[i]]]
            j+=2
        else :
            pixel_1 = pixels_value[j] - math.floor(m/2)
            pixel_2 = pixels_value[j+1] + math.ceil(m/2)
            if (pixel_1 < 0 or pixel_1 > 255) or (pixel_2 < 0 or pixel_2 > 255):
                continue
            else:
                embeddable_pixels += [[lower_upper_bound[i],list_of_di[i]]]
            j+=2
    return embeddable_pixels

def calculate(embeddable_pixels):
    b=[]
    for i in range(len(embeddable_pixels)):
        if embeddable_pixels[i][1] >= 0:
            b+=[embeddable_pixels[i][1]-embeddable_pixels[i][0][0]]
        else:
            b+=[-embeddable_pixels[i][1]-embeddable_pixels[i][0][0]]
        # ,embeddable_pixels[i][0][2]]
    return b

def n_bits_convert (embeddable_pixels):
    n_bits=[]
    for i in embeddable_pixels:
        n_bits.append(i[0][2])
    
    return n_bits

def decimal_to_binary(b, n_bits):
    binary_list = []
    for i in range(len(b)):
        binary = bin(abs(b[i]))[2:]
        binary = '0'*(n_bits[i]-len(binary)) + binary
        binary_list.append(binary)
    return binary_list

def list_to_string(bin_lst):
    string = ''.join(str(e) for e in bin_lst)  # join list elements into a string
    string = string.replace(' ', '')  # remove any existing spaces
    string = ' '.join(string[i:i+8] for i in range(0, len(string), 8))  # add a space after every 8 characters
    return string

def convert_binary_to_ascii(one_line_binary_string):
    binary_list = one_line_binary_string.split()
    ascii_list = []
    for binary in binary_list:
        decimal = int(binary, 2)
        ascii_char = chr(decimal)
        ascii_list.append(ascii_char)
    return ''.join(ascii_list)

    
di=calculate_di(pixel_value_stegano_image)
# print(di[:30])

abs_list_of_di = abs_di(pixel_value_stegano_image)
print('*****************************************************')
#print(pixel_value_stegano_image[-2])
lower_upper_bound=find_domain_in_quantity_table(abs_list_of_di)
# print(lower_upper_bound[:30])

embeddable_pixels = check_falling_off_bound(pixel_value_stegano_image,di,lower_upper_bound)
# print(embeddable_pixels[:30])

b=calculate(embeddable_pixels)
print(b[:30])
n_bits = n_bits_convert(embeddable_pixels)
# print(n_bits[:30])
secret_bin = decimal_to_binary(b,n_bits)
# print(dec_to_ascii(b)[:50])
print(secret_bin[:30])
print('*****************************************************')


binary_string = list_to_string(secret_bin)
print(binary_string[:30])

message = convert_binary_to_ascii(binary_string)
print(message[:50])

