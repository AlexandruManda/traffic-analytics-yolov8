print('Start #################################################################');

db = db.getSiblingDB('trackerDb');
db.createUser(
  {
    user: 'init',
    pwd: 'init',
    roles: [{ role: 'readWrite', db: 'trackerDb' }],
  },
);
db.createCollection('trackerConfig');

print('END #################################################################');


