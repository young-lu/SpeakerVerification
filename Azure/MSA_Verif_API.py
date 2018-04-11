import VerificationServiceHttpClientHelper
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--create_profile","-cp", help="create profile(s) with your subscription key", action="store_true", dest="create")
parser.add_argument("--enroll_profile","-ep", help="enroll profile(s) with three audio files each fo the same phrase", action="store_true", dest="enroll")
parser.add_argument("--list_profiles","-lp", help="list profiles stored for a subscription key", action="store_true",dest="list")
# parser.add_argument("--save","-s",help="save profile IDs to .txt file", action="store_true",dest="save")
parser.add_argument("--verify","-v", help="accept or reject an audio file match to stored voice profile", action="store_true",dest="verify")
parser.add_argument("--delete_profile", "-dp", help="delete voice profile(s)",action="store_true",dest="delete")
parser.add_argument("--recursive","-r", help="recursive profile creation/enrollment",dest="recursive")
parser.add_argument("--key", "-k", help="subscription key",dest="key",type=str)
parser.add_argument("--profile", "-p", help="profile ID",type=str,dest="profile")
parser.add_argument("--filename", "-fn", help="file or directory to be used",type=str,dest="filename")
parser.add_argument("--test","-t",action="store_true",dest="test")
args = parser.parse_args()

def create_profile(subscription_key, locale):
    """Creates a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    locale -- the locale string
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    creation_response = helper.create_profile(locale)

    print('Profile ID = {0}'.format(creation_response.get_profile_id()))

def delete_profile(subscription_key, profile_id):
    """Delete the given profile from the server
        
    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to reset
    """
    
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(subscription_key)
    
    helper.delete_profile(profile_id)
    
    print('Profile {0} has been successfully deleted.'.format(profile_id))

class EnrollmentResponse:
    """This class encapsulates the enrollment response."""

    _ENROLLMENT_STATUS = 'enrollmentStatus'
    _ENROLLMENTS_COUNT = 'enrollmentsCount'
    _REMAINING_ENROLLMENTS = 'remainingEnrollments'
    _ENROLLMENT_PHRASE = 'phrase'

    def __init__(self, response):
        """Constructor of the EnrollmentResponse class.

        Arguments:
        response -- the dictionary of the deserialized python response
        """
        self._enrollment_status = response.get(self._ENROLLMENT_STATUS, None)
        self._enrollments_count = response.get(self._ENROLLMENTS_COUNT, None)
        self._remaining_enrollments = response.get(self._REMAINING_ENROLLMENTS, None)
        self._enrollment_phrase = response.get(self._ENROLLMENT_PHRASE, None)

    def get_enrollment_status(self):
        """Returns the enrollment status"""
        return self._enrollment_status

    def get_enrollments_count(self):
        """Returns the number of enrollments already performed"""
        return self._enrollments_count

    def get_enrollment_phrase(self):
        """Returns the enrollment phrase extracted from this request"""
        return self._enrollment_phrase

    def get_remaining_enrollments(self):
        """Returns the number of remaining enrollments before the profile is ready for verification"""
        return self._remaining_enrollments

def enroll_profile(subscription_key, profile_id, file_path):
    """Enrolls a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to enroll
    file_path -- the path of the file to use for enrollment
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    enrollment_response = helper.enroll_profile(profile_id, file_path)

    print('Enrollments Completed = {0}'.format(enrollment_response.get_enrollments_count()))
    print('Remaining Enrollments = {0}'.format(enrollment_response.get_remaining_enrollments()))
    print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))
    print('Enrollment Phrase = {0}'.format(enrollment_response.get_enrollment_phrase()))

def get_profile(subscription_key, profile_id):
    """Get a speaker's profile with given profile ID
    
    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to resets
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)
    
    profile = helper.get_profile(profile_id)
    
    print('Profile ID = {0}\nLocale = {1}\nEnrollments Completed = {2}\nRemaining Enrollments = {3}\nCreated = {4}\nLast Action = {5}\nEnrollment Status = {6}\n'.format(
        profile._profile_id,
        profile._locale,
        profile._enrollments_count,
        profile._remaining_enrollments_count,
        profile._created_date_time,
        profile._last_action_date_time,
        profile._enrollment_status))

def print_all_profiles(subscription_key):
    """Print all the profiles for the given subscription key.

    Arguments:
    subscription_key -- the subscription key string
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    profiles = helper.get_all_profiles()

    print('Profile ID, Locale, Enrollments Count, Remaining Enrollments Count,'
          ' Created Date Time, Last Action Date Time, Enrollment Status')
    for profile in profiles:
        print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(
            profile.get_profile_id(),
            profile.get_locale(),
            profile.get_enrollments_count(),
            profile.get_remaining_enrollments_count(),
            profile.get_created_date_time(),
            profile.get_last_action_date_time(),
            profile.get_enrollment_status()))


class ProfileCreationResponse:
    """This class encapsulates the response of the creation of a user profile."""

    _PROFILE_ID = 'verificationProfileId'

    def __init__(self, response):
        """Constructor of the ProfileCreationResponse class.

        Arguments:
        response -- the dictionary of the deserialized python response
        """
        self._profile_id = response.get(self._PROFILE_ID, None)

    def get_profile_id(self):
        """Returns the profile ID of the user"""
        return self._profile_id

def reset_enrollments(subscription_key, profile_id):
	"""Reset enrollments of a given profile from the server
	
    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to reset
	"""
	
	helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(subscription_key)
	
	helper.reset_enrollments(profile_id)
	
	print('Profile {0} has been successfully reset.'.format(profile_id))

