# Notifications message bus prototype
## The problem
There exists multiple brands, each brand has multiple users, also each brand has many reviews. Reviews are added/updated frequently. One have to accumulate changes in reviews and make aggregated notification of each responsible user.
## The solution
Redis as message bus with safe accumulation/consuming. For each user there exist a list of reviews to notify about. List is safe to push and pull reviews.
### Data storage
For monitoring of data usage each user stores its time of last data pulling. So for each user there exist:
- `{user_id}` key with list of reviews
- `{user_id}_last_pulled_at` key with time of last data pulling
### Testing details
Simple brand-user connection is stored in `example_users.json`. It contains connection of brand and users, something like: `{"Brand1": [1,2], "Brand2": [4]}`
### Processes
There exist four processes. For testing purposes they're implemented as four commands.
#### Push reviews
Simple pusher with two commands:
- `poetry run push_valid_data`. It generate random review_id for each valid user_id and push it to Redis
- `poetry run push_invalid_data`. It generate random review_id for random user_id (invalid data, user belongs to brand) and push it to Redis
#### Pull reviews
`poetry run pull`. It iterates over all known user_ids and pull data for them
#### Monitor database
`poetry run monitor`. Monitor worker that iterates over `{user_id}_last_pulled_at` keys and check if they are old.
#### Clean database
`poetry run clean {user_id}`. It remove `{user_id}` key and `{user_id}_last_pulled_at` key from Redis.
## Setup

```bash
git clone git@github.com:jaturken/notifications-prototype.git
cd notifications-prototype
poetry install
poetry shell
```
## Workflow
1. Start monitor worker in separate shell: `poetry run monitor`
2. Push valid data: `poetry run push_valid_data` and see data pushed
3. Pull data: `poetry run pull` and see data pulled
4. Check monitor log and see serenity
5. Push invalid data: `poetry run push_invalid_data` and see invalid data pushed
6. Pull data: `poetry run pull` and see no invalid data pulled
7. After 20 sec(default monitor config) check monitor log and see invalid data alerted
8. Clean invalid data: `poetry run clean {invalid_user_id}`
9. Check monitor logs and see serenity
