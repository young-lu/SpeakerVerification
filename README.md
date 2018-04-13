# SpeakerVerification
Spring 2018 Research Assistant 

MSA_Verif_API.py is a python wrapper file I wrote to easily use Microsoft's speaker verification API

place the file in the Cognitive-SpeakerRecognition-Python/Verification folder after cloning the githuhb repo

___

create any number of voice profiles with an API key:
```Python
python MSA_Verif_API.py -cp [number_of_speakers] -k [subscription_key]
```
enroll many voices recursively with a directory of speech samples, seperated by subdirectories:
```Python
python MSA_Verif_API.py -ep -r [VoiceDirectory] -k [subscription_key] -f [ID_List.txt]
```
perform verification of one or many speakers on a list of voice profiles:
```Python
python MSA_Verif_API.py -v -r [VoiceDirectory] -k [subscription_key] -f [ID_List.txt]
```
