#input seed phrase separated by spaces (12, 15, 18, 21, or 24 also possible); i.e., "unusual survey coin divide biology album harbor fee profit nest claw mammal shaft basic diesel crater scatter modify bottom excuse hawk undo negative ?"
seed_phrase = input("Please input your seed in words (separate by spaces) and leave ? as the last word: ").lower()

seed_phrase = seed_phrase.split(" ")

english = open("english.txt")

word_list = english.read().split("\n")

english.close()

seed_phrase_index = [word_list.index(word) if word != "?" else word for word in seed_phrase]

seed_phrase_binary = [format(number, "011b") if number != "?" else number for number in seed_phrase_index]

num_missing_bits = int(11-(1/3)*(len(seed_phrase)))

missing_bits_possible = [bin(x)[2:].rjust(num_missing_bits, "0") for x in range(2**num_missing_bits)]

entropy_possible = ["".join(seed_phrase_binary[:-1])+bits for bits in missing_bits_possible]

#refer to SHA256 library for entropy checksum
import hashlib

checksum = [format(hashlib.sha256(int(entropy, 2).to_bytes(len(entropy) // 8, byteorder="big")).digest()[0],"08b")[:11-num_missing_bits] for entropy in entropy_possible]

last_word_bits = [i + j for i, j in zip(missing_bits_possible, checksum)]

#output as word options according to BIP39 wordlist
last_word = [word_list[int(bits, 2)] for bits in last_word_bits]

print(last_word)
