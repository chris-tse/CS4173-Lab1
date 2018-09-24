# CS 4173 Lab 1
Christopher Tse

## Task 1: Frequency Analysis Against Monoalphabetic Substitution Cipher

### Single Character Frequency Analysis

In order to find the encryption key and plaintext, we can make use of some properties of substitution ciphers which make it weak to attacks. The most helpful one would be frequency analysis. Initially, we can attempt a simple substitution of the alphabet after a single letter frequency analysis according to the relative frequencies:

```bash
$ tr 'nyvxuqmhtipaczlbgredfskjow' 'etaoinsrhdlucmfywgpbvkxqjz' < ciphertext.txt > plain.txt
```

### Bigram Frequency Analysis

This does not prove to be very helpful, although we do find several instances of the word 'the' after this substitution. This leads us to a bigram frequency analysis and substitution. The two most common bigrams are 'TH' and 'HE' which combined make up the word 'THE', and we know this is correct. Replacing these gives us a good starting point to begin building the key:

```bash
$ tr 'ytnhmu' 'THERIN' < ciphertext.txt  > plain.txt
```

### Incremental Substitution
Now we can make use of the word list provided to make incremental additions to the substitution key. Using the `worddiff.py` script, we can search for any words in the text that now only have `n` number of unsubstituted letters to compare with the word list:

```bash
./worddiff.py 1 < plain.txt

TzRN, xN, RIrHT, THIq, TRIe, v, vT, ITq, HIq, vT, ENp, v, v, lHETHER, ...
```

Using the `compareword.py` script, we can choose a word from the result of the `worddiff.py` script and convert it to a regex pattern to find any words in the word list that may match. For example:

```bash
$ ./compareword.py lHETHER < words.txt

whether
```

Since there is only one match in this case, it is highly likely that 'l' is the substitution of 'W'. We can now improve our key:

```bash
$ tr 'ytnhmul' 'THERINW' < ciphertext.txt  > plain.txt
```

We can repeat this. For example, using the another one of the outputs 'gETWEEN':

```bash
$ ./compareword.py gETWEEN < words.txt

between
```

Therefore, we can replace 'g' with 'B' and repeat again:

```bash
$ tr 'ytnhmulg' 'THERINWB' < ciphertext.txt  > plain.txt
```

Continuing on with this method, we can quickly decode more and more words until the full key and original plaintext has been recovered. The number passed into `worddiff.py can be changed to find words with more unsubstituted letters`. The final key is `'ytnhmulgidqvrxpeajzcbfsko'` to be replaced with `'THERINWBLYSAGODPCQUMFVKXJ'`. The decoded plaintext can be found in the included `decoded.txt`.

## Task 2: Encryption using Different Ciphers and Modes

In this task, we try encryption with several different ciphers. We have a plaintext contained in the file `plain.txt` which we will encrypt. First, let us examine the results of using AES-128 using CBC vs ECB:

```
$ openssl enc -aes-128-ecb -e \
    -in plain.txt -out aes-ecb.bin \
    -K 00112233445566778889aabbccddeeff \
    -iv 0102030405060708
    
$ openssl enc -aes-128-cbc -e \
    -in plain.txt -out aes-cbc.bin \
    -K 00112233445566778889aabbccddeeff \
    -iv 0102030405060708
```
By using a tool such as `hexdump` or `xxd` we can view the resulting binary contents of the file:

```
$ xxd -b plain.txt
00000000: 01010100 01101000 01100101 00100000 01110001 01110101  The qu
00000006: 01101001 01100011 01101011 00100000 01100010 01110010  ick br
0000000c: 01101111 01110111 01101110 00100000 01100110 01101111  own fo
00000012: 01111000 00100000 01101010 01110101 01101101 01110000  x jump
00000018: 01110011 00100000 01101111 01110110 01100101 01110010  s over
0000001e: 00100000 01110100 01101000 01100101 00100000 01101100   the l
00000024: 01100001 01111010 01111001 00100000 01100100 01101111  azy do
0000002a: 01100111                                               g

$ xxd -b aes-ecb.bin
00000000: 00001010 11110100 11010101 00010010 11101101 10110011  ......
00000006: 10001011 10110000 10000010 00011101 00111001 11000110  ....9.
0000000c: 10010111 11111101 10100001 10101110 11101110 10111111  ......
00000012: 10110100 01011110 01111011 00011100 00011101 01100001  .^{..a
00000018: 01100001 00111101 10110100 01111010 10001100 01101100  a=.z.l
0000001e: 10010110 11001000 01011110 11000100 00000000 01010110  ..^..V
00000024: 11010100 11001110 10011001 00111001 01010010 00011001  ...9R.
0000002a: 01010110 11101111 00100011 11001001 01011101 01010110  V.#.]V

$ xxd -b aes-cbc.bin
00000000: 11111101 10001110 00010000 01101100 11010111 10001011  ...l..
00000006: 10010010 10001001 00101100 00111000 00000010 11001110  ..,8..
0000000c: 11000000 10011110 01010010 11111101 00101011 10110110  ..R.+.
00000012: 11110011 11001100 10010100 10001110 01010000 01111111  ....P.
00000018: 11100100 10110110 00011110 01101101 10111101 01000011  ...m.C
0000001e: 10100101 11100001 10101001 00011111 10100100 11000101  ......
00000024: 01011010 00001101 11010111 11110111 11010001 10001101  Z.....
0000002a: 00000010 10101110 00111100 10011111 01101101 01001110  ..<.mN
```

We can observe how with the plaintext, although it is not a full 48 bytes, the resulting output is due to AES being a block cipher which will provide padding for the plaintext. We can also see that different modes result in different ciphertexts. We can see similar results with the outputs of the AES-256 encryption as well as the DES encryption in CBC and ECB modes.

There is also a provided `plain2.txt` which has a slight change in the plaintext. This demonstrates the avalanche effect of these ciphers as well, since a small change in the plaintext results in completely different ciphertexts.

## Task 3: Encryption Mode – ECB vs. CBC

