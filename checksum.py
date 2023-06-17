#draw 23 words from BIP39 wordlist (english.txt)
seed_phrase = "unusual survey coin divide biology album harbor fee profit nest claw mammal shaft basic diesel crater scatter modify bottom excuse hawk undo negative ?"

#convert seed phrase into a list to be able to interface with each word individually.
seed_phrase = seed_phrase.split(" ")

#open the "english.txt" file and stores it into variable "english"
english = open("english.txt")

#read the "english.txt" file stored in variable "english" and stores the words in the variable "word_list". Also, changes the variable type to a list.
word_list = english.read().split("\n")

#close the "english.txt" file stored in variable "english" since we don't need it anymore.
english.close()

#convert seed_phrase (with words) to indexed number in BIP39 wordlist
seed_phrase_index = [word_list.index(word) if word != "?" else word for word in seed_phrase]

#convert seed_phrase_index (with numbers) to binary
seed_phrase_binary = [format(number, "011b") if number != "?" else number for number in seed_phrase_index]

#calculate the number of bits missing for entropy
num_missing_bits = int(11-(1/3)*(len(seed_phrase)))

#calculate all the possible permutation of missing bits for entropy
missing_bits_possible = [bin(x)[2:].rjust(num_missing_bits, "0") for x in range(2**num_missing_bits)]

#combine the binary representation of seed phrase with each possible missing bits to result in the possible entropy
entropy_possible = ["".join(seed_phrase_binary[:-1])+bits for bits in missing_bits_possible]

#input each entropy_possible in the SHA256 function to result in the corresponding checksum
import hashlib

checksum = [format(hashlib.sha256(int(entropy, 2).to_bytes(len(entropy) // 8, byteorder="big")).digest()[0],"08b")[:11-num_missing_bits] for entropy in entropy_possible]

#combine the missing bits with its corresponding checksum
last_word_bits = [i + j for i, j in zip(missing_bits_possible, checksum)]

#transform 11 bit number to indexed number and then the corresponding word in the BIP39 wordlist
last_word = [word_list[int(bits, 2)] for bits in last_word_bits]

print(last_word)
