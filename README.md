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

These modes are partially compromised :
- CFB
- CBC


requirement : 
- python 3.X
- TensorFlow
- Keras
- Numpy

**TensorFlow 2.8** has a leaking memory bug, **2.7 version** works fine.

Datasets can be created with **gendataset-XX.py** scripts. I suggest to use 50k of samples for train data and 10k of samples for test data.
Number of sample and size of sample can be adjusted in scripts.

To generate train data :
```
python3 gendataset-XX.py > xx-50k.dat
```

To generate test data :
```
python3 gendataset-XX.py > xx-10k-test.dat
```

To train a model until every bits of predicted data all match with output test data bits :
```
python3 keras-xx.py
```
