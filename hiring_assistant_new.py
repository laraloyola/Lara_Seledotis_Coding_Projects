import pypdf
import pdfminer.high_level
from pypdf import PdfReader
import os
import re

leadership_buzzwords = ["team lead", "Leadership", "Led", "Trained"]

'''Import the resume samples, scan each one. For skills like Python rank their years of 
experience as 'strong', 'moderate', or 'entry-level'. 
 Step1) install pypdf and be able to read pdf imported'''

def read_pdf(filepath):
    document_info = None
    text = ""
    num_pages = 0
    try:
        reader = PdfReader(filepath)
        document_info = reader.metadata
        num_pages = len(reader.pages)
        print(f"Number of pages: {num_pages}")
        for page in reader.pages:
            page_text = page.extract_text() #pulls from each page
            if page_text:
                text += page_text
    except Exception:
        print("Cannot read pdf")
        text = pdfminer.high_level.extract_text(filepath)
    return text, document_info, num_pages

def main():
    applicant_list = []
    count = 0
    folder_path = r"C:\\Users\\laran\\PycharmProjects\\PythonProject\\engr352_pycharm\\SampleResumes"
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(".pdf"):
                filepath = os.path.join(root, filename)
                print(f"\n\nReading: {filename}")
                try:
                    text, document_info, num_pages = read_pdf(filepath)
                    candidate, matched_skills, candidate_score, min_score = quantify_candidate(text, count, document_info, num_pages)
                    total_score = matched_skills + candidate_score + min_score
                    qualified = (min_score >= 3)
                    if not qualified:
                        print(f"Applicant {candidate[0]} does not meet minimum requirements")
                    candidate.append(f"Filename: {filename}")
                    candidate.append(f"Total score {total_score}")
                    candidate.append(f"Qualified? {qualified}") #search for last value in list to determine if we should match them or not
                    applicant_list.append(candidate)  # get all candidates, their scores and skills together for sorting
                    count += 1
                except Exception as error:
                    print(f"Error reading {filename}: {error}")
                    continue

    if len(applicant_list) == 0:
        print("No applicant found")
        return None
    #begin sorting candidates by matched skills, score and qualifications
    #use quicksort since we have less than 30 resumes to filter, if greater than 30 use mergesort
    ranked_list = quicksort(applicant_list, 0, len(applicant_list) - 1) #sort by score
    print("___________Ranked Values____________")
    print("___________ Rankings of ALL Applicants ___________")
    i = 0
    for applicant in ranked_list:
        i += 1
        print(f"{i}. Name: {applicant[0]} Total Score: {get_score(applicant)}")
    if ranked_list:
        print("Top Applicant:", ranked_list[0])
    else:
        print("No applicant found")
    meets_minimum_req = []
    for person in ranked_list:
        for skill in person:
            if skill == "Qualified? True":
                meets_minimum_req.append(person)

    print(f"\n\nNumber of Applicants who meet minimum requirements: {len(meets_minimum_req)}")
    print("___________ Rankings of Applicants Who Meet Minimum Requirements ___________")
    i = 0
    for applicant in meets_minimum_req:
        i += 1
        print(f"{i}. Name: {applicant[0]} Total Score: {get_score(applicant)}")
    if meets_minimum_req:
        print("Top Applicant:", meets_minimum_req[0])
    else:
        print("No qualified applicants meet minimum requirements")

    candidate_number = get_input()
    i = 0
    if candidate_number <= 4 and candidate_number != None:
        print(f"Here is {candidate_number} of applicant's that meet the minimum requirements")
        for applicant in meets_minimum_req:
            i += 1
            print(f"{i}. Name: {applicant[0]} Total Score: {get_score(applicant)}")
            print(f"Profile {applicant}")
    elif candidate_number != None:
        print(f"We only have {len(meets_minimum_req)} applicants who meet the minimum requirements")
        print("Here are those who meet the minimum requirements")
        i = 0
        for applicant in meets_minimum_req:
            i += 1
            print(f"{i}. Name: {applicant[0]} Total Score: {get_score(applicant)}")
            print(f"Profile {applicant}")
        j = 0
        remaining = candidate_number - len(meets_minimum_req)
        if remaining > 0:
            print("Here are other applicants who scored highly")
            j = 0
            for applicant in ranked_list: #print top x candidates who are NOT in meets_minimum_req
                if applicant not in meets_minimum_req and j < remaining:
                    i += 1
                    print(f"{i}. Name: {applicant[0]} Total Score: {get_score(applicant)}")
                    print(f"Profile: {applicant}")
                    j += 1
    else:
        print("\n")