class VerificationProfile:
    """This class encapsulates a user profile."""

    _PROFILE_ID = 'verificationProfileId'
    _LOCALE = 'locale'
    _ENROLLMENTS_COUNT = 'enrollmentsCount'
    _REMAINING_ENROLLMENTS_COUNT = 'remainingEnrollmentsCount'
    _CREATED_DATE_TIME = 'createdDateTime'
    _LAST_ACTION_DATE_TIME = 'lastActionDateTime'
    _ENROLLMENT_STATUS = 'enrollmentStatus'

    def __init__(self, response):
        """Constructor of the VerificationProfile class.

        Arguments:
        response -- the dictionary of the deserialized python response
        """
        self._profile_id = response.get(self._PROFILE_ID, None)
        self._locale = response.get(self._LOCALE, None)
        self._enrollments_count = response.get(self._ENROLLMENTS_COUNT, None)
        self._remaining_enrollments_count = response.get(self._REMAINING_ENROLLMENTS_COUNT, None)
        self._created_date_time = response.get(self._CREATED_DATE_TIME, None)
        self._last_action_date_time = response.get(self._LAST_ACTION_DATE_TIME, None)
        self._enrollment_status = response.get(self._ENROLLMENT_STATUS, None)

    def get_profile_id(self):
        """Returns the profile ID of the user"""
        return self._profile_id

    def get_locale(self):
        """Returns the locale of the user"""
        return self._locale

    def get_enrollments_count(self):
        """Returns the total number of speech samples submitted for enrollment for this user"""
        return self._enrollments_count

    def get_remaining_enrollments_count(self):
        """Returns the number of speech samples required remaining to complete enrollment"""
        return self._remaining_enrollments_count

    def get_created_date_time(self):
        """Returns the creation date time of the user"""
        return self._created_date_time

    def get_last_action_date_time(self):
        """Returns the last action date time of the user"""
        return self._last_action_date_time

    def get_enrollment_status(self):
        """Returns the enrollment status of the user"""
        return self._enrollment_status

class VerificationResponse:
    """This class encapsulates the verification response."""

    _RESULT = 'result'
    _CONFIDENCE = 'confidence'

    def __init__(self, response):
        """Constructor of the VerificationResponse class.

        Arguments:
        response -- the dictionary of the deserialized python response
        """
        self._result = response.get(self._RESULT, None)
        self._confidence = response.get(self._CONFIDENCE, None)

    def get_result(self):
        """Returns whether the voice clip belongs to the profile (Accept / Reject)"""
        return self._result

    def get_confidence(self):
        """Returns the verification confidence"""
        return self._confidence

def verify_file(subscription_key, file_path, profile_id):
    """verify a profile based on submitted audio sample

    Arguments:
    subscription_key -- the subscription key string
    file_path -- the audio file path for verification
    profile_id -- ID of a profile to attempt to match the audio sample to
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)
    verification_response = helper.verify_file(file_path, profile_id)
    print('Verification Result = {0}'.format(verification_response.get_result()))
    print('Confidence = {0}'.format(verification_response.get_confidence()))



if __name__ == "__main__":
    """create profiles from number of speakers argument and the subscription key"""
    """ MSA_Verif_API.py -cp number_of_speakers -k subscription_key"""
    # elif (sys.argv[1] == '--create_profiles') or (sys.argv[1] == '-cp'):
    if (args.create) :
        if len(sys.argv) < 5 : 
            print('ERROR: MSA_Verif_API.py -cp number_of_speakers -k subscription_key')
        else:
            n = int(sys.argv[2])
            for i in range(n) :
                create_profile(sys.argv[4], 'en-us')

            helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
                    sys.argv[4])
            profiles = helper.get_all_profiles()
            f = open("ID_List.txt","w")
            for profile in profiles:
                f.write("{0}\n".format(profile.get_profile_id()))



        """ enroll profiles using the key, ID_List.txt, and directory of .wav files """
    elif (args.enroll) :
        if (args.recursive):
            try :
                SpeakDir = args.recursive
                key = args.key
                f = args.filename
                idlist = [] 
                for line in open(f) : # array of id's for easy access
                    idlist.append(line)
                i = 0
                for speaker in os.listdir(SpeakDir) :
                    # print(idlist[i])
                    pid = idlist[i]
                    for wave in os.listdir("{0}/{1}".format(SpeakDir,speaker)) :
                        # print("{0}-->{1}".format(wave,pid))
                        path = "{0}/{1}/{2}".format(SpeakDir,speaker,wave)
                        # print(path)
                        enroll_profile(key,pid,path)
                    i+=1
            except :
                print("ERROR: python MSA_Verif_API.py -ep -r [Directory] -k [key] -f [ID_List.txt]")
        else : #  MSA_Verif_API.py -ep -k [key] -p [pid] -f [.wav]
            wave = args.filename
            key = args.key
            pid = args.profile
            enroll_profile(key,pid,wave)




        """ list all profiles enrolled for the given subscription  and save them to a .txt file"""
    elif (args.list) :
        try :
            helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
                    args.key)
            profiles = helper.get_all_profiles()
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
                    profiles.append(line)

                for folder in os.listdir(VoiceDir) :
                    voice_folders.append("{0}/{1}".format(VoiceDir,folder))

                i=0
                for folder in voice_folders:
                    for wav in os.listdir(folder) :
                        filename = "{0}/{1}".format(folder,wave)
                        verify_file(key,filename,profiles[i])
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
                print("ERROR: python MSA_Verif_API.py --verify --key [key] --profile [pid] -f [voice]")


        """ """
    elif (args.delete) :
        if (len(sys.argv) < 3) :
            print("ERROR: python MSA_Verif_API.py --delete_profile --filename ID_list --profile profile_id --key subscription_key")
        elif (args.filename) :
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

