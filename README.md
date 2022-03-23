# aes-killer
AES encryption killer with machine learning

No **AES** encryption has not been compromised ! if used correctly, using **AES** is safe in 2022.

I noticed some encryption program don't add padding during encryption. 

**What's is padding ?**
- Padding is a block of random data added at the head of a file.  https://en.wikipedia.org/wiki/Padding_(cryptography)


Without padding, some block cipher mode of operation are vulnerable. It's possible to find plain data with machine learning.


These modes are completly compromised without padding :
- CTR
- GCM
