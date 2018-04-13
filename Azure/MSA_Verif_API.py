# MSA_Verif_API.py
#
# Connor Lu
# 
# 
# This wrapper file is used in combination with MS Azure Congitive Services Speaker Verification API
# Place this file in the same directory as the API files 
# Cognitive-SpeakerRecognition-Python/Verification
import VerificationServiceHttpClientHelper
import VerificationProfile
import VerificationResponse
from VerifyFile import *
import http.client, urllib.request, urllib.parse, urllib.error, base64, ssl
import EnrollmentResponse
from EnrollProfile import *
import ProfileCreationResponse
from CreateProfile import *
from GetProfile import *
from PrintAllProfiles import *
from ResetEnrollments import *
from DeleteProfile import * 

import os
import sys
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("--create_profile","-cp", help="-cp [number_of_speakers] -k [subscription_key]", dest="create")
parser.add_argument("--enroll_profile","-ep", help="-ep -r [Directory] -k [key] -f [ID_List.txt]", action="store_true", dest="enroll")
parser.add_argument("--list_profiles","-lp", help="-lp -k [key] (-f [file.txt])", action="store_true",dest="list")
parser.add_argument("--verify","-v", help="-v -k [subscription-key] -p [profile] -f [.wav])", action="store_true",dest="verify")
parser.add_argument("--delete_profile", "-dp", help="delete voice profile(s)",action="store_true",dest="delete")
parser.add_argument("--recursive","-r", help="recursive profile creation/enrollment",dest="recursive")
parser.add_argument("--key", "-k", help="subscription key",dest="key",type=str)
parser.add_argument("--profile", "-p", help="profile ID",type=str,dest="profile")
parser.add_argument("--filename", "-fn", help="file or directory to be used",type=str,dest="filename")
parser.add_argument("--test","-t",action="store_true",dest="test")
args = parser.parse_args()


if __name__ == "__main__":
    """create profiles from number of speakers argument and the subscription key"""
    if (args.create) :
        n = int(args.create)
        for i in range(n) :
            create_profile(args.key, 'en-us')

        """ enroll profiles using the key, ID_List.txt, and directory of .wav files """
    elif (args.enroll) :
        if (args.recursive):
            try :
                SpeakDir = args.recursive
                key = args.key
                f = args.filename
                idlist = [] 
                for line in open(f) :
                    idlist.append(line)
                i = 0
                for speaker in os.listdir(SpeakDir) :
                    # print(idlist[i])
                    pid = idlist[i]
                    pid = pid.rstrip()
                    for wave in os.listdir("{0}/{1}".format(SpeakDir,speaker)) :
                        path = "{0}/{1}/{2}".format(SpeakDir,speaker,wave)
                        print('enroll_profile({0},{1},{2}'.format(key,pid,path))
                        enroll_profile(key,pid,path)
                    i+=1
                    print('\n\n\n')
            except :
                print("ERROR: python MSA_Verif_API.py -ep -r [Directory] -k [key] -f [ID_List.txt]")
        else : 
            wave = args.filename
            key = args.key
            pid = args.profile
            ep = "{0},{1},{2}".format(key,pid,wave)
            enroll_profile(key,pid,wave)




        """ list all profiles enrolled for the given subscription  and save them to a .txt file"""
    elif (args.list) :
        try :
            helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
                    args.key)
            profiles = helper.get_all_profiles()
            if (args.filename) :
                f = open(args.filename,"w")
                for profile in profiles:
                    f.write("{0}\n".format(profile.get_profile_id()))
            print_all_profiles(args.key)
        except :
            print("ERROR: python MSA_Verif_API.py --list_profiles --key subscription key --filename [ID_List.txt]")


        """  """
    elif (args.verify) :
        if (args.recursive) :
            try :
                VoiceDir = args.recursive
                key = args.key 
                profiles = []
                voice_folders = []
                for line in open(args.filename):
                    l = line.rstrip()
                    profiles.append(l)
                print(profiles)
                for folder in os.listdir(VoiceDir) :
                    voice_folders.append("{0}/{1}".format(VoiceDir,folder))
                print(voice_folders)
                i=0
                for pro in profiles:

                    for wav in voice_folders:
                        print('verify_file({0},{1},{2})'.format(key,wav,pro))
                        verify_file(key,wav,pro)
                        print('\n')
                        i+=1
                    
            except :
                print("ERROR: python MSA_Verif_API.py --verify -r [VoiceDir] --key [key] -f [ID_List.txt]")
        else :
            try : 
                voice = args.filename
                key = args.key
                profile = args.profile
                verify_file(key,voice,profile)
            except :
                print("ERROR: python MSA_Verif_API.py --verify --key [key] --profile [pid] -f [voice]\n")


        """ """
    elif (args.delete) :
        if (args.filename) :
            for line in open(args.filename) :
                delete_profile(args.key, line)
        elif (args.profile) :
            delete_profile(args.key, args.profile)

    elif (args.test) :
        print('test mode.')
        f = args.filename
        folders = []
        printme = []
        for folder in os.listdir(f) :
            folders.append("{0}/{1}".format(f,folder))

        i=1
        for fold in folders:
            for o in os.listdir(fold):
                print("{2} --> {0}/{1}".format(fold,o,i))
            i+=1
            print('\n')