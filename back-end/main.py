from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
neo4j_uri = os.getenv("NEO4J_URI")

# Initialize the driver
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

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

def create_like_relationship(user_name, soccer_name):
   with driver.session() as session:
      session.write_transaction(_create_like_relationship, user_name, soccer_name)

def _create_like_relationship(tx, user_name, soccer_name):
   query = (
      "MATCH (u:User {name: $user_name}), (s:Soccer {name: $soccer_name}) "
      "CREATE (u)-[:LIKE]->(s) "
      "RETURN u, s"
   )
   result = tx.run(query, user_name=user_name, soccer_name=soccer_name)
   return result.single()

def find_users_who_like_soccer():
   with driver.session() as session:
      result = session.execute_read(_find_users_who_like_soccer)
      return result

def _find_users_who_like_soccer(tx):
   query = (
      "MATCH (u:User)-[:LIKE]->(s:Soccer)"
      "RETURN u"
   )
   result = tx.run(query)
   return [record["u"] for record in result]

# Example usage
# create_user_node("Alice")
# create_like_relationship("Alice", "Soccer")

users_who_like_soccer = find_users_who_like_soccer()
for user in users_who_like_soccer:
   print(user.get("name"))

# Close the driver
driver.close()