def calculate_probabilities(file_path, sample_size):
    try:
        with open(file_path, "r") as f:
            sample = f.read(sample_size).lower()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except IOError:
        print(f"Error: An error occurred while reading the file {file_path}.")
        return {}

    characters = "abcdefghijklmnopqrstuvwxyz \n"
    for i in sample:
        if i not in characters:
            characters+=i
    dict = {char: round(sample.count(char)/sample_size,3) for char in characters}
    probabilities=[]
    for i in characters:
        probabilities.append([i,dict[i],""])
    probabilities.sort(key=lambda x:x[1],reverse=True)
    return probabilities

def encoding(file_path, sample_size):
    message_bit = calculate_probabilities(file_path, sample_size)
    n=len(message_bit)
    d={}
    L=[]
    while True:
        if n==2:
            message_bit[0][2]+="1"
            message_bit[1][2]+="0"
            for i in message_bit:
                d[i[0]]=i[2]
            message_bit[0].pop(1)
            message_bit[1].pop(1)
            break
        else:
            message_bit[n-1][2]+="0"
            message_bit[n-2][2]+="1"
            message_bit[n-1]+=[message_bit[n-2][0],len(message_bit[n-2][2])]
            message_bit[n-2][1]+=message_bit[n-1][1]
            L.append(message_bit.pop())
            n=n-1
            message_bit.sort(key=lambda x:x[1],reverse=True)

    n=len(L)
    i=2
    while n>=1:
        message_bit.append([L[-1][0],L[-1][2]+d[L[-1][3]][L[-1][4]:]])
        d[message_bit[i][0]]=message_bit[i][1]
        i+=1
        n=n-1
        L.pop()
    for i in d:
        d[i]=d[i][::-1]
    return d

def encoded_text(file_path,d):
    try:
        with open(file_path, "r") as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except IOError:
        print(f"Error: An error occurred while reading the file {file_path}.")
        return

    try:
        with open("Encoded_text", "w") as f:
            for char in text:
                f.write(d[char])
    except IOError:
        print("Error: An error occurred while writing the encoded text.")

def decoding_text(d):
    d1={}
    for i in d:
        d1[d[i]]=i
    try:
        with open("Encoded_text", "r") as f:
            msg_code = f.read()
    except FileNotFoundError:
        print("Error: The file Encoded_text was not found.")
        return
    except IOError:
        print("Error: An error occurred while reading the encoded text.")
        return
    
    try:
        with open("Decoded_text", "w") as f:
            temp=''
            for i in msg_code:
                temp+=i
                if temp in d1:
                    f.write(d1[temp])
                    temp='' 
    except IOError:
        print("Error: An error occurred while writing the decoded text.")
        
file_path = "Text"
sample_size = 300
d=encoding(file_path, sample_size)
if d:
    encoded_text(file_path,d)
    decoding_text(d)