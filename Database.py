from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

 
password = "bs91HZDXuubCNpsE"
uri = f"mongodb+srv://mostafahesham1939:{password}@games.w7y92bm.mongodb.net/?retryWrites=true&w=majority"

 

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

 

db = client['projectgame']
collection = db['players']

print("Connected to MongoDB.")


def store_player_data(user_id, user_score, win_user):
    data = {
        'user_id': user_id,
        'user_score': user_score,
        'win_user': win_user
    }
    # Store data in MongoDB
    collection.update_one(
        {'user_id': user_id},
        {'$set': data},
        upsert=True
    )
    print('Data stored successfully.')


def retrieve_player_data(user_id):
    # Retrieve data from MongoDB
    data = collection.find_one({'user_id': user_id})
    if data:
        print('User ID:', data['user_id'])
        print('User Score:', data['user_score'])
        print('Win User:', data['win_user'])
    else:
        print('User not found.')


def update_player_score(user_id, new_score):
    # Update player score
    collection.update_one(
        {'user_id': user_id},
        {'$set': {'user_score': new_score}}
    )
    print('Player score updated successfully.')


def increment_player_score(user_id, increment):
    # Increment player score
    collection.update_one(
        {'user_id': user_id},
        {'$inc': {'user_score': increment}}
    )
    print('Player score incremented successfully.')


def delete_player_data(user_id):
    # Delete player data
    result = collection.delete_one({'user_id': user_id})
    if result.deleted_count > 0:
        print('Player data deleted successfully.')
    else:
        print('Player not found.')


# Example usage
store_player_data('18p7502', 500, 'Mostafa')

retrieve_player_data('18p7502')

update_player_score('18p7502', 700)

retrieve_player_data('18p7502')

increment_player_score('18p7502', 100)

retrieve_player_data('18p7502')

delete_player_data('18p7502')

retrieve_player_data('18p7502')

store_player_data('18p9203', 300, '3ssam')

retrieve_player_data('18p9203')