'''sort score and name from each candidate, (title), then do mergesort to filter the highest score
then print highest score and their skills'''

def quantify_candidate(resume_text, count, document_info, num_pages):
    ''' function to go through candidate resume and quantify skills.
    Returns a list of their name and their highlighted skills. Maybe
    good to use linked list of candidate and their attributes'''
    candidate = []
    name_provided = False
    if document_info.title is None:
        print("No name provided")
    else:
        print(f"Candidate Name: {document_info.title}")
        candidate.append(document_info.title)
        name_provided = True
    if document_info.author is not None:
        print("Author:", document_info.author)
        #name_provided = True
        #candidate.append(document_info.author) #author instead of name
    resume_text = resume_text.lower()
    #l_buzzwords = [item.lower() for item in buzzwords]
    l_leadership_buzzwords = [item.lower() for item in leadership_buzzwords]
    word = resume_text.split()
    matched_skills = 0

    for i in range(len(word)):
        if word[i].startswith("gpa"):
            gpa_match = re.search(r"\d+\.\d+", " ".join(word[i:i+3]))
            if gpa_match:
                candidate.append(f"gpa: {gpa_match.group()}") #captures other types of formats
    for keyword in l_leadership_buzzwords:
        if keyword in resume_text.lower():
            candidate.append("Leadership Skills")
            matched_skills += 1

    #filter through synonyms / wording issues
    ''' loop through resume_text and see if phrase matches'''
    minimum_req = []
    pref_req = []
    ideal_req = []
    min_score = 0
    pref_score = 0
    ideal_score = 0
    c_minreq = {
    "Software Design": ["software", "software design", "software development"],
    "Hardware Design": ["hardware", "hardware design", "hardware development"],
    "Co-Design Experience": ["co-design", "codesign", "design", "designed", "designing", "co design", "co engineered"],
    "Computer Engineering": ["computer engineering", "computer engineer", "computer eng", "compe", "comp-e", "comp-eng"]}
    c_prefreq = {
        "Research Experience": ["research", "researched", "academic research"],
        "Development Experience": ["development", "developed", "dev", "implementation"],
        "Research and Development": ["research and development", "r&d", "r and d", "r & d"],
        "Project Management Experience": ["project management", "project manager", "project lead",
        "program manager", "program lead", "team lead", "team manager"]}
    c_idealreq = {
    "Python Knowledge": ["knowledge of python", "python", "python programming", "python developer"],
    "VHDL Knowledge": ["vhdl", "vhdl design"],
    "Assembly Language": ["assembly", "assembly language", "risc-v", "riscv"],
    "Leadership Skills": ["team lead", "led team", "leadership", "mentored", "trained others"]}
    ###################THIS DOESNT WORK NEED TO REDO THIS
    resume_lower = resume_text.lower()
    #minimum
    for skills, synonyms in c_minreq.items():
        #check if synonym in text
        for word in synonyms:
            if word in resume_lower:
                minimum_req.append(skills)
                min_score += 1

    print("MINIMUM SCORE", min_score, minimum_req)

    #preferred
    for skills, synonyms in c_prefreq.items():
        for word in synonyms:
            if word in resume_lower:
                pref_req.append(skills)
                pref_score += 1

    #ideal
    for skills, synonyms in c_idealreq.items():
        for word in synonyms:
            if word in resume_lower:
                ideal_req.append(skills)
                ideal_score += 1

    #### add minimum, preffered and ideal skills to total skills
    for skill in minimum_req:
        candidate.append(skill)
        matched_skills += 1
    for skill in pref_req:
        candidate.append(skill)
        matched_skills += 2
    for skill in ideal_req:
        candidate.append(skill)
        matched_skills += 3

    ''' eliminate redundancy in candidate list '''
    #remove duplicate strings
    candidate = list(dict.fromkeys(candidate)) #remove duplicates from list
    matched_skills = len(candidate) - 1
    #filter gpa
    gpa_entry = next((item for item in candidate if "gpa:" in item.lower()), None)
    if gpa_entry:
        candidate_score, performance = gpa_scores(gpa_entry)
    else:
        candidate_score, performance = gpa_scores("gpa: 0.0")

    if name_provided == False: #if no name give applicant number
        candidate.insert(0, f"Applicant{count}")

    if num_pages > 1:
        candidate_score -= 1 #resume should only be one page
        candidate.append("Improper Resume Format")

    #update candiate score with minimum, preffered and ideal qualifications
    candidate_score = candidate_score + min_score + pref_score + ideal_score
    #last two values in candidate list will be skills score and candidate score in that order
    #this will be used in rankings
    candidate.append(performance)
    candidate.append(matched_skills)
    candidate.append(candidate_score)

    #formatting capital letters
    cap_list = []
    for item in candidate:
        if type(item) == str:
            cap_list.append(item.capitalize())
        else:
            cap_list.append(item)
    candidate = cap_list

    print("Candidate profile:", candidate)
    print("Skills Matched:", matched_skills)
    print("Candidate Score:", candidate_score)

    return candidate, matched_skills, candidate_score, min_score


