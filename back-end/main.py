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


# Create a user like relationship to a hobby
def create_like_relationship(user_name, hobby_name):
   with driver.session() as session:
      session.write_transaction(_create_like_relationship, user_name, hobby_name)

def _create_like_relationship(tx, user_name, hobby_name):
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


# Main function
def main():
   # create_user_node("Alice")
   # create_user_node("Bob")
   # create_user_node("Charlie")

   # create_hobby_node("Swimming")
   # create_hobby_node("Running")
   # create_hobby_node("Cycling")

   # create_like_relationship("Alice", "Swimming")
   # create_like_relationship("Alice", "Running")
   # create_like_relationship("Bob", "Running")
   # create_like_relationship("Charlie", "Cycling")

   print(find_users_that_like_hobby("Running"))

main()

# Close the driver
driver.close()

