try:
    from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import relationship, sessionmaker
    from sys import argv
    import os
    print("All Modules Loaded....")
except:
    print("Modules Not Found")

script, state_user = argv

#Directory that I am working in
basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)
# print('=='*50)

DATABASE = 'nba1.db'

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    points = Column(Integer)
    team_id = Column(String, ForeignKey('teams.id'))

    def __init__(self, name, points, team_id):
        self.name = name
        self.points = points
        self.team_id = team_id


class Team(Base):
    __tablename__ = 'teams'

    id = Column(String, primary_key=True)
    name = Column(String)
    state = Column(String)
    players = relationship('Player', backref='team')

    def __init__(self, team_id, name, state):
        self.id = team_id
        self.name = name
        self.state = state


# delete the database if it already exists
if os.path.exists(DATABASE):
    os.remove(DATABASE)


engine = create_engine(
    f'sqlite:///{DATABASE}',
    # uncomment the next line to see sqlalchemy working some database magic
    # echo=True
)
Session = sessionmaker(bind=engine)
session = Session()

Player.__table__.create(engine)
Team.__table__.create(engine)


with open('nba-teams.csv', 'r') as nba_teams:
    teams = []
    for line in nba_teams:
        team_id, team_name, state = line.strip().split(',')
        team = Team(team_id, team_name, state)
        teams.append(team)
    session.add_all(teams)
    session.commit()


with open('nba-stats.csv', 'r') as nba_stats:
    players = []
    for line in nba_stats:
        player_name, team_abbrev, points = line.strip().split(',')
        player = Player(player_name, points, team_abbrev)
        players.append(player)
    session.add_all(players)
    session.commit()

# def query():
#     data = Player.query.all()
#     print(data)

# if __name__ == "__main__":
#     query()

players = session.query(Player).join(Team).filter(Team.state ==f'{state_user}').all()
for player in players:
    print(player.name, player.points, player.team.name, state_user)






























# def create_database():
#     Database.create()
#     Lebron = nba_player('Lebron James',  2500, 'LJA')
#     Kobe = nba_player('Kobe Bryant',  2600, 'KBA')
#     Jordan = nba_player('Michael Jordan',  2700, 'MJA')
#
#     Database.session.add_all(Lebron)
#     Database.session.add_all(Kobe)
#     Database.sesson.add_all(Jordan)
#
#     Database.session.commit()
#     print("Database Created")
#
# if __name__ == "__main__":
#     create_database()