def gpa_scores(gpa):
    ''' linked list implementation for person and their skills. Rank them and compare'''
    candidate_score = 0
    filtered_gpa = ""
    numbers = gpa.split() #split off the 'gpa: from number
    if len(numbers) < 2: #if no GPA
        return 0, "No GPA Found"
    need_split = False
    #regular expressions for characters and next patterns
    #use r as regualr expression (backslashes), \d+ for multiple digits, . for decimal, and numbers[1] for string after GPA
    correct_format = re.search(r"\d+\.\d+", numbers[1]) #make sure there are no more than those 2 strings gpa and numbers
    #correct_format returns true if there is GPA if not it is none
    if not correct_format:
        return 0, "Invalid GPA Format"
    filtered_gpa = float(correct_format.group())
    if filtered_gpa > 3.9:
        candidate_score += 3
        print("Excellent GPA")
        performance = "Excellent GPA"
    elif filtered_gpa > 3.75:
        candidate_score += 2
        print("Great GPA")
        performance = "Great GPA"
    elif filtered_gpa > 3.5:
        candidate_score += 1
        print("Good GPA")
        performance = "Good GPA"
    elif filtered_gpa > 3.0:
        candidate_score += 0
        print("Below Average GPA")
        performance = "Below Average GPA"
    else:
        candidate_score -= 2
        print("Note: Low GPA of", filtered_gpa)
        performance = "Low GPA"
    return candidate_score, performance

def quicksort(unranked_list, p, q):
    ''' sort the list based on total score. Want to sort based on total score but keep applicant name and associated values
            linked along -- format for _applicant list input
    list = [[Applicant, skill1, skill2, skill3, ..., total_score, qualified],
            [Applicant2, skill1, skill2, skill3, ..., total_score, qualified], ...] '''
    if p < q:
        pivot = partition(unranked_list, p, q) #split
        quicksort(unranked_list, p, pivot - 1) #left side
        quicksort(unranked_list, pivot + 1, q) #right side

    return unranked_list

def partition(unranked_list, p, q):
    ''' quicksort partition in descending order for total score'''
    pivot = unranked_list[q] #last value is pivot point
    pivot_score = get_score(pivot) #getting score of our value
    i = p - 1
    for j in range(p, q): #iterate through list
        if get_score(unranked_list[j]) >= pivot_score: #descending order, we want it to be greater
            i += 1 #increase iteration
            temp = unranked_list[i]
            unranked_list[i] = unranked_list[j]
            unranked_list[j] = temp #swap
    temp = unranked_list[i + 1]
    unranked_list[i + 1] = unranked_list[q]
    unranked_list[q] = temp #swap ending
    return i + 1


def get_score(candidate):
    #get score back (not hard coded)
    score = 0
    for person in candidate:
            if (str(person).lower().startswith("total score") or str(person).lower().startswith("total score:")):
                score = int(person.split()[-1])
    return score
def get_input():
    candidate_number = input("\nHow many people do you want to hire?")
    if candidate_number.isdigit():
        return int(candidate_number)
    else:
        return None

main()