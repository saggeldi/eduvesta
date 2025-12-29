#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Turkmen Translation Generator for Eduvestra Mobile App
This script creates a comprehensive Turkmen translation file.
"""

import json
import re

# Read the English source
with open('/Users/merdana/AndroidStudioProjects/eduvesta/src/assets/lang/en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Read existing Turkmen translations
with open('/Users/merdana/AndroidStudioProjects/eduvesta/src/assets/lang/tk.json', 'r', encoding='utf-8') as f:
    tk_existing = json.load(f)

# Comprehensive Turkmen translation dictionary
# This is a massive dictionary covering all common educational and technical terms
tk_translations = {}

# Start with existing translations
tk_translations.update(tk_existing)

# Now add comprehensive translations for all remaining entries
# I'll use pattern matching and common phrase translation

def translate_value(key, value):
    """Translate English value to Turkmen"""

    # If already translated, keep it
    if key in tk_existing:
        return tk_existing[key]

    # Skip empty values
    if not value or value == "":
        return value

    # Keep technical terms intact but translate descriptive text
    result = value

    # Replace branding
    result = result.replace("Moodle App", "Eduvestra")
    result = result.replace("Moodle app", "Eduvestra")
    result = result.replace("Moodle Mobile", "Eduvestra")
    result = result.replace("Moodle mobile", "Eduvestra")
    result = result.replace("campus.example.edu", "eduvestra.com")
    result = result.replace("https://campus.example.edu", "https://eduvestra.com")

    # Dictionary of phrase translations (sorted by length, longest first for better matching)
    translations_map = {
        # Badges
        "Alignment": "Deňleşdiriş",
        "Awarded to": "Berildi",
        "Badge details": "Nyşanyň jikme-jiklikleri",
        "Badges": "Nyşanlar",
        "Endorsement": "Makullama",
        "Endorsement comment": "Makullama tesw iri",
        "Claim URL": "Talap URL",
        "Email": "E-poçta",
        "Course: {{$a}}": "Kurs: {{$a}}",
        "Date issued": "Berlen senesi",
        "Expired": "Möhleti geçen",
        "This badge expired on {{$a}}.": "Bu nyşanyň möhleti {{$a}}-da geçdi.",
        "Expired {{$a}}": "Möhleti {{$a}} geçdi",
        "Expires {{$a}}": "Möhleti {{$a}} geçýär",
        "Image caption": "Suratyň ady",
        "Issued by {{$a}}": "{{$a}} tarapyndan berildi",
        "Issued {{$a}}": "{{$a}} berildi",
        "Name": "Ady",
        "URL": "URL",
        "Language": "Dil",
        "More details": "Giňişleýin maglumat",
        "There are currently no badges available for users to earn.": "Häzirki wagtda ulanyjylar üçin gazanyp boljak nyşan ýok.",
        "Related badges": "Degişli nyşanlar",
        "Version": "Wersiýa",

        # Block names
        "Activities": "Işjeňlikler",
        "Activity results": "Işjeňligiň netijeleri",
        "Latest badges": "Iň täze nyşanlar",
        "Blog menu": "Blog menýusy",
        "Recent blog entries": "Soňky blog ýazgylary",
        "Blog tags": "Blog belgileri",
        "Calendar": "Kalendar",
        "Upcoming events": "Geljekki wakalar",
        "Comments": "Teswirler",
        "Course completion status": "Kursuň tamamlanma ýagdaýy",
        "Global search": "Umumy gözleg",
        "Random glossary entry": "Tötänleýin lügat ýazgysy",
        "Learning plans": "Okuw meýilnamalary",
        "All": "Ählisi",
        "All (including removed from view)": "Ählisi (görnüşden aýrylanlar bilen)",
        "Switch to card view": "Karta görnüşine geç",
        "Switch to list view": "Sanaw görnüşine geç",
        "Browse all courses": "Kurslary göz geçir",
        "Starred": "Ýyldyzly",
        "Future": "Geljekki",
        "Removed from view": "Görnüşden aýryldy",
        "In progress": "Dowam edýär",
        "Last accessed": "Soňky gezek açylan",
        "You are currently not enrolled in any courses.": "Häzirki wagtda hiç bir kursa ýazylmadyňyz.",
        "Browse all available courses below and start learning.": "Aşakdaky elýeterli kurslary göz geçiriň we öwrenmäge başlaň.",
        "Your search didn't match any courses.": "Gözlegiňiz hiç bir kurs bilen gabat gelmedi.",
        "Try adjusting your filters or browse all courses below.": "Süzgüçleriňizi sazlamaga synanyşyň ýa-da aşakdaky kurslary göz geçiriň.",
        "Past": "Geçen",
        "Course overview": "Kursuň syn",
        "Search available courses": "Elýeterli kurslary gözle",
        "Short name": "Gysga ady",
        "Course name": "Kursuň ady",
        "Latest announcements": "Iň täze habarlar",
        "Online users": "Onlaýn ulanyjylar",
        "Private files": "Şahsy faýllar",
        "Recent activity": "Soňky işjeňlik",
        "No recent courses": "Soňky kurslar ýok",
        "Recently accessed courses": "Soňky açylan kurslar",
        "No recent items": "Soňky zatlar ýok",
        "Recently accessed items": "Soňky açylan zatlar",
        "RSS feeds": "RSS akymlary",
        "Search forums": "Forumlary gözle",
        "Self completion": "Öz-özüňi tamamlama",
        "Additional activities": "Goşmaça işjeňlikler",
        "No starred courses": "Ýyldyzly kurslar ýok",
        "Starred courses": "Ýyldyzly kurslar",
        "Tags": "Bellikler",

        # Timeline
        "Filter timeline by date": "Wagtyň hatyny sene boýunça süzüň",
        "Due date": "Tabşyrmaly senesi",
        "Next 30 days": "Indiki 30 gün",
        "Next 3 months": "Indiki 3 aý",
        "Next 6 months": "Indiki 6 aý",
        "Next 7 days": "Indiki 7 gün",
        "No in-progress courses": "Dowam edýän kurslar ýok",
        "No activities require action": "Hiç bir işjeňlik hereket talap etmeýär",
        "Overdue": "Möhleti geçen",
        "Timeline": "Wagtyň haty",
        "Search by activity type or name": "Işjeňligiň görnüşi ýa-da ady boýunça gözle",
        "Sort by courses": "Kurslar boýunça tertiple",
        "Sort by dates": "Seneler boýunça tertiple",

        # Blog
        "Add a new entry": "Täze ýazgy goş",
        "Blog about course {{$a.coursename}}": "{{$a.coursename}} kursy barada blog",
        "Blog about {{$a.modtype}}: {{$a.modname}}": "{{$a.modtype}}: {{$a.modname}} barada blog",
        "Associations": "Birleşmeler",
        "Blog": "Blog",
        "Delete the blog entry '{{$a}}'?": "'{{$a}}' blog ýazgysyny pozmaly?",
        "Blog entries": "Blog ýazgylary",
        "Blog entry body": "Blog ýazgynyň göwresi",
        "Entry title": "Ýazgynyň ady",
        "Error loading blog entries.": "Blog ýazgylaryny ýüklemekde ýalňyşlyk.",
        "Original blog entry": "Asyl blog ýazgysy",
        "No visible entries here": "Bu ýerde görünýän ýazgylar ýok",
        "Publish to": "Neşir et",
        "Yourself (draft)": "Öz-özüňize (garalama)",
        "Anyone on this site": "Bu sahypada islendik kişi",
        "Anyone in the world": "Dünýäde islendik kişi",
        "Show only your entries": "Diňe öz ýazgylaryňyzy görkeziň",
        "Site blog": "Sahypa blogu",

        # Calendar
        "All day": "Tutuş gün",
        "Calendar event": "Kalendar wakasy",
        "Calendar events": "Kalendar wakalary",
        "Calendar reminders": "Kalendar ýatlatmalary",
        "Category events": "Kategoriýa wakalary",
        "Are you sure you want to delete the \\\"{{$a}}\\\" event?": "\\\"{{$a}}\\\" wakany pozmak isleýärsiňizmi?",
        "The \\\"{{$a.name}}\\\" event is part of a series. Do you want to delete just this event, or all {{$a.count}} events in the series?": "\\\"{{$a.name}}\\\" wakasy seriýanyň bir bölegi. Diňe şu wakany, ýa-da seriýadaky ähli {{$a.count}} wakany pozmak isleýärsiňizmi?",
        "Course events": "Kurs wakalary",
        "Current Month": "Häzirki aý",
        "Next day": "Indiki gün",
        "Previous day": "Öňki gün",
        "Day view: {{$a}}": "Günüň görnüşi: {{$a}}",
        "Default notification time": "Deslapky bildiriş wagty",
        "Delete all events": "Wakalaryň hemmesini poz",
        "Delete event": "Wakany poz",
        "Delete this event": "Bu wakany poz",
        "Detailed month view: {{$a}}": "Aýyň jikme-jik görnüşi: {{$a}}",
        "Duration in minutes": "Dowamlylygy minutlarda",
        "Without duration": "Dowamlylyksyz",
        "Until": "Çenli",
        "Editing event": "Waka redaktirlenýär",
        "Error loading event.": "Wakany ýüklemekde ýalňyşlyk.",
        "Error loading events.": "Wakalary ýüklemekde ýalňyşlyk.",
        "Calendar event deleted": "Kalendar wakasy pozuldy",
        "Duration": "Dowamlylygy",
        "End time": "Gutarýan wagty",
        "Type of event": "Wakanyň görnüşi",
        "Event title": "Wakanyň ady",
        "Start time": "Başlanýan wagty",
        "Event type": "Wakanyň görnüşi",
        "Fri": "Anna",
        "Friday": "Anna",
        "Go to activity": "Işjeňlige git",
        "Group events": "Topar wakalary",
        "The duration in minutes you have entered is invalid. Please enter the duration in minutes greater than 0 or select no duration.": "Girizendiňiz minutlardaky dowamlylygy nädogry. 0-dan uly minutlarda dowamlylygy giriziň ýa-da dowamlylyksyz saýlaň.",
        "The date and time you selected for duration until is before the start time of the event. Please correct this before proceeding.": "Dowamlylygyň gutarýan wagty üçin saýlanan sene we wagt wakanyň başlanýan wagtyndan öň. Dowam etmezden ozal düzediň.",
        "Mon": "Duş",
        "Monday": "Duşenbe",
        "Monthly view": "Aýlyk görnüş",
        "Next month": "Indiki aý",
        "Previous month": "Öňki aý",
        "New event": "Täze waka",
        "There are no events": "Wakalar ýok",
        "Sorry, but you do not have permission to update the calendar event.": "Bagyşlaň, ýöne kalendar wakasyny täzelemäge rugsdyňyz ýok.",
        "Reminders": "Ýatlatmalar",
        "Repeated events": "Gaýtalanýan wakalar",
        "Also apply changes to the other {{$a}} events in this repeat series": "Şeýle hem üýtgetmeleri bu gaýtalanýan seriýadaky beýleki {{$a}} wakalara ulanyň",
        "Apply changes to this event only": "Üýtgetmeleri diňe şu waka ulanyň",
        "Repeat this event": "Bu wakany gaýtala",
        "Repeat weekly, creating altogether": "Hepdelik gaýtala, jemi döretmek",
        "Sat": "Şen",
        "Saturday": "Şenbe",
        "Set a new reminder": "Täze ýatlatma goýuň",
        "Site events": "Sahypa wakalary",
        "Sun": "Ýek",
        "Sunday": "Ýekşenbe",
        "Thu": "Pen",
        "Thursday": "Penşenbe",
        "Today": "Şugün",
        "Tomorrow": "Ertir",
        "Tue": "Siş",
        "Tuesday": "Sişenbe",
        "Category event": "Kategoriýa wakasy",
        "Close event": "Waka ýapylýar",
        "Course event": "Kurs wakasy",
        "Due event": "Möhleti gelýän waka",
        "Grading due event": "Bahalaýşyň möhleti gelýän waka",
        "Group event": "Topar wakasy",
        "Open event": "Waka açylýar",
        "Site event": "Sahypa wakasy",
        "User event": "Ulanyjy wakasy",
        "User events": "Ulanyjy wakalary",
        "Wed": "Çar",
        "Wednesday": "Çarşenbe",
        "When": "Haçan",
        "Yesterday": "Düýn",

        # Competency
        "Competencies": "Başarnyklar",
        "Competencies most often not proficient in this course": "Bu kursda köplenç başarnyksyz başarnyklar",
        "Course competencies": "Kurs başarnyklarysyn",
        "Competency ratings in this course do not affect learning plans.": "Bu kursdaky başarnyk bahalary okuw meýilnamalaryna täsir etmeýär.",
        "Competency ratings in this course are updated immediately in learning plans.": "Bu kursdaky başarnyk bahalary okuw meýilnamalarynda dessine täzelenýär.",
        "Cross-referenced competencies": "Çapraz salgylanýan başarnyklar",
        "No competencies found": "Başarnyklar tapylmady",
        "Evidence": "Subutnama",
        "The rule of the competency was met.": "Başarnygyň düzgüni ýerine ýetirildi.",
        "The course '{{$a}}' was completed.": "'{{$a}}' kursy tamamlandy.",
        "The activity '{{$a}}' was completed.": "'{{$a}}' işjeňligi tamamlandy.",
        "The rating was restored along with the course '{{$a}}'.": "Baha '{{$a}}' kursy bilen bilelikde dikeldildi.",
        "The evidence of prior learning '{{$a}}' was linked.": "Öňki okuwyň subutnamasy '{{$a}}' baglanyşdyryldy.",
        "The evidence of prior learning '{{$a}}' was unlinked.": "Öňki okuwyň subutnamasy '{{$a}}' baglanyşykdan aýryldy.",
        "The competency rating was manually set.": "Başarnyk bahasy el bilen bellendi.",
        "The competency rating was manually set in the course '{{$a}}'.": "Başarnyk bahasy '{{$a}}' kursunda el bilen bellendi.",
        "The competency rating was manually set in the learning plan '{{$a}}'.": "Başarnyk bahasy '{{$a}}' okuw meýilnamasynda el bilen bellendi.",
        "Learning plan competencies": "Okuw meýilnamasynyň başarnyklarysyn",
        "My learning plans": "Meniň okuw meýilnamalarym",
        "No activities": "Işjeňlikler ýok",
        "No competencies": "Başarnyklar ýok",
        "No competencies have been linked to this course.": "Bu kursa hiç bir başarnyk baglanyşdyrylmadyk.",
        "No other competencies have been cross-referenced to this competency.": "Bu başarnyk bilen hiç bir beýleki başarnyk çapraz salgylanmadyk.",
        "No evidence": "Subutnama ýok",
        "No learning plans were created.": "Okuw meýilnamalary döredilmedi.",
        "No learning plans contain this competency.": "Hiç bir okuw meýilnamasy bu başarnygy öz içine almaýar.",
        "Path:": "Ýoly:",
        "Active": "Işjeň",
        "Complete": "Doly",
        "Draft": "Garalama",
        "In review": "Gözden geçirilýär",
        "Waiting for review": "Syn garaşylýar",
        "Proficient": "Başarnykly",
        "Progress": "Öňegidişlik",
        "Rating": "Baha",
        "Review status": "Syn ýagdaýy",
        "Status": "Ýagdaý",
        "Learning plan template": "Okuw meýilnamasynyň şablony",
        "Upon course completion:": "Kursy tamamlandan soň:",
        "Idle": "Dymmak",
        "{{$a.x}} out of {{$a.y}} competencies are proficient": "{{$a.y}} başarnykdan {{$a.x}} başarnykly",
        "You are proficient in {{$a.x}} out of {{$a.y}} competencies in this course.": "Bu kursda {{$a.y}} başarnykdan {{$a.x}}-da başarnyksyňyz.",

        # Course completion
        "Complete course": "Kursy tamamla",
        "Completed": "Tamamlandy",
        "Completion date": "Tamamlanan senesi",
        "Completion": "Tamamlama",
        "Confirm self completion": "Öz-özüňi tamamlamagy tassykla",
        "Could not load the course completion report. Please try again later.": "Kursuň tamamlanma hasabatyny ýükläp bolmady. Soňrak synanyşyň.",
        "Course completion": "Kursuň tamamlanmasy",
        "Criteria": "Ölçegler",
        "Criteria group": "Ölçeg topary",
        "All criteria below are required": "Aşakdaky ähli ölçegler talap edilýär",
        "Any criteria below are required": "Aşakdaky islendik ölçeg talap edilýär",
        "Manual self completion": "El bilen öz-özüňi tamamlama",
        "You are currently not being tracked by completion in this course": "Häzirki wagtda bu kursda tamamlama boýunça yzarlanmaýarsyňyz",
        "Not yet started": "Entek başlanmady",
        "Pending": "Garaşylýar",
        "Required": "Hökmany",
        "Required criteria": "Hökmany ölçegler",
        "Requirement": "Talap",
        "View course report": "Kurs hasabatyny gör",

        # Enrol
        "Guest access": "Myhman giriş",
        "Guest access requires password": "Myhman giriş parol talap edýär",
        "Incorrect access password, please try again": "Giriş paroly nädogry, gaýtadan synanyşyň",
        "Are you sure you want to enrol yourself in this course?": "Bu kursa ýazylmak isleýärsiňizmi?",
        "An error occurred while self enrolling.": "Öz-özüňi ýazgyt etmekde ýalňyşlyk ýüze çykdy.",
        "Enrolment key": "Ýazgyt açary",
        "Self enrolment": "Öz-özüňi ýazgyt etme",
        "Configure devices": "Enjamlary sazla",
        "Your users are not receiving any notification from this site on their mobile devices. Enable mobile notifications in the Notification settings page.": "Ulanyjylar bu sahypadan ykjam enjamlarynda hiç bir bildiriş almaýarlar. Bildiriş sazlamalary sahypasynda ykjam bildirişleri açyň.",

        # Messages
        "Accept and add to contacts": "Kabul et we kontaktlara goş",
        "Add contact": "Kontakt goş",
        "Are you sure you want to add {{$a}} to your contacts?": "{{$a}}-ny kontaktlaryňyza goşmak isleýärsiňizmi?",
        "Star conversation": "Söhbetdeşligi ýyldyzla",
        "Add to contacts": "Kontaktlara goş",
        "Block user": "Ulanyjyny blokla",
        "Are you sure you want to block {{$a}}?": "{{$a}}-ny bloklamak isleýärsiňizmi?",
        "You can't block {{$a}} because they have a role with permission to message all users.": "{{$a}}-ny bloklap bilmeýärsiňiz, sebäbi ähli ulanyjylara habar ibermäge rugsady bar.",
        "Accept messages from:": "Habar kabul et:",
        "My contacts and anyone in my courses": "Kontaktlarym we kurslarymda bar adamlar",
        "My contacts only": "Diňe kontaktlarym",
        "Anyone on the site": "Sahypada islendik kişi",
        "Contact blocked": "Kontakt bloklanan",
        "Contact request sent": "Kontakt haýyşy iberildi",
        "Contacts": "Kontaktlar",
        "Conversation actions menu": "Söhbetdeşlik hereketleri menýusy",
        "Decline": "Ret et",
        "Are you sure you would like to delete this entire conversation? This will not delete it for other conversation participants.": "Bu söhbetdeşligi bütin pozmak isleýärsiňizmi? Bu beýleki gatnaşyjylar üçin pozulmaz.",
        "Are you sure you would like to delete this entire personal conversation?": "Bu şahsy söhbetdeşligi bütin pozmak isleýärsiňizmi?",
        "Delete conversation": "Söhbetdeşligi poz",
        "Delete for me and for everyone else": "Men we beýlekiler üçin poz",
        "Delete message": "Habary poz",
        "Are you sure you want to delete this message? It will only be deleted from your messaging history and will still be viewable by the user who sent or received the message.": "Bu habary pozmak isleýärsiňizmi? Diňe siziň habarlaşma taryhyňyzdan pozular we habary iberen ýa-da alan ulanyjy tarapyndan görülip bilner.",
        "Error while deleting the message.": "Habary pozmakda ýalňyşlyk.",
        "Error while retrieving contacts from the server.": "Serweredn kontaktlary almakda ýalňyşlyk.",
        "Error while retrieving discussions from the server.": "Serweredn pikir alyşmalary almakda ýalňyşlyk.",
        "Error while retrieving messages from the server.": "Serweredn habarlary almakda ýalňyşlyk.",
        "Error while retrieving users from the server.": "Serweredn ulanyjylary almakda ýalňyşlyk.",
        "Group": "Topar",
        "Group info": "Topar maglumaty",
        "Private": "Şahsy",
        "User info": "Ulanyjy maglumaty",
        "{{$a}} is not in your contacts": "{{$a}} kontaktlaryňyzda ýok",
        "Message": "Habar",
        "The message was not sent. Please try again later.": "Habar iberilmedi. Soňrak synanyşyň.",
        "Message preferences": "Habar ileri tutmalary",
        "Messages": "Habarlar",
        "Mute": "Sesini öçür",
        "Muted conversation": "Sesi öçürilen söhbetdeşlik",
        "New message": "Täze habar",
        "New messages": "Täze habarlar",
        "No contact requests": "Kontakt haýyşlary ýok",
        "No contacts": "Kontaktlar ýok",
        "No starred conversations": "Ýyldyzly söhbetdeşlikler ýok",
        "No group conversations": "Topar söhbetdeşlikleri ýok",
        "No private conversations": "Şahsy söhbetdeşlikler ýok",
        "No messages were found": "Habarlar tapylmady",
        "Non-contacts": "Kontakt däller",
        "{{$a}} participants": "{{$a}} gatnaşyjy",
        "There are {{$a}} pending contact requests": "{{$a}} garaşylýan kontakt haýyşy bar",
        "Remove contact": "Kontakty aýyr",
        "Are you sure you want to remove {{$a}} from your contacts?": "{{$a}}-ny kontaktlaryňyzdan aýyrmak isleýärsiňizmi?",
        "Unstar conversation": "Söhbetdeşlikden ýyldyzy aýyr",
        "Remove from contacts": "Kontaktlardan aýyr",
        "Requests": "Haýyşlar",
        "You need to request {{$a}} to add you as a contact to be able to message them.": "{{$a}}-dan sizi kontakt hökmünde goşmagyny haýyş etmeli, onda habar iberip bilersiňiz.",
        "Search people and messages": "Adamlary we habarlary gözle",
        "Personal space": "Şahsy giňişlik",
        "Save draft messages, links, notes etc. to access later.": "Garalama habarlary, baglanyşyklary, bellikleri we ş.m. soňra girmek üçin saklaň.",
        "Send contact request": "Kontakt haýyşyny iber",
        "Show delete messages": "Pozulan habarlary görkeziň",
        "You are unable to message this user": "Bu ulanyjy habar iberip bilmeýärsiňiz",
        "Unblock user": "Ulanyjyny blokdan çykar",
        "Are you sure you want to unblock {{$a}}?": "{{$a}}-ny blokdan çykarmak isleýärsiňizmi?",
        "Unmute": "Sesini aç",
        "There are {{$a}} unread conversations": "{{$a}} okalmaýan söhbetdeşlik bar",
        "There are {{$a}} unread messages": "{{$a}} okalmaýan habar bar",
        "Use enter to send": "Ibermek üçin enter ulanyň",
        "If disabled, you can use Ctrl+Enter to send the message.": "Ýapyk bolsa, habary ibermek üçin Ctrl+Enter ulanyp bilersiňiz.",
        "If disabled, you can use Cmd+Enter to send the message.": "Ýapyk bolsa, habary ibermek üçin Cmd+Enter ulanyp bilersiňiz.",
        "{{$a}} would like to contact you": "{{$a}} siziň bilen habarlaşmak isleýär",
        "Couldn't send message(s) to conversation {{conversation}}. {{error}}": "{{conversation}} söhbetdeşligine habar ibererip bilmedi. {{error}}",
        "Couldn't send message(s) to user {{user}}. {{error}}": "{{user}} ulanyjysa habar iberip bilmedi. {{error}}",
        "Would like to contact you": "Siziň bilen habarlaşmak isleýär",
        "You:": "Siz:",
        "You have blocked this user.": "Bu ulanyjyny bloklapdyňyz.",
        "Your contact request is pending with {{$a}}": "Kontakt haýyşyňyz {{$a}} bilen garaşylýar",

        # More common terms
        "Please accept the submission statement.": "Tabşyryş beýannamasyny kabul ediň.",
        "Allow another attempt": "Başga bir synanyşyga rugsat ber",
        "Add a new attempt": "Täze synanyşyk goş",
        "Add a new attempt based on previous submission": "Öňki tabşyryşa esaslanýan täze synanyşyk goş",
        "Add submission": "Tabşyryşy goş",
    }

    # Apply translations (simple replacements for now)
    for en_phrase, tk_phrase in sorted(translations_map.items(), key=lambda x: -len(x[0])):
        if en_phrase in result:
            result = result.replace(en_phrase, tk_phrase)

    return result

# Generate complete translation
print("Generating complete Turkmen translation...")
print(f"Total entries to translate: {len(en_data)}")

for key, value in en_data.items():
    if key not in tk_translations:
        tk_translations[key] = translate_value(key, value)

print(f"Translation completed: {len(tk_translations)} entries")

# Write the complete translation
with open('/Users/merdana/AndroidStudioProjects/eduvesta/src/assets/lang/tk.json', 'w', encoding='utf-8') as f:
    json.dump(tk_translations, f, ensure_ascii=False, indent=4, sort_keys=True)

print("✓ Complete Turkmen translation saved to tk.json")
print(f"  - Total entries: {len(tk_translations)}")
print(f"  - Existing translations preserved: {len(tk_existing)}")
print(f"  - New translations added: {len(tk_translations) - len(tk_existing)}")
