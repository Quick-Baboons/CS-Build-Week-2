import time
from rooms import rooms

unique_rooms = {}

for room in rooms:
    room_id = str(room['room_id'])
    room_title = room['title']
    if room_title not in unique_rooms:
        unique_rooms[room_title] = {
            'room_id': room_id,
            'amount': 1
        }
    else:
        unique_rooms[room_title]['amount'] += 1

# for unique_room in unique_rooms:
#     if unique_room['amount'] > 1:
#         del unique_room

print(unique_rooms)



{ 
   'Wishing Well':{ 
      'room_id':'55',
      'amount':1
   },
   'Shop':{ 
      'room_id':'1',
      'amount':1
   },
   'A misty room':{ 
      'room_id':'8',
      'amount':424
   },
   'Mt. Holloway':{ 
      'room_id':'3',
      'amount':29
   },
   'A brightly lit room':{ 
      'room_id':'0',
      'amount':1
   },
   'The Peak of Mt. Holloway':{ 
      'room_id':'22',
      'amount':1
   },
   'A Dark Cave':{ 
      'room_id':'216',
      'amount':36
   },
   "Glasowyn's Grave":{ 
      'room_id':'499',
      'amount':1
   },
   "Linh's Shrine":{ 
      'room_id':'461',
      'amount':1
   },
   "Pirate Ry's":{ 
      'room_id':'467',
      'amount':1
   },
   "Sandofsky's Sanctum":{ 
      'room_id':'492',
      'amount':1
   },
   'Fully Shrine':{ 
      'room_id':'374',
      'amount':1
   },
   "Arron's Athenaeum":{ 
      'room_id':'486',
      'amount':1
   },
   'The Transmogriphier':{ 
      'room_id':'495',
      'amount':1
   }
}