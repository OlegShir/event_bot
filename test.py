



def biglion_find_new_post(post, last_post):
    # преобразование входных номеров постов в строку для их дальнейшего разделения: 4173332 -> 417  3332
    post_string = str(post)
    last_post_string = str(last_post)
    # получаем длину номера поста, если в будущем увеличется разряд
    post_length = len(post_string) 
    last_post_length = len(last_post_string)
    if (int(post_string[0:post_length-4]) >= int(last_post_string[0:last_post_length-4])) & \
        (int(post_string[post_length-4:post_length+1]) < int(last_post_string[last_post_length-4:last_post_length+1])):
        print('Yes')
    else: 
        print('No')



a=4174564
b=4173333

biglion_find_new_post(a,b)
def main():
    pass



if __name__ == '__main__':
    main()