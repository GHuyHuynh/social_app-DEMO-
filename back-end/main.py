from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
neo4j_uri = os.getenv("NEO4J_URI")

# Initialize the driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))


# Create a user node
def create_user_node(name):
   with driver.session() as session:
      session.write_transaction(_create_and_return_user, name)

def _create_and_return_user(tx, name):
   query = (
      "CREATE (u:User {name: $name}) "
      "RETURN u"
   )
   result = tx.run(query, name=name)
   return result.single()


# Create a hobby node
def create_hobby_node(name):
   with driver.session() as session:
      session.write_transaction(_create_and_return_hobby, name)

def _create_and_return_hobby(tx, name):
   query = (
      "CREATE (h:Hobby {name: $name}) "
      "RETURN h"
   )
   result = tx.run(query, name=name)
   return result.single()


# Create an event node and relate it to multiple hobbies
def create_event_node(event_name, hobby_names):
   with driver.session() as session:
      session.write_transaction(_create_and_return_event, event_name, hobby_names)

def _create_and_return_event(tx, event_name, hobby_names):
   query = (
      "CREATE (e:Event {name: $event_name}) "
      "WITH e "
      "UNWIND $hobby_names AS hobby_name "
      "MATCH (h:Hobby {name: hobby_name}) "
      "CREATE (e)-[:RELATED_TO]->(h) "
      "RETURN e"
   )
   result = tx.run(query, event_name=event_name, hobby_names=hobby_names)
   return result.single()



# Create an attends relationship between a user and an event
def create_attends_relationship(user_name, event_name):
   with driver.session() as session:
      session.write_transaction(_create_attends_relationship, user_name, event_name)

def _create_attends_relationship(tx, user_name, event_name):
   query = (
      "MATCH (u:User {name: $user_name}) "
      "MATCH (e:Event {name: $event_name}) "
      "CREATE (u)-[:ATTENDS]->(e)"
   )
   tx.run(query, user_name=user_name, event_name=event_name)



# Create a user like relationship to a hobby
def create_like_hobby_relationship(user_name, hobby_name):
   with driver.session() as session:
      session.write_transaction(_create_like_hobby_relationship, user_name, hobby_name)

def _create_like_hobby_relationship(tx, user_name, hobby_name):
   query = (
      "MATCH (u:User {name: $user_name}) "
      "MATCH (h:Hobby {name: $hobby_name}) "
      "CREATE (u)-[:LIKES]->(h)"
   )
   tx.run(query, user_name=user_name, hobby_name=hobby_name)


# Find all users that like a hobby
def find_users_that_like_hobby(hobby_name):
   with driver.session() as session:
      return session.read_transaction(_find_users_that_like_hobby, hobby_name)

def _find_users_that_like_hobby(tx, hobby_name):
   query = (
      "MATCH (u:User)-[:LIKES]->(h:Hobby {name: $hobby_name}) "
      "RETURN u.name"
   )
   result = tx.run(query, hobby_name=hobby_name)
   return [record["u.name"] for record in result]


# Find all users that attend an event
def find_users_that_attend_event(event_name):
   with driver.session() as session:
      return session.read_transaction(_find_users_that_attend_event, event_name)

def _find_users_that_attend_event(tx, event_name):
   query = (
      "MATCH (u:User)-[:ATTENDS]->(e:Event {name: $event_name}) "
      "RETURN u.name"
   )
   result = tx.run(query, event_name=event_name)
   return [record["u.name"] for record in result]


# Find all events for a user
def find_events_for_user(username):
   with driver.session() as session:
      events = session.read_transaction(_find_events, username)
      return events

def _find_events(tx, username):
   query = (
      "MATCH (u:User {name: $username})-[:LIKES]->(h:Hobby)<-[:RELATED_TO]-(e:Event) "
      "RETURN e.name AS event_name"
   )
   result = tx.run(query, username=username)
   return [record["event_name"] for record in result]



# Main function
def main():
   # create_user_node("Alice")
   # create_user_node("Bob")
   # create_user_node("Charlie")

   # create_hobby_node("Swimming")
   # create_hobby_node("Running")
   # create_hobby_node("Cycling")
   # create_hobby_node("Soccer")

   # create_like_hobby_relationship("Alice", "Swimming")
   # create_like_hobby_relationship("Alice", "Running")
   # create_like_hobby_relationship("Bob", "Running")
   # create_like_hobby_relationship("Charlie", "Cycling")
   # create_like_hobby_relationship("Alice", "Cycling")
   # create_like_hobby_relationship("Charlie", "Soccer")

   # create_event_node("Triathlon", ["Swimming", "Running", "Cycling"])
   # create_event_node("Soccer Tournament", ["Soccer"])

   # create_attends_relationship("Alice", "Triathlon")
   # create_attends_relationship("Bob", "Triathlon")

   print(find_users_that_like_hobby("Cycling"))

   print(find_users_that_attend_event("Triathlon"))


   events_for_charlie = find_events_for_user("Charlie")
   print(events_for_charlie)

main()

# Close the driver
driver.close()

