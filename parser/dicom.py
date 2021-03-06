import re

PATIENT_NAME = 'PatientName'
PATIENT_BIRTHDATE = 'PatientBirthDate'
PATIENT_ID = 'PatientID'
PATIENT_SEX = 'PatientSex'
STUDY_DATE = 'StudyDate'
MODALITY = 'Modality'
BODY_PART_EXAMINED = 'BodyPartExamined'
STUDY_DESCRIPTION = 'StudyDescription'
SERIES_DESCRIPTION = 'SeriesDescription'
ACCESSION_NUMBER = 'AccessionNumber'
STUDY_ID = 'StudyID'
SERIES_NUMBER = 'SeriesNumber'
INSTANCE_NUMBER = 'InstanceNumber'
REFERRING_PHYSICIAN_NAME = 'ReferringPhysicianName'
INSTANCE_AVAILABILITY = 'InstanceAvailability'
INSTITUTION_NAME = 'InstitutionName'
STUDY_INSTANCE_UID = 'StudyInstanceUID'
SERIES_INSTANCE_UID = 'SeriesInstanceUID'
SPECIFIC_CHARACTER_SET = 'SpecificCharacterSet'
QUERY_RETRIEVE_LEVEL = 'QueryRetrieveLevel'
RETRIEVE_AE_TITLE = 'RetrieveAETitle'

TAGS = {
    '(0010,0010)': PATIENT_NAME,
    '(0010,0030)': PATIENT_BIRTHDATE,
    '(0010,0020)': PATIENT_ID,
    '(0010,0040)': PATIENT_SEX,
    '(0008,0020)': STUDY_DATE,
    '(0008,0060)': MODALITY,
    '(0018,0015)': BODY_PART_EXAMINED,
    '(0008,1030)': STUDY_DESCRIPTION,
    '(0008,103e)': SERIES_DESCRIPTION,
    '(0008,0050)': ACCESSION_NUMBER,
    '(0020,0010)': STUDY_ID,
    '(0020,0011)': SERIES_NUMBER,
    '(0020,0013)': INSTANCE_NUMBER,
    '(0008,0090)': REFERRING_PHYSICIAN_NAME,
    '(0008,0056)': INSTANCE_AVAILABILITY,
    '(0008,0080)': INSTITUTION_NAME,
    '(0020,000d)': STUDY_INSTANCE_UID,
    '(0020,000e)': SERIES_INSTANCE_UID,
    '(0008,0005)': SPECIFIC_CHARACTER_SET,
    '(0008,0052)': QUERY_RETRIEVE_LEVEL,
    '(0008,0054)': RETRIEVE_AE_TITLE
}


def get_headers(fileobject):
    result = []
    single_header = {}
    for line in fileobject:
        if is_valid(line):
            single_header[get_tag(line)] = get_value(line)
        if is_start_or_end(line) and single_header:
            result.append(single_header.copy())
            single_header.clear()
    return result


def is_start_or_end(line):
    """ Returns True if it is the start or end of a DICOM header.
        Checks for an Line 'W:<empty space>'
     """
    return re.match('^W:\s*$', line)


def is_valid(line):
    return line.startswith('W:') \
           and '(' in line and ')' in line and '[' in line and ']' in line


def get_tag_value(line):
    return get_tag(line), get_value(line)


def get_tag(line):
    """
    Returns the tag value of the line, which is everything between
    the first square brackets.
    For example on this line
        W: (0010,0040) CS [F ]
    tag value would be (0010,0040)
    """
    return TAGS[line[3:14]]


def get_value(line):
    """
    Returns the value of the line, which is everything between
    the first and last square bracket.
    :param line: a line of the dicom file
    :return: value
    """
    x = line.find('[') + 1
    y = line.rfind(']')
    return line[x:y].strip()
