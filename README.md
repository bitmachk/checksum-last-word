## checksum
**Calculate the possible last word**

The user is prompted to input your seed in words separated by spaces, with a question mark "?" as the last word. The input is converted to lowercase and stored in the variable `seed_phrase`.
```
seed_phrase = input("Please input your seed in words (separate by spaces) and leave ? as the last word: ").lower()
```

The `seed_phrase` is split into individual words using the space separator and stored in a list.
```
seed_phrase = seed_phrase.split(" ")
```

The file "english.txt" (obtain this BIP39 wordlist from [here](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt)) is opened in read mode, and its contents are read and stored in the variable `word_list`. Each line in the file represents a word.
```
english = open("english.txt")
word_list = english.read().split("\n")
english.close()
```

The index of each word in `seed_phrase` is determined by checking its position in the `word_list`. If the word is "?" (the last word), it is assigned the value of "?". The resulting indices are stored in the `seed_phrase_index` list.
```
seed_phrase_index = [word_list.index(word) if word != "?" else word for word in seed_phrase]
```

Each index in `seed_phrase_index` is converted to its binary representation with 11 bits, padded with leading zeros if necessary. If the index is "?", it is assigned the value of "?". The resulting binary representations are stored in the `seed_phrase_binary` list.
```
seed_phrase_binary = [format(number, "011b") if number != "?" else number for number in seed_phrase_index]
```

The number of missing bits is calculated by subtracting the fractional part of `11 - (1/3) * len(seed_phrase)` from 11. This determines the number of bits needed to complete a valid binary representation. The calculation uses 1/3 of the length of `seed_phrase` because each word contributes 11 bits, but the last word "?" contributes fewer bits.
```
num_missing_bits = int(11 - (1/3) * len(seed_phrase)))
```

All possible combinations of missing bits, represented as binary strings, are generated using the range from 0 to 2^num_missing_bits. Each binary string is padded with leading zeros to match the number of missing bits and stored in the `missing_bits_possible` list.
```
missing_bits_possible = [bin(x)[2:].rjust(num_missing_bits, "0") for x in range(2**num_missing_bits)]
```

For each binary string in `missing_bits_possible`, the missing bits are appended to the previously obtained binary representation of `seed_phrase` (excluding the last word). This creates all possible entropy combinations with missing bits, which are stored in the `entropy_possible` list.
```
entropy_possible = ["".join(seed_phrase_binary[:-1]) + bits for bits in missing_bits_possible]
```

The `hashlib` module is imported, and for each entropy combination in `entropy_possible`, a checksum is computed. The entropy is converted to bytes, and its SHA-256 hash is computed. The first byte of the hash is converted to an 8-bit binary string and truncated to remove the excess bits based on the number of missing bits. The resulting checksums are stored in the `checksum` list.
```
import hashlib
checksum = [format(hashlib.sha256(int(entropy, 2).to_bytes(len(entropy) // 8, byteorder="big")).digest()[0], "08b")[:11 - num_missing_bits] for entropy in entropy_possible]
```

The missing bits and checksum bits are concatenated for each entropy combination to form the final bits representing the last word. These bits are used as indices in `word_list`, and the corresponding words are extracted. The resulting words are stored in the `last_word` list.
```
last_word_bits = [i + j for i, j in zip(missing_bits_possible, checksum)]
last_word = [word_list[int(bits, 2)] for bits in last_word_bits]
```

Finally, the `last_word` list, containing the possible last words based on the input seed phrase, is printed.
```
print(last_word)
```
