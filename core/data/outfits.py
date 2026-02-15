import json
import os

# Define the outfits data
OUTFITS_DATA = {
    "1": {
        "name": "Outfit 1",
        "outfit": [
             {"id": "body-flesh", "type": "clothing", "amount": 1},
             {"id": "hair_front-n_malenew27", "type": "clothing", "amount": 1},
             {"id": "hair_back-n_doodlekitchen2024tomshair", "type": "clothing", "amount": 1},
             {"id": "nose-n_01", "type": "clothing", "amount": 1},
             {"id": "eyebrow-n_dailyquest2024cutbrows", "type": "clothing", "amount": 1},
             {"id": "mouth-n_aprilfoolsinvisible2020mouth", "type": "clothing", "amount": 1},
             {"id": "face_hair-n_newbasicfacehairupper14", "type": "clothing", "amount": 1},
             {"id": "shirt-n_goldilocksgrab2021tatteredsweater", "type": "clothing", "amount": 1},
             {"id": "pants-n_dailyquest2024khakipants", "type": "clothing", "amount": 1},
             {"id": "shoes-n_chaseitems2024sneakersallwhite", "type": "clothing", "amount": 1},
             {"id": "handbag-n_cartooncutiesskypass2022greenball", "type": "clothing", "amount": 1},
             {"id": "eye-n_costumepartyllludcgrabone2024jbrionneeye", "type": "clothing", "amount": 1},
             {"id": "hat-n_dailyquest2025kireyloveglasses", "type": "clothing", "amount": 1},
             {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
             {"id": "bag-n_pastelwitchskypass2022cat", "type": "clothing", "amount": 1}
        ]
    },
    "2": {
        "name": "Outfit 2",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_basic2018sidebangspulledback", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_moicdonatesprinkleswimweargrab2023sprinkletails", "type": "clothing", "amount": 1},
            {"id": "nose-n_01", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_basic2018newbrows03", "type": "clothing", "amount": 1},
            {"id": "mouth-n_11", "type": "clothing", "amount": 1},
            {"id": "shirt-n_duckdailyrewards2018ducktop", "type": "clothing", "amount": 1},
            {"id": "pants-n_aprilfoolsinvisible2020pants", "type": "clothing", "amount": 1},
            {"id": "shoes-n_chaseitems2024sneakersallwhite", "type": "clothing", "amount": 1},
            {"id": "eye-n_basic2018butterflyeyes", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "bag-n_pastelwitchskypass2022cat", "type": "clothing", "amount": 1},
            {"id": "hat-n_duckdailyrewards2018hoodiehat_1", "type": "clothing", "amount": 1}
        ]
    },
    "3": {
        "name": "Outfit 3",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_malenew27", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_spacerunnerup19moonhair", "type": "clothing", "amount": 1},
            {"id": "nose-n_01", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_dailyquest2024cutbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-n_aprilfoolsinvisible2020mouth", "type": "clothing", "amount": 1},
            {"id": "face_hair-n_newbasicfacehairupper14", "type": "clothing", "amount": 1},
            {"id": "shirt-n_farmanimal2019goatinacoat", "type": "clothing", "amount": 1},
            {"id": "pants-n_farmanimal2019goatpants", "type": "clothing", "amount": 1},
            {"id": "shoes-n_chaseitems2024sneakersallwhite", "type": "clothing", "amount": 1},
            {"id": "handbag-n_JanuaryDailyReward2021BerryBear", "type": "clothing", "amount": 1},
            {"id": "eye-n_costumepartyllludcgrabone2024jbrionneeye", "type": "clothing", "amount": 1},
            {"id": "hat-n_farmanimal2019hornyhood_1", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "bag-n_pastelwitchskypass2022cat", "type": "clothing", "amount": 1}
        ]
    },
    "4": {
        "name": "Outfit 4",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_malenew27", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_spacerunnerup19moonhair", "type": "clothing", "amount": 1},
            {"id": "nose-n_01", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_dailyquest2024cutbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-f_01", "type": "clothing", "amount": 1},
            {"id": "face_hair-n_newbasicfacehairupper14", "type": "clothing", "amount": 1},
            {"id": "shirt-n_astronautgrab2019spacesuit", "type": "clothing", "amount": 1},
            {"id": "pants-n_astronautgrab2019spacepants", "type": "clothing", "amount": 1},
            {"id": "shoes-n_astronautgrab2019spaceshoes", "type": "clothing", "amount": 1},
            {"id": "eye-n_costumepartyllludcgrabone2024jbrionneeye", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "hat-n_astronautgrab2019nasahelmet_3", "type": "clothing", "amount": 1}
        ]
    },
    "5": {
        "name": "Outfit 5",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-m_06", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_spacerunnerup19moonhair", "type": "clothing", "amount": 1},
            {"id": "nose-n_01", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_dailyquest2024cutbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-f_01", "type": "clothing", "amount": 1},
            {"id": "face_hair-n_newbasicfacehairupper14", "type": "clothing", "amount": 1},
            {"id": "shirt-n_2016newyearcoat", "type": "clothing", "amount": 1},
            {"id": "pants-n_2016newyearpants", "type": "clothing", "amount": 1},
            {"id": "shoes-n_2016newyearboots", "type": "clothing", "amount": 1},
            {"id": "eye-n_costumepartyllludcgrabone2024jbrionneeye", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "bag-n_emeralddaily2020thekitty", "type": "clothing", "amount": 1},
            {"id": "hat-n_2016newyeartophat_1", "type": "clothing", "amount": 1}
        ]
    },
    "6": {
        "name": "Outfit 6",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_octhrsupport2024halfgrabshort", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_octhrsupport2024halfgrabshort", "type": "clothing", "amount": 1},
            {"id": "nose-n_octhrsupport2024blushednose", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_octhrsupport2024brashedbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-n_octhrsupport2024sweetlips", "type": "clothing", "amount": 1},
            {"id": "shirt-n_octhrsupport2024pinkshirtnskirt", "type": "clothing", "amount": 1},
            {"id": "pants-n_junepicnicskypassudc2023picnicshorts", "type": "clothing", "amount": 1},
            {"id": "shoes-n_octhrsupport2024pinkplatformwhitepantys", "type": "clothing", "amount": 1},
            {"id": "eye-n_octhrsupport2024almond", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "bag-n_emeralddaily2020thekitty", "type": "clothing", "amount": 1},
            {"id": "hat-n_octhrsupport2024pinkcap", "type": "clothing", "amount": 1}
        ]
    },
    "7": {
        "name": "Outfit 7",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_octhrsupport2024halfgrabshort", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_octhrsupport2024halfgrabshort", "type": "clothing", "amount": 1},
            {"id": "nose-n_octhrsupport2024blushednose", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_octhrsupport2024brashedbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-n_octhrsupport2024sweetlips", "type": "clothing", "amount": 1},
            {"id": "shirt-n_mummyjacket", "type": "clothing", "amount": 1},
            {"id": "pants-n_mummypants", "type": "clothing", "amount": 1},
            {"id": "shoes-n_mummyslippers", "type": "clothing", "amount": 1},
            {"id": "eye-n_octhrsupport2024almond", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "handbag-n_mummyplush", "type": "clothing", "amount": 1},
            {"id": "hat-n_mummyhat_3", "type": "clothing", "amount": 1}
        ]
    },
    "8": {
        "name": "Outfit 8",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_arcticfriendsskypass2022frozentipsmale", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_arcticfriendsskypass2022frozentipsmale", "type": "clothing", "amount": 1},
            {"id": "nose-n_01", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_dailyquest2024cutbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-n_aprilfoolsinvisible2020mouth", "type": "clothing", "amount": 1},
            {"id": "shirt-n_electionsuitwhite", "type": "clothing", "amount": 1},
            {"id": "pants-n_electionpantswhite", "type": "clothing", "amount": 1},
            {"id": "shoes-n_chaseitems2024sneakersallwhite", "type": "clothing", "amount": 1},
            {"id": "eye-n_decturquoise2020turquoiseeyes", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1}
        ]
    },
    "9": {
        "name": "Outfit 9",
        "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_2016ninjaponytail", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_2016ninjaponytail", "type": "clothing", "amount": 1},
            {"id": "nose-n_01", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_dailyquest2024cutbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-n_aprilfoolsinvisible2020mouth", "type": "clothing", "amount": 1},
            {"id": "shirt-n_2016ninjadress", "type": "clothing", "amount": 1},
            {"id": "pants-n_2016ninjashorts", "type": "clothing", "amount": 1},
            {"id": "shoes-n_2016ninjashoes", "type": "clothing", "amount": 1},
            {"id": "eye-n_decturquoise2020turquoiseeyes", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "skirt-n_schoolreportertightskirt", "type": "clothing", "amount": 1},
            {"id": "gloves-n_2016ninjagloves", "type": "clothing", "amount": 1},
            {"id": "glasses-n_2016snowboardgogglesblack", "type": "clothing", "amount": 1}
        ]
    },
    "10": {
         "name": "Outfit 10",
         "outfit": [
            {"id": "body-flesh", "type": "clothing", "amount": 1},
            {"id": "hair_front-n_2016ninjahair", "type": "clothing", "amount": 1},
            {"id": "hair_back-n_2016ninjahair", "type": "clothing", "amount": 1},
            {"id": "nose-n_01", "type": "clothing", "amount": 1},
            {"id": "eyebrow-n_dailyquest2024cutbrows", "type": "clothing", "amount": 1},
            {"id": "mouth-n_aprilfoolsinvisible2020mouth", "type": "clothing", "amount": 1},
            {"id": "shirt-n_2016ninjashirt", "type": "clothing", "amount": 1},
            {"id": "pants-n_2016ninjapants", "type": "clothing", "amount": 1},
            {"id": "shoes-n_2016ninjaboots", "type": "clothing", "amount": 1},
            {"id": "eye-n_decturquoise2020turquoiseeyes", "type": "clothing", "amount": 1},
            {"id": "freckle-n_registrationavatars2023contour", "type": "clothing", "amount": 1},
            {"id": "skirt-n_schoolreportertightskirt", "type": "clothing", "amount": 1},
            {"id": "gloves-n_2016ninjahalfgloves", "type": "clothing", "amount": 1},
            {"id": "glasses-n_2016snowboardgogglesblack", "type": "clothing", "amount": 1}
         ]
    }
}

def get_outfit(index: str):
    return OUTFITS_DATA.get(index)
