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

Continuing on with this method, we can quickly decode more and more words until the full key and original plaintext has been recovered. The final key is `'ytnhmulgidqvrxpeajzcbfsko'` to be replaced with `'THERINWBLYSAGODPCQUMFVKXJ'`. The decoded plaintext can be found in the included `decoded.txt`