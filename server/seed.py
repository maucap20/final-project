from app import db, User, Organization, VolunteerOpportunity

# Create sample users
user1 = User(email='user1@example.com', password='password1')
user2 = User(email='user2@example.com', password='password2')

# Create sample organizations
org1 = Organization(name='Charity A', description='Helping those in need')
org2 = Organization(name='Nonprofit B', description='Supporting local communities')

# Create sample volunteer opportunities
opportunity1 = VolunteerOpportunity(
    title='Food Drive',
    description='Collecting food donations for the homeless',
    organization=org1,
)
opportunity2 = VolunteerOpportunity(
    title='Community Cleanup',
    description='Cleaning up local parks and streets',
    organization=org2,
)

# Add and commit the data to the database
db.session.add_all([user1, user2, org1, org2, opportunity1, opportunity2])
db.session.commit()